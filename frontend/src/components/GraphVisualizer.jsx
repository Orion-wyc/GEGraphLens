import { useEffect, useRef, useState } from 'react'
import { getGraph, analyzeGraph } from '../services/api'
import { Graph } from '@antv/g6'
import './GraphVisualizer.css'

function GraphVisualizer({ file, onGraphParsed }) {
  const containerRef = useRef(null)
  const graphRef = useRef(null)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedNode, setSelectedNode] = useState(null)
  const [graphData, setGraphData] = useState(null)

  useEffect(() => {
    initGraph()
    loadGraphData()
    loadAnalysis()

    return () => {
      if (graphRef.current) {
        graphRef.current.destroy()
      }
    }
  }, [file.graph_id])

  const initGraph = () => {
    if (!containerRef.current) return

    const width = containerRef.current.offsetWidth
    const height = 600

    graphRef.current = new Graph({
      container: containerRef.current,
      width,
      height,
      modes: {
        default: ['drag-canvas', 'zoom-canvas', 'drag-node', 'click-select'],
      },
      layout: {
        type: 'dagre',
        rankdir: 'LR',
        nodesep: 50,
        ranksep: 100,
      },
      defaultNode: {
        type: 'rect',
        size: [120, 50],
        style: {
          fill: '#e6f7ff',
          stroke: '#1890ff',
          lineWidth: 2,
          radius: 4,
        },
        labelCfg: {
          style: {
            fill: '#333',
            fontSize: 12,
            fontWeight: 'bold',
          },
          position: 'center',
        },
      },
      defaultEdge: {
        type: 'polyline',
        style: {
          stroke: '#a3b1bf',
          lineWidth: 2,
          endArrow: true,
          radius: 10,
        },
        labelCfg: {
          style: {
            fill: '#666',
            fontSize: 10,
          },
          position: 'center',
        },
      },
      nodeStateStyles: {
        selected: {
          fill: '#fff1b8',
          stroke: '#faad14',
          lineWidth: 3,
        },
        hover: {
          fill: '#d6f4ff',
          stroke: '#40a9ff',
          lineWidth: 3,
        },
      },
      edgeStateStyles: {
        selected: {
          stroke: '#faad14',
          lineWidth: 3,
        },
        hover: {
          stroke: '#40a9ff',
          lineWidth: 3,
        },
      },
    })

    graphRef.current.on('node:click', (evt) => {
      const { item } = evt
      const nodeData = item.getModel()
      setSelectedNode(nodeData)
    })

    graphRef.current.on('canvas:click', () => {
      setSelectedNode(null)
    })
  }

  const loadGraphData = async () => {
    try {
      const data = await getGraph(file.graph_id)
      
      const processedData = processGraphData(data)
      setGraphData(processedData)
      
      graphRef.current.data(processedData)
      graphRef.current.render()
      graphRef.current.fitView()
      
      onGraphParsed(data)
      setLoading(false)
    } catch (error) {
      console.error('加载图数据失败:', error)
      setLoading(false)
    }
  }

  const processGraphData = (data) => {
    const nodes = data.nodes.map(node => ({
      id: node.id,
      label: node.name,
      type: node.type,
      data: node,
      style: getNodeStyle(node.type),
    }))

    const edges = data.edges.map(edge => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      label: edge.label,
      data: edge,
      style: getEdgeStyle(edge.edge_type),
    }))

    return { nodes, edges }
  }

  const getNodeStyle = (type) => {
    const colorMap = {
      'Data': { fill: '#e6f7ff', stroke: '#1890ff' },
      'Const': { fill: '#f6ffed', stroke: '#52c41a' },
      'Conv': { fill: '#fff7e6', stroke: '#fa8c16' },
      'Cast': { fill: '#f9f0ff', stroke: '#722ed1' },
      'Relu': { fill: '#fff0f6', stroke: '#eb2f96' },
      'Pooling': { fill: '#fff1b8', stroke: '#faad14' },
      'BatchNorm': { fill: '#e6fffb', stroke: '#13c2c2' },
      'Concat': { fill: '#fff2e8', stroke: '#fa541c' },
      'Add': { fill: '#f0f5ff', stroke: '#2f54eb' },
      'Mul': { fill: '#fff0f6', stroke: '#c41d7f' },
    }

    const style = colorMap[type] || { fill: '#f5f5f5', stroke: '#8c8c8c' }
    return {
      fill: style.fill,
      stroke: style.stroke,
      lineWidth: 2,
      radius: 4,
    }
  }

  const getEdgeStyle = (edgeType) => {
    if (edgeType === 'control') {
      return {
        stroke: '#ff4d4f',
        lineWidth: 2,
        endArrow: true,
        lineDash: [5, 5],
      }
    }
    return {
      stroke: '#a3b1bf',
      lineWidth: 2,
      endArrow: true,
    }
  }

  const loadAnalysis = async () => {
    try {
      const data = await analyzeGraph(file.graph_id)
      setAnalysis(data.analysis)
    } catch (error) {
      console.error('加载分析数据失败:', error)
    }
  }

  const handleFitView = () => {
    if (graphRef.current) {
      graphRef.current.fitView()
    }
  }

  const handleZoomIn = () => {
    if (graphRef.current) {
      const zoom = graphRef.current.getZoom()
      graphRef.current.zoomTo(zoom * 1.2)
    }
  }

  const handleZoomOut = () => {
    if (graphRef.current) {
      const zoom = graphRef.current.getZoom()
      graphRef.current.zoomTo(zoom * 0.8)
    }
  }

  const renderNodeDetails = () => {
    if (!selectedNode) return null

    const node = selectedNode.data
    return (
      <div className="node-details-panel">
        <div className="panel-header">
          <h3>节点详情</h3>
          <button 
            className="close-button"
            onClick={() => setSelectedNode(null)}
          >
            ×
          </button>
        </div>
        
        <div className="node-info">
          <div className="info-section">
            <h4>基本信息</h4>
            <div className="info-row">
              <span className="info-label">名称:</span>
              <span className="info-value">{node.name}</span>
            </div>
            <div className="info-row">
              <span className="info-label">类型:</span>
              <span className="info-value">{node.type}</span>
            </div>
            <div className="info-row">
              <span className="info-label">ID:</span>
              <span className="info-value">{node.id}</span>
            </div>
          </div>

          {node.input_descs && node.input_descs.length > 0 && (
            <div className="info-section">
              <h4>输入张量</h4>
              {node.input_descs.map((desc, idx) => (
                <div key={idx} className="tensor-info">
                  <div className="info-row">
                    <span className="info-label">名称:</span>
                    <span className="info-value">{desc.name || `input_${idx}`}</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">数据类型:</span>
                    <span className="info-value">{desc.dtype}</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">形状:</span>
                    <span className="info-value">[{desc.shape.join(', ')}]</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">布局:</span>
                    <span className="info-value">{desc.layout}</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">大小:</span>
                    <span className="info-value">{desc.size} bytes</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">设备:</span>
                    <span className="info-value">{desc.device_type}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {node.output_descs && node.output_descs.length > 0 && (
            <div className="info-section">
              <h4>输出张量</h4>
              {node.output_descs.map((desc, idx) => (
                <div key={idx} className="tensor-info">
                  <div className="info-row">
                    <span className="info-label">名称:</span>
                    <span className="info-value">{desc.name || `output_${idx}`}</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">数据类型:</span>
                    <span className="info-value">{desc.dtype}</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">形状:</span>
                    <span className="info-value">[{desc.shape.join(', ')}]</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">布局:</span>
                    <span className="info-value">{desc.layout}</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">大小:</span>
                    <span className="info-value">{desc.size} bytes</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">设备:</span>
                    <span className="info-value">{desc.device_type}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {node.attrs && Object.keys(node.attrs).length > 0 && (
            <div className="info-section">
              <h4>属性</h4>
              {Object.entries(node.attrs).map(([key, value]) => (
                <div key={key} className="info-row">
                  <span className="info-label">{key}:</span>
                  <span className="info-value">
                    {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="graph-visualizer">
      <div className="graph-header">
        <h2>图可视化</h2>
        <div className="file-meta">
          <span>文件: {file.filename}</span>
          <span>大小: {(file.size / 1024).toFixed(2)} KB</span>
        </div>
        <div className="toolbar">
          <button onClick={handleFitView}>适应视图</button>
          <button onClick={handleZoomIn}>放大</button>
          <button onClick={handleZoomOut}>缩小</button>
        </div>
      </div>

      {analysis && (
        <div className="analysis-panel">
          <h3>图分析</h3>
          <div className="analysis-stats">
            <div className="stat-item">
              <span className="stat-label">节点数:</span>
              <span className="stat-value">{analysis.total_nodes}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">边数:</span>
              <span className="stat-value">{analysis.total_edges}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">数据边:</span>
              <span className="stat-value">{analysis.data_edges}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">控制边:</span>
              <span className="stat-value">{analysis.control_edges}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">平均度:</span>
              <span className="stat-value">{analysis.avg_degree.toFixed(2)}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">最大度:</span>
              <span className="stat-value">{analysis.max_degree}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">最小度:</span>
              <span className="stat-value">{analysis.min_degree}</span>
            </div>
          </div>
          
          {analysis.node_types && (
            <div className="node-types">
              <h4>节点类型统计</h4>
              {Object.entries(analysis.node_types).map(([type, count]) => (
                <div key={type} className="type-item">
                  <span className="type-name">{type}:</span>
                  <span className="type-count">{count}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <div className="graph-container" ref={containerRef}>
        {loading && <div className="loading">加载中...</div>}
      </div>

      {selectedNode && renderNodeDetails()}
    </div>
  )
}

export default GraphVisualizer