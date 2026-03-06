# GE Graph Lens 项目架构

## 项目概述

GE Graph Lens 是一个前后端分离的 Web 应用，用于解析、可视化和分析 GE Dump 图结构。该项目基于 FastAPI（后端）和 React（前端）构建，使用 Protocol Buffers 解析图数据，并通过 AntV G6 进行可视化展示。

## 技术架构

### 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                        用户界面                            │
│                    (React + AntV G6)                     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                        API 层                             │
│                      (Axios HTTP)                         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                      后端服务                             │
│                     (FastAPI)                             │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    数据处理层                              │
│              (Protobuf 解析 + 图分析)                     │
└─────────────────────────────────────────────────────────┘
```

### 后端架构

```
backend/
├── main.py                 # FastAPI 主应用
│   ├── 路由定义
│   ├── CORS 中间件
│   └── API 端点
├── requirements.txt        # Python 依赖
└── uploads/               # 上传文件存储目录
```

**后端技术栈：**
- **FastAPI**: 高性能异步 Web 框架
- **Uvicorn**: ASGI 服务器
- **Protobuf**: Google Protocol Buffers 解析
- **Pydantic**: 数据验证

**主要 API 端点：：**
- `GET /`: API 信息
- `GET /health`: 健康检查
- `POST /api/upload`: 上传文件
- `POST /api/parse`: 解析文件
- `GET /api/graph/{graph_id}`: 获取图数据
- `GET /api/analyze/{graph_id}`: 分析图

### 前端架构

```
frontend/
├── src/
│   ├── App.jsx             # 主应用组件
│   ├── main.jsx            # 应用入口
│   ├── components/         # React 组件
│   │   ├── FileUpload.jsx  # 文件上传组件
│   │   └── GraphVisualizer.jsx  # 图可视化组件
│   ├── services/           # API 服务
│   │   └── api.js         # API 调用封装
│   ├── stores/             # 状态管理
│   │   └── useStore.js    # Zustand 状态存储
│   └── utils/              # 工具函数
├── package.json            # Node.js 依赖
└── vite.config.js          # Vite 配置
```

**前端技术栈：**
- **React 18**: UI 框架
- **Vite**: 构建工具
- **AntV G6**: 图可视化库
- **Axios**: HTTP 客户端
- **Zustand**: 状态管理

## 数据流

### 文件上传和解析流程

```
用户选择文件
    │
    ▼
FileUpload 组件
    │
    ├─► uploadFile() ──► POST /api/upload
    │                         │
    │                         ▼
    │                     保存文件到 uploads/
    │                         │
    │                         ▼
    │                     返回文件信息
    │
    ├─► parseFile() ──► POST /api/parse
    │                        │
    │                        ▼
    │                    解析 protobuf 文件
    │                        │
    │                        ▼
    │                    返回 graph_id
    │
    ▼
切换到 GraphVisualizer 组件
    │
    ├─► getGraph() ──► GET /api/graph/{graph_id}
    │                      │
    │                      ▼
    │                  返回图数据（节点和边）
    │
    ├─► analyzeGraph() ──► GET /api/analyze/{graph_id}
    │                          │
    │                          ▼
    │                      返回分析结果
    │
    ▼
使用 AntV G6 渲染图
```

## 状态管理

### Zustand Store 结构

```javascript
{
  currentFile: null,      // 当前上传的文件信息
  graphData: null,        // 图数据（节点和边）
  analysis: null,         // 图分析结果
  loading: false,         // 加载状态
  error: null            // 错误信息
}
```

## 图数据结构表示

### 节点数据结构

```json
{
  "id": "node_id",
  "label": "节点名称",
  "type": "节点类型",
  "properties": {
    "key": "value"
  }
}
```

### 边数据结构

```json
{
  "id": "edge_id",
  "source": "source_node_id",
  "target": "target_node_id",
  "label": "边标签",
  "properties": {
    "key": "value"
  }
}
```

### 图分析结果结构

```json
{
  "total_nodes": 100,
  "total_edges": 150,
  "avg_degree": 3.0,
  "connected_components": 1,
  "max_degree": 10,
  "min_degree": 1
}
```

## 部署架构

### 开发环境

```
┌─────────────────────┐
│  前端开发服务器      │
│  (Vite: 5173)       │
└─────────────────────┘
          │
          │ CORS
          ▼
┌─────────────────────┐
│  后端开发服务器      │
│  (Uvicorn: 8000)    │
└─────────────────────┘
```

### 生产环境

```
┌─────────────────────┐
│  Nginx 反向代理     │
│  (静态文件服务)      │
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│  后端应用服务器      │
│  (Gunicorn/Uvicorn) │
└─────────────────────┘
```

## 安全考虑

1. **文件上传验证**：
   - 文件类型限制（仅支持 .txt）
   - 文件大小限制
   - 文件名验证

2. **CORS 配置**：
   - 仅允许特定源访问
   - 配置允许的 HTTP 方法和头

3. **API 安全**：
   - 输入验证
   - 错误处理
   - 速率限制（待实现）

## 性能优化

1. **前端优化**：
   - React 组件懒加载
   - 图数据分块加载
   - 虚拟滚动（大列表）

2. **后端优化**：
   - 异步处理
   - 文件流式处理
   - 缓存机制

3. **图渲染优化**：
   - 使用 AntV G6 的布局优化
   - 节点和边的样式优化
   - 交互性能优化

## 扩展性设计

1. **插件化架构**：
   - 支持自定义图布局算法
   - 支持自定义节点和边样式
   - 支持自定义分析算法

2. **多格式支持**：
   - 扩展支持多种图数据格式
   - 支持多种可视化方式

3. **API 扩展**：
   - RESTful API 设计
   - 支持批量操作
   - 支持过滤和搜索

## 监控和日志

1. **前端监控**：
   - 错误日志
   - 性能监控
   - 用户行为追踪

2. **后端监控**：
   - API 请求日志
   - 性能指标
   - 错误追踪

## 测试策略

1. **单元测试**：
   - 组件测试
   - 工具函数测试
   - API 函数测试

2. **集成测试**：
   - API 端点测试
   - 文件上传和解析流程测试

3. **端到端测试**：
   - 用户流程测试
   - 跨浏览器测试