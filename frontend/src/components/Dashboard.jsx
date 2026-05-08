import { useState, useEffect } from 'react'
import Terminal from './Terminal'
import Timeline from './Timeline'
import FileExplorer from './FileExplorer'
import StatusBar from './StatusBar'
import axios from 'axios'

function Dashboard({ config }) {
  const [sandbox, setSandbox] = useState(null)
  const [timelineEvents, setTimelineEvents] = useState([])

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await axios.get('/api/sandbox/status')
        setSandbox(response.data)
      } catch (error) {
        // Sandbox not yet started or not found
      }
    }
    fetchStatus()
    const interval = setInterval(fetchStatus, 2000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    const fetchTimeline = async () => {
      try {
        const response = await axios.get('/api/timeline')
        setTimelineEvents(response.data)
      } catch (error) {
        // Timeline not available
      }
    }
    fetchTimeline()
    const interval = setInterval(fetchTimeline, 2000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="dashboard">
      <header className="header">
        <span>sandbox-{sandbox?.id || '...'}</span>
        <span>{sandbox?.status || '...'}</span>
      </header>
      <div className="main">
        <div className="left-panel">
          <Terminal sandboxId={sandbox?.id} />
          <FileExplorer sandboxId={sandbox?.id} />
        </div>
        <div className="right-panel">
          <Timeline events={timelineEvents} />
          <StatusBar sandbox={sandbox} />
        </div>
      </div>
    </div>
  )
}

export default Dashboard
