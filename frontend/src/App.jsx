import { useState } from 'react'
import Wizard from './components/Wizard'
import Dashboard from './components/Dashboard'

function App() {
  const [view, setView] = useState('wizard')
  const [config, setConfig] = useState(null)

  const handleStart = (configData) => {
    setConfig(configData)
    setView('dashboard')
  }

  return (
    <div className="app">
      {view === 'wizard' && <Wizard onStart={handleStart} />}
      {view === 'dashboard' && <Dashboard config={config} />}
    </div>
  )
}

export default App
