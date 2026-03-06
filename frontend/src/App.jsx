import { useState } from 'react'
import FileUpload from './components/FileUpload'
import GraphVisualizer from './components/GraphVisualizer'
import './App.css'

function App() {
  const [uploadedFile, setUploadedFile] = useState(null)
  const [graphData, setGraphData] = useState(null)

  const handleFileUploaded = (file) => {
    setUploadedFile(file)
  }

  const handleGraphParsed = (data) => {
    setGraphData(data)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>GE Dump Graph Visualizer</h1>
        <p>解析、可视化、分析GE Dump图</p>
      </header>
      
      <main className="app-main">
        {!uploadedFile ? (
          <FileUpload onFileUploaded={handleFileUploaded} />
        ) : (
          <GraphVisualizer 
            file={uploadedFile}
            onGraphParsed={handleGraphParsed}
          />
        )}
      </main>
    </div>
  )
}

export default App