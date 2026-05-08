function Timeline({ events }) {
  return (
    <div className="timeline">
      <h3>Timeline</h3>
      <div className="timeline-list">
        {events.map((event) => (
          <div key={event.id} className="timeline-item">
            <span className="timestamp">
              {new Date(event.timestamp).toLocaleTimeString()}
            </span>
            <span className="type">{event.type}</span>
            <span className="data">{JSON.stringify(event.data)}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Timeline
