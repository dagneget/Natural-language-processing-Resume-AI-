from fpdf import FPDF
import os

class PDFReport(FPDF):
    def header(self):
        # Logo
        self.set_font('helvetica', 'B', 20)
        self.cell(0, 10, 'Candidate Screening Report', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def clean_text(text):
    if not text: return ""
    # Common unsupported characters in standard PDF fonts
    replacements = {
        "ﬁ": "fi", "ﬂ": "fl",
        "’": "'", "‘": "'",
        "“": '"', "”": '"',
        "–": "-", "—": "-"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Encode to latin-1 (standard PDF encoding) and replace unknowns with ?
    return text.encode('latin-1', 'replace').decode('latin-1')

def generate_report(candidate_data, job_description, filename):
    pdf = PDFReport()
    pdf.add_page()
    
    # 1. Candidate Info
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, f"Candidate: {clean_text(filename)}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('helvetica', '', 12)
    contact = candidate_data.get('contact', {})
    pdf.cell(0, 8, f"Email: {clean_text(contact.get('email', 'N/A'))}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Phone: {clean_text(contact.get('phone', 'N/A'))}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    # Education & Experience
    education = candidate_data.get('education', [])
    experience = candidate_data.get('experience')
    
    if education:
        pdf.cell(0, 8, f"Education: {clean_text(', '.join(education))}", new_x="LMARGIN", new_y="NEXT")
    if experience:
        pdf.cell(0, 8, f"Experience: {clean_text(experience)} years identified", new_x="LMARGIN", new_y="NEXT")
        
    pdf.ln(10)

    # 2. Score Section
    score = candidate_data.get('score', 0)
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, "Match Score", new_x="LMARGIN", new_y="NEXT")
    
    # Simple ASCII Bar Chart logic or just Color Text
    pdf.set_font('helvetica', 'B', 24)
    if score >= 70:
        pdf.set_text_color(16, 185, 129) # Green
    elif score >= 50:
        pdf.set_text_color(245, 158, 11) # Orange
    else:
        pdf.set_text_color(239, 68, 68) # Red
        
    pdf.cell(0, 15, f"{score}%", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0) # Reset
    pdf.ln(5)

    # 3. Skills Section
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, "Extracted Skills", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', '', 11)
    
    skills = candidate_data.get('skills', [])
    if skills:
        # Wrap skills nicely
        skills_text = ", ".join(skills)
        pdf.multi_cell(0, 8, clean_text(skills_text))
    else:
        pdf.cell(0, 8, "No specific skills detected.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # 3.1 Missing Skills (if any)
    missing = candidate_data.get('missing_skills', [])
    if missing:
        pdf.set_text_color(239, 68, 68) # Red
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 10, "Missing Skills from JD:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('helvetica', '', 11)
        pdf.multi_cell(0, 8, clean_text(", ".join(missing)))
        pdf.set_text_color(0, 0, 0) # Reset
        pdf.ln(5)

    # 4. Job Description Snippet
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, "Job Text Snippet", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', 'I', 10)
    pdf.multi_cell(0, 6, clean_text(job_description[:500]) + "...")
    
    # Output
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    out_path = os.path.join(reports_dir, f"Report_{filename}.pdf")
    pdf.output(out_path)
    
    return out_path
