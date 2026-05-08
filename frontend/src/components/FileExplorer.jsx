import { useState, useEffect } from 'react'
import axios from 'axios'

function FileExplorer({ sandboxId }) {
  const [files, setFiles] = useState([])

  useEffect(() => {
    const fetchFiles = async () => {
      if (!sandboxId) return
      try {
        const response = await axios.get('/api/filesystem/list', {
          params: { sandbox_id: sandboxId }
        })
        setFiles(response.data)
      } catch (error) {
        // Files not available
      }
    }
    fetchFiles()
  }, [sandboxId])

  return (
    <div className="file-explorer">
      <h3>Files</h3>
      <div className="file-tree">
        <div className="file-item">/</div>
        {files.map((file) => (
          <div key={file} className="file-item">{file}</div>
        ))}
      </div>
    </div>
  )
}

export default FileExplorer
