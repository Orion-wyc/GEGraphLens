# GE Graph Lens API 文档

## 基础信息

- **Base URL**: `http://localhost:8000`
- **API 版本**: `1.0.0`
- **内容类型**: `application/json`

## API 端点

### 1. 根路径

获取 API 基本信息。

**请求**
```
GET /
```

**响应**
```json
{
  "message": "GE Dump Graph Visualizer API",
  "version": "1.0.0"
}
```

---

### 2. 健康检查

检查 API 服务状态。

**请求**
```
GET /health
```

**响应**
```json
{
  "status": "healthy"
}
```

---

### 3. 上传文件

上传 GE Dump 文件到服务器。

**请求**
```
POST /api/upload
Content-Type: multipart/form-data
```

**参数**
- `file` (file, required): 上传的文件，仅支持 .txt 格式

**响应示例**
```json
{
  "filename": "graph_dump.txt",
  "size": 1024,
  "path": "uploads/graph_dump.txt",
  "message": "File uploaded successfully"
}
```

**错误响应**
```json
{
  "detail": "Only .txt files are supported"
}
```

**状态码**
- `200`: 上传成功
- `400`: 文件类型不支持

---

### 4. 解析文件

解析已上传的文件并生成图数据。

**请求**
```
POST /api/parse
Content-Type: application/json
```

**请求体**
```json
{
  "filename": "graph_dump.txt"
}
```

**响应示例**
```json
{
  "filename": "graph_dump.txt",
  "graph_id": "graph_001",
  "nodes_count": 100,
  "edges_count": 150,
  "message": "Parsing completed"
}
```

**错误响应**
```json
{
  "detail": "File not found"
}
```

**状态码**
- `200`: 解析成功
- `404`: 文件不存在

---

### 5. 获取图数据

获取指定图的节点和边数据。

**请求**
```
GET /api/graph/{graph_id}
```

**路径参数**
- `graph_id` (string, required): 图的唯一标识符

**响应示例**
```json
{
  "graph_id": "graph_001",
  "nodes": [
    {
      "id": "node_1",
      "label": "Node 1",
      "type": "operator",
      "properties": {
        "input_count": 2,
        "output_count": 1
      }
    },
    {
      "id": "node_2",
      "label": "Node 2",
      "type": "data",
      "properties": {
        "shape": [10, 20],
        "dtype": "float32"
      }
    }
  ],
  "edges": [
    {
      "id": "edge_1",
      "source": "node_1",
      "target": "node_2",
      "label": "output",
      "properties": {
        "tensor_name": "output_tensor"
      }
    }
  ],
  "message": "Graph data retrieved successfully"
}
```

**数据结构说明**

#### 节点对象
| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| id | string | 是 | 节点唯一标识符 |
| label | string | 是 | 节点显示名称 |
| type | string | 是 | 节点类型（operator, data, const 等） |
| properties | object | 否 | 节点属性字典 |

#### 边对象
| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| id | string | 是 | 边唯一标识符 |
| source | string | 是 | 源节点 ID |
| target | string | 是 | 目标节点 ID |
| label | string | 否 | 边显示标签 |
| properties | object | 否 | 边属性字典 |

---

### 6. 分析图

对图进行统计分析。

**请求**
```
GET /api/analyze/{graph_id}
```

**路径参数**
- `graph_id` (string, required): 图的唯一标识符

**响应示例**
```json
{
  "graph_id": "graph_001",
  "analysis": {
    "total_nodes": 100,
    "total_edges": 150,
    "avg_degree": 3.0,
    "connected_components": 1,
    "max_degree": 10,
    "min_degree": 1,
    "node_types": {
      "operator": 60,
      "data": 30,
      "const": 10
    },
    "subgraph_count": 5
  },
  "message": "Analysis completed"
}
```

**分析指标说明**

| 指标 | 类型 | 说明 |
|------|------|------|
| total_nodes | integer | 节点总数 |
| total_edges | integer | 边总数 |
| avg_degree | float | 平均度数 |
| connected_components | integer | 连通分量数 |
| max_degree | integer | 最大度数 |
| min_degree | integer | 最小度数 |
| node_types | object | 各类型节点数量统计 |
| subgraph_count | integer | 子图数量 |

---

## 错误响应格式

所有 API 端点在出错时返回统一的错误格式：

```json
{
  "detail": "错误描述信息"
}
```

**常见错误状态码**
- `400`: 请求参数错误
- `404`: 资源不存在
- `500`: 服务器内部错误

---

## 使用示例

### cURL 示例

#### 上传文件
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@graph_dump.txt"
```

#### 解析文件
```bash
curl -X POST "http://localhost:8000/api/parse" \
  -H "Content-Type: application/json" \
  -d '{"filename": "graph_dump.txt"}'
```

#### 获取图数据
```bash
curl -X GET "http://localhost:8000/api/graph/graph_001"
```

#### 分析图
```bash
curl -X GET "http://localhost:8000/api/analyze/graph_001"
```

### JavaScript/Axios 示例

```javascript
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

// 上传文件
const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await axios.post(`${API_BASE_URL}/api/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  
  return response.data
}

// 解析文件
const parseFile = async (filename) => {
  const response = await axios.post(`${API_BASE_URL}/api/parse`, { filename })
  return response.data
}

// 获取图数据
const getGraph = async (graphId) => {
  const response = await axios.get(`${API_BASE_URL}/api/graph/${graphId}`)
  return response.data
}

// 分析图
const analyzeGraph = async (graphId) => {
  const response = await axios.get(`${API_BASE_URL}/api/analyze/${graphId}`)
  return response.data
}
```

### Python/requests 示例

```python
import requests

API_BASE_URL = "http://localhost:8000"

# 上传文件
def upload_file(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{API_BASE_URL}/api/upload", files=files)
    return response.json()

# 解析文件
def parse_file(filename):
    response = requests.post(
        f"{API_BASE_URL}/api/parse",
        json={"filename": filename}
    )
    return response.json()

# 获取图数据
def get_graph(graph_id):
    response = requests.get(f"{API_BASE_URL}/api/graph/{graph_id}")
    return response.json()

# 分析图
def analyze_graph(graph_id):
    response = requests.get(f"{API_BASE_URL}/api/analyze/{graph_id}")
    return response.json()
```

---

## 性能考虑

### 文件大小限制
- 建议单文件大小不超过 100MB
- 大文件处理采用流式读取

### 超时设置
- 文件上传: 30 秒
- 文件解析: 60 秒
- 图数据获取: 10 秒

### 分页支持
对于大型图，建议实现分页获取节点和边的功能（待开发）

---

## 安全考虑

### CORS 配置
当前允许的源：
- `http://localhost:5173`
- `http://localhost:3000`

### 文件验证
- 仅允许 .txt 格式文件
- 文件名验证（防止路径遍历攻击）

### 输入验证
- 所有输入参数都经过验证
- 使用 Pydantic 进行数据验证

---

## 版本历史

### v1.0.0 (当前版本)
- 初始版本
- 支持文件上传和解析
- 支持图数据获取
- 支持图分析

---

## 未来计划

### 即将添加的功能
- [ ] 批量文件上传
- [ ] 图数据分页
- [ ] 图搜索和过滤
- [ ] 图导出（多种格式）
- [ ] WebSocket 实时更新
- [ ] 用户认证和授权
- [ ] API 速率限制
- [ ] 缓存机制