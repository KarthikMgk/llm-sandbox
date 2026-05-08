import { useState } from 'react'
import axios from 'axios'

function Wizard({ onStart }) {
  const [apiKey, setApiKey] = useState('')
  const [model, setModel] = useState('minimax-01')
  const [containerImage, setContainerImage] = useState('ubuntu:22.04')
  const [agentKey, setAgentKey] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    setLoading(true)
    try {
      await axios.post('/api/config', null, {
        params: { apiKey, model, containerImage, agentKey }
      })
      await axios.post('/api/sandbox/start')
      onStart({ apiKey, model, containerImage, agentKey })
    } catch (error) {
      console.error('Failed to start sandbox:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="wizard">
      <h1>Sandbox Setup</h1>
      <div className="form-group">
        <label>API Key</label>
        <input
          type="password"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          placeholder="Enter your API key"
        />
      </div>
      <div className="form-group">
        <label>Model</label>
        <input
          type="text"
          value={model}
          onChange={(e) => setModel(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label>Container Image</label>
        <input
          type="text"
          value={containerImage}
          onChange={(e) => setContainerImage(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label>Agent Key</label>
        <input
          type="password"
          value={agentKey}
          onChange={(e) => setAgentKey(e.target.value)}
          placeholder="Agent authentication key"
        />
      </div>
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Starting...' : 'Start Sandbox'}
      </button>
    </div>
  )
}

export default Wizard
