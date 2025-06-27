import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [faqs, setFaqs] = useState<any[]>([])
  const [logs, setLogs] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function fetchData() {
    setLoading(true)
    try {
      const faqRes = await fetch('http://localhost:8000/ivr/faq')
      const logRes = await fetch('http://localhost:8000/ivr/logs')
      const faqData = await faqRes.json()
      const logData = await logRes.json()
      setFaqs(faqData.faqs)
      setLogs(logData.logs)
    } catch (e) {
      // handle error
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  async function handleAddFaq(e: React.FormEvent) {
    e.preventDefault()
    setSubmitting(true)
    const form = new FormData()
    form.append('question', question)
    form.append('answer', answer)
    await fetch('http://localhost:8000/ivr/faq', {
      method: 'POST',
      body: form
    })
    setQuestion('')
    setAnswer('')
    setSubmitting(false)
    fetchData()
  }

  async function handleDeleteFaq(id: string) {
    await fetch(`http://localhost:8000/ivr/faq/${id}`, { method: 'DELETE' })
    fetchData()
  }

  async function handleDeleteLog(id: string) {
    await fetch(`http://localhost:8000/ivr/logs/${id}`, { method: 'DELETE' })
    fetchData()
  }

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <h2>IVR Admin Panel</h2>
      {loading ? <p>Loading...</p> : (
        <>
          <section>
            <h3>FAQs</h3>
            <form onSubmit={handleAddFaq} style={{marginBottom: 16}}>
              <input
                type="text"
                placeholder="Question"
                value={question}
                onChange={e => setQuestion(e.target.value)}
                required
              />
              <input
                type="text"
                placeholder="Answer"
                value={answer}
                onChange={e => setAnswer(e.target.value)}
                required
              />
              <button type="submit" disabled={submitting}>Add FAQ</button>
            </form>
            <ul>
              {faqs.length === 0 ? <li>No FAQs found.</li> : faqs.map((faq) => (
                <li key={faq.id}>
                  <b>{faq.question}</b>: {faq.answer}
                  <button onClick={() => handleDeleteFaq(faq.id)} style={{marginLeft: 8}}>Delete</button>
                </li>
              ))}
            </ul>
          </section>
          <section>
            <h3>Call Logs</h3>
            <ul>
              {logs.length === 0 ? <li>No logs found.</li> : logs.map((log) => (
                <li key={log.id}>
                  Caller: {log.caller || 'Unknown'} | <a href={log.recording_url} target="_blank" rel="noopener noreferrer">Recording</a>
                  <button onClick={() => handleDeleteLog(log.id)} style={{marginLeft: 8}}>Delete</button>
                </li>
              ))}
            </ul>
          </section>
        </>
      )}
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
