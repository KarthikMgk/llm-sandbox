import { useEffect, useRef } from 'react'
import { Terminal as XTerm } from '@xterm/xterm'
import '@xterm/xterm/css/xterm.css'

function Terminal({ sandboxId }) {
  const terminalRef = useRef(null)
  const xtermRef = useRef(null)

  useEffect(() => {
    if (!terminalRef.current || xtermRef.current) return

    const xterm = new XTerm({
      theme: { background: '#fff' },
      fontFamily: 'SF Mono, Monaco, Inconsolata, monospace'
    })
    xterm.open(terminalRef.current)
    xtermRef.current = xterm

    return () => {
      xterm.dispose()
    }
  }, [])

  return <div className="terminal" ref={terminalRef} />
}

export default Terminal