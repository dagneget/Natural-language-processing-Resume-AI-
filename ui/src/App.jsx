import { useState } from 'react'
import { Upload, FileText, CheckCircle, AlertCircle, Award, Briefcase, Zap, Mail } from 'lucide-react'
import './index.css'

function App() {
  const [file, setFile] = useState(null)
  const [jd, setJd] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setResult(null)
    setError(null)
  }

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please select a resume file.")
      return
    }

    setLoading(true)
    setError(null)
    const formData = new FormData()
    formData.append("resume", file)
    formData.append("job_description", jd)

    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error("Analysis failed. Please try again.")
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header className="header">
        <div className="logo">
          <Zap className="logo-icon" />
          <span>ResumeAI</span>
        </div>
        <p className="subtitle">Automated Screening & Skill Extraction</p>
      </header>

      <main className="main-content">
        <div className="card upload-section">
          <h2><Briefcase className="icon" /> Job Description</h2>
          <textarea
            className="jd-input"
            value={jd}
            onChange={(e) => setJd(e.target.value)}
            placeholder="Paste Job Description here..."
          />

          <h2><Upload className="icon" /> Upload Resume</h2>
          <div className="file-input-wrapper">
            <input type="file" id="resume-upload" onChange={handleFileChange} accept=".pdf,.docx,.txt" />
            <label htmlFor="resume-upload" className="file-label">
              {file ? (
                <span className="file-name"><FileText className="inline-icon" /> {file.name}</span>
              ) : (
                <span>Choose a PDF/DOCX file</span>
              )}
            </label>
          </div>

          <button className="analyze-btn" onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Candidate"}
          </button>

          {error && <div className="error-msg"><AlertCircle size={16} /> {error}</div>}
        </div>

        {result && (
          <div className="card result-section fade-in">
            <div className="score-header">
              <div className="score-circle" style={{
                background: `conic-gradient(#4ADE80 ${result.score * 3.6}deg, #374151 0deg)`
              }}>
                <div className="score-inner">
                  <span className="score-value">{result.score}%</span>
                  <span className="score-label">Match</span>
                </div>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem' }}>
                <div>
                  <h3><Mail className="icon" /> Contact Info</h3>
                  <p>Email: {result.contact.email || 'N/A'}</p>
                  <p>Phone: {result.contact.phone || 'N/A'}</p>

                  {result.education && result.education.length > 0 && (
                    <div style={{ marginTop: '0.5rem' }}>
                      <strong>Education:</strong> {result.education.join(', ')}
                    </div>
                  )}
                  {result.experience && (
                    <div style={{ marginTop: '0.5rem' }}>
                      <strong>Experience:</strong> {result.experience} years
                    </div>
                  )}

                  {result.category && (
                    <p style={{ marginTop: '1rem', color: '#60A5FA', fontWeight: 'bold' }}>
                      Detected Field: {result.category}
                    </p>
                  )}
                </div>
              </div>

              <div className="skills-container">
                <h3><Award className="icon" /> Extracted Skills</h3>
                <div className="tags">
                  {result.skills.map((skill, index) => (
                    <span key={index} className="tag">{skill}</span>
                  ))}
                  {result.skills.length === 0 && <span className="no-skills">No specific skills detected.</span>}
                </div>
              </div>

              {result.missing_skills && result.missing_skills.length > 0 && (
                <div className="skills-container" style={{ marginTop: '1.5rem', border: '1px solid #FECACA', background: '#FEF2F2', padding: '1rem', borderRadius: '0.5rem' }}>
                  <h3 style={{ color: '#DC2626' }}><AlertCircle className="icon" size={20} /> Missing Skills from JD</h3>
                  <div className="tags">
                    {result.missing_skills.map((skill, index) => (
                      <span key={index} className="tag" style={{ background: '#FEE2E2', color: '#B91C1C', border: '1px solid #FCA5A5' }}>{skill}</span>
                    ))}
                  </div>
                </div>
              )}

              {/* Keyword Highlighting Section */}
              {result.summary && (
                <div className="card" style={{ marginTop: '2rem', padding: '1rem', background: '#1F2937' }}>
                  <h3><FileText className="icon" /> Resume Preview (Keywords Highlighted)</h3>
                  <div style={{ padding: '1rem', background: '#111827', borderRadius: '0.5rem', maxHeight: '300px', overflowY: 'auto', whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>
                    {(() => {
                      // Simple highlighting logic
                      const text = result.summary;
                      const skills = new Set(result.skills.map(s => s.toLowerCase()));
                      const parts = text.split(/(\b\w+\b)/g); // basic tokenizer

                      return parts.map((part, i) => {
                        if (skills.has(part.toLowerCase())) {
                          return <span key={i} style={{ background: '#F59E0B', color: '#000', padding: '0 2px', borderRadius: '2px', fontWeight: 'bold' }}>{part}</span>
                        }
                        return part;
                      })
                    })()}
                  </div>
                </div>
              )}

              {result.report_url && (
                <div style={{ marginTop: '2rem', textAlign: 'center' }}>
                  <a
                    href={`http://localhost:8000${result.report_url}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="analyze-btn"
                    style={{ display: 'inline-block', width: 'auto', textDecoration: 'none', background: '#10B981' }}
                  >
                    <FileText className="inline-icon" style={{ marginRight: '8px' }} />
                    Download Official Report (PDF)
                  </a>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
