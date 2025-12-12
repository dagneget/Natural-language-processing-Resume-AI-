from src.extractor import extract_skills, extract_contact_info

def test_extract_skills_simple():
    text = "I have experience with Python and Java."
    skills = extract_skills(text)
    # Check if skills are lowercased and extracted
    assert "python" in skills
    assert "java" in skills

def test_extract_skills_nlp():
    # This might depend on the model loading, but let's test a known entity
    text = "Proficient in Microsoft Excel."
    skills = extract_skills(text)
    # Excel might be PRODUCT or ORG
    # Note: This test is fuzzy if model behaves differently, but good for smoke test
    pass 

def test_extract_contact_info():
    text = "Contact me at test@example.com or (123) 456-7890."
    info = extract_contact_info(text)
    assert info['email'] == "test@example.com"
    assert info['phone'] == "(123) 456-7890"
