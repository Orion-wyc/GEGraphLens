import { useState } from 'react'
import { uploadFile, parseFile } from '../services/api'
import './FileUpload.css'

function FileUpload({ onFileUploaded }) {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile && !selectedFile.name.endsWith('.txt')) {
      setError('请上传.txt格式的文件')
      setFile(null)
      return
    }
    setFile(selectedFile)
    setError(null)
  }

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    setError(null)

    try {
      const uploadResult = await uploadFile(file)
      const parseResult = await parseFile(uploadResult.filename)
      
      onFileUploaded({
        ...uploadResult,
        ...parseResult
      })
    } catch (err) {
      setError(err.message || '上传失败')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="file-upload">
      <div className="upload-area">
        <input
          type="file"
          id="file-input"
          accept=".txt"
          onChange={handleFileChange}
          className="file-input"
        />
        <label htmlFor="file-input" className="file-label">
          <div className="upload-icon">📁</div>
          <p>点击选择或拖拽文件到此处</p>
          <p className="upload-hint">支持.txt格式的GE Dump文件</p>
        </label>
      </div>

      {file && (
        <div className="file-info">
          <p><strong>文件名:</strong> {file.name}</p>
          <p><strong>大小:</strong> {(file.size / 1024).toFixed(2)} KB</p>
          <button
            onClick={handleUpload}
            disabled={uploading}
            className="upload-button"
          >
            {uploading ? '上传中...' : '开始解析'}
          </button>
        </div>
      )}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
    </div>
  )
}

export default FileUpload