# GE Dump Graph Visualizer

基于 FastAPI + React 的 GE Dump 图解析、可视化和分析工具。

## 技术栈

### 后端
- **FastAPI** - 高性能异步 Web 框架
- **Uvicorn** - ASGI 服务器
- **Protobuf** - Google Protocol Buffers 解析
- **Pydantic** - 数据验证

### 前端
- **React 18** - UI 框架
- **Vite** - 构建工具
- **AntV G6** - 图可视化库
- **Axios** - HTTP 客户端
- **Zustand** - 状态管理

## 项目结构

```
ge_graph_lens/
├── backend/                 # 后端服务
│   ├── main.py             # FastAPI 主应用
│   ├── requirements.txt    # Python 依赖
│   └── uploads/            # 上传文件存储
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # React 组件
│   │   ├── services/       # API 服务
│   │   ├── stores/         # 状态管理
│   │   └── utils/          # 工具函数
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 快速开始

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

后端服务将在 http://localhost:8000 启动

API API 文档: http://localhost:8000/docs

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 http://localhost:5173 启动

## API 接口

### 健康检查
```
GET /health
```

### 上传文件
```
POST /api/upload
Content-Type: multipart/form-data
```

### 解析文件
```
POST /api/parse
Body: { "filename": "string" }
```

### 获取图数据
```
GET /api/graph/{graph_id}
```

### 分析图
```
GET /api/analyze/{graph_id}
```

## 功能特性

- ✅ 文件上传和解析
- ✅ 图可视化（AntV G6）
- ✅ 图分析（节点统计、连通性等）
- ✅ 响应式设计
- ✅ 异步处理大文件

## 开发计划

- [ ] 实现 protobuf 解析器
- [ ] 流式处理大文件
- [ ] 更多图分析算法
- [ ] 节点详情查看
- [ ] 图布局优化
- [ ] 导出功能

## 许可证

MIT