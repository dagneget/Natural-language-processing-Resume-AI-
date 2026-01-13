import { useState } from 'react'
import { Upload, FileText, CheckCircle, AlertCircle, Award, Briefcase, Zap, Mail, Download, Target, Cpu, User } from 'lucide-react'
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

  const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000"

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
      const response = await fetch(`${API_BASE}/analyze`, {
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
        <p className="subtitle">PRECISION SEMANTIC SCREENING ENGINE</p>
      </header>

      <main className="main-content">
        <div className="card">
          <h2><Briefcase className="icon" /> Job Context</h2>
          <textarea
            className="jd-input"
            value={jd}
            onChange={(e) => setJd(e.target.value)}
            placeholder="Paste the job description here to enable semantic matching..."
          />

          <h2><Upload className="icon" /> Resume / CV</h2>
          <div className="file-input-wrapper">
            <input type="file" id="resume-upload" onChange={handleFileChange} accept=".pdf,.docx,.txt" />
            <label htmlFor="resume-upload" className="file-label">
              {file ? (
                <span className="file-name"><FileText className="inline-icon" /> {file.name}</span>
              ) : (
                <>
                  <Upload size={32} style={{ marginBottom: '1rem', opacity: 0.5 }} />
                  <span>Drop your PDF/DOCX here</span>
                  <span style={{ fontSize: '0.8rem', opacity: 0.6, marginTop: '0.5rem' }}>or click to browse</span>
                </>
              )}
            </label>
          </div>

          <button className="analyze-btn" onClick={handleAnalyze} disabled={loading}>
            {loading ? (
              <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
                <Cpu className="animate-spin" /> Neural Analysis in Progress...
              </span>
            ) : "Start Intelligence Scan"}
          </button>

          {error && <div className="error-msg" style={{ color: '#ef4444', marginTop: '1rem', textAlign: 'center' }}><AlertCircle size={16} /> {error}</div>}
        </div>

        {result ? (
          <div className="card fade-in">
            <div className="score-visual">
              <div className="score-circle" style={{
                background: `conic-gradient(#8b5cf6 ${result.score * 3.6}deg, rgba(255,255,255,0.1) 0deg)`
              }}>
                <div className="score-inner">
                  <span className="score-value">{result.score}%</span>
                  <span className="score-label">Match</span>
                </div>
              </div>
              <div style={{ flex: 1 }}>
                <h3 style={{ textTransform: 'none', margin: 0, fontSize: '1.5rem' }}>{result.filename}</h3>
                <p style={{ color: '#818cf8', fontWeight: 600, margin: '5px 0' }}>{result.category} Specialist</p>
                <div style={{ display: 'flex', gap: '1rem', marginTop: '10px' }}>
                  <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}><Mail size={14} className="inline-icon" /> {result.contact.email || 'No Email'}</div>
                  {result.experience && <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}><Target size={14} className="inline-icon" /> {result.experience} Exp</div>}
                </div>
              </div>
            </div>

            <div className="info-grid" style={{ marginTop: '1rem' }}>
              <div className="info-item">
                <label><User size={12} /> Domain Fit</label>
                <div style={{ height: '6px', background: '#334155', borderRadius: '3px', marginTop: '8px' }}>
                  <div style={{ width: `${Math.min(result.score + 10, 100)}%`, height: '100%', background: 'linear-gradient(to right, #8b5cf6, #ec4899)', borderRadius: '3px' }}></div>
                </div>
              </div>
              <div className="info-item">
                <label><Award size={12} /> Skill Match</label>
                <div style={{ height: '6px', background: '#334155', borderRadius: '3px', marginTop: '8px' }}>
                  <div style={{ width: `${(result.skills.length / (result.skills.length + (result.missing_skills?.length || 0)) * 100) || 0}%`, height: '100%', background: '#10b981', borderRadius: '3px' }}></div>
                </div>
              </div>
            </div>

            <div style={{ marginTop: '2rem' }}>
              <h3><Target className="icon" /> Skill Inventory</h3>
              <div className="tags">
                {result.skills.map((skill, index) => (
                  <span key={index} className="tag">{skill}</span>
                ))}
                {result.missing_skills?.map((skill, index) => (
                  <span key={index} className="tag tag-missing">{skill}</span>
                ))}
              </div>
            </div>

            {result.summary && (
              <div style={{ marginTop: '2rem' }}>
                <h3><FileText className="icon" /> Semantic Preview</h3>
                <div className="preview-container">
                  {(() => {
                    const text = result.summary;
                    const skills = new Set(result.skills.map(s => s.toLowerCase()));
                    const words = text.split(/(\b\w+\b)/g);
                    return words.map((word, i) => {
                      if (skills.has(word.toLowerCase())) {
                        return <span key={i} className="highlight">{word}</span>
                      }
                      return word;
                    })
                  })()}
                </div>
              </div>
            )}

            {result.report_url && (
              <a
                href={`${API_BASE}${result.report_url}`}
                target="_blank"
                rel="noopener noreferrer"
                className="download-link"
              >
                <Download size={20} />
                Generate Deep Analysis Report (PDF)
              </a>
            )}
          </div>
        ) : (
          <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: 0.8, borderStyle: 'dashed' }}>
            <Target size={48} style={{ opacity: 0.2, marginBottom: '1rem' }} />
            <p style={{ color: '#94a3b8', textAlign: 'center' }}>Upload a resume to begin semantic ranking and skill extraction.</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App

