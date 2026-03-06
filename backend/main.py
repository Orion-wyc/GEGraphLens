from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import os
import sys

# 设置 protobuf 使用纯 Python 实现
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

from proto_parser import parse_ge_dump_file


class ParseRequest(BaseModel):
    filename: str

app = FastAPI(
    title="GE Dump Graph Visualizer API",
    description="API for parsing, visualizing, and analyzing GE Dump graphs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph_store = {}

@app.get("/")
async def root():
    return {"message": "GE Dump Graph Visualizer API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/upload")
async def upload_dump_file(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")
    
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, file.filename)
    content = await file.read()
    
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    return {
        "filename": file.filename,
        "size": len(content),
        "path": file_path,
        "message": "File uploaded successfully"
    }

@app.post("/api/parse")
async def parse_dump_file(request: ParseRequest):
    file_path = os.path.join("uploads", request.filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        graph = parse_ge_dump_file(file_path)
        graph_id = f"graph_{request.filename}"
        
        graph_store[graph_id] = graph
        
        return {
            "filename": request.filename,
            "graph_id": graph_id,
            "nodes_count": len(graph.nodes),
            "edges_count": len(graph.edges),
            "message": "Parsing completed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")

@app.get("/api/graph/{graph_id}")
async def get_graph(graph_id: str):
    if graph_id not in graph_store:
        raise HTTPException(status_code=404, detail="Graph not found")
    
    graph = graph_store[graph_id]
    
    nodes = []
    for node_id, node in graph.nodes.items():
        node_data = {
            "id": node.id,
            "label": node.name,
            "type": node.type,
            "inputs": node.inputs,
            "outputs": node.outputs,
            "attrs": node.attrs,
            "input_descs": node.input_descs,
            "output_descs": node.output_descs
        }
        nodes.append(node_data)
    
    edges = []
    for edge in graph.edges:
        edge_data = {
            "id": edge.id,
            "source": edge.source,
            "target": edge.target,
            "source_port": edge.source_port,
            "target_port": edge.target_port,
            "edge_type": edge.edge_type,
            "label": edge.label
        }
        edges.append(edge_data)
    
    return {
        "graph_id": graph_id,
        "name": graph.name,
        "inputs": graph.inputs,
        "outputs": graph.outputs,
        "nodes": nodes,
        "edges": edges,
        "message": "Graph data retrieved successfully"
    }

@app.get("/api/analyze/{graph_id}")
async def analyze_graph(graph_id: str):
    if graph_id not in graph_store:
        raise HTTPException(status_code=404, detail="Graph not found")
    
    graph = graph_store[graph_id]
    
    total_nodes = len(graph.nodes)
    total_edges = len(graph.edges)
    
    node_degrees = {}
    for edge in graph.edges:
        if edge.source not in node_degrees:
            node_degrees[edge.source] = 0
        node_degrees[edge.source] += 1
        
        if edge.target not in node_degrees:
            node_degrees[edge.target] = 0
        node_degrees[edge.target] += 1
    
    avg_degree = sum(node_degrees.values()) / len(node_degrees) if node_degrees else 0
    max_degree = max(node_degrees.values()) if node_degrees else 0
    min_degree = min(node_degrees.values()) if node_degrees else 0
    
    node_types = {}
    for node in graph.nodes.values():
        if node.type not in node_types:
            node_types[node.type] = 0
        node_types[node.type] += 1
    
    data_edges = sum(1 for edge in graph.edges if edge.edge_type == "data")
    control_edges = sum(1 for edge in graph.edges if edge.edge_type == "control")
    
    return {
        "graph_id": graph_id,
        "analysis": {
            "total_nodes": total_nodes,
            "total_edges": total_edges,
            "avg_degree": avg_degree,
            "max_degree": max_degree,
            "min_degree": min_degree,
            "data_edges": data_edges,
            "control_edges": control_edges,
            "node_types": node_types,
            "connected_components": 1
        },
        "message": "Analysis completed successfully"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)