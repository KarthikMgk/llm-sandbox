function StatusBar({ sandbox }) {
  return (
    <div className="status-bar">
      <h3>Status</h3>
      <div className="status-item">
        <span>cpu</span>
        <span>--</span>
      </div>
      <div className="status-item">
        <span>mem</span>
        <span>--</span>
      </div>
      <div className="status-item">
        <span>net</span>
        <span>--</span>
      </div>
      <div className="status-item">
        <span>agent</span>
        <span>auth required</span>
      </div>
    </div>
  )
}

export default StatusBar