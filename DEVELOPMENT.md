# GE Graph Lens 开发指南

## 开发环境设置

### 前置要求

- **Node.js**: 18.x 或更高版本
- **Python**: 3.9 或更高版本
- **Git**: 用于版本控制

### 后端开发环境

1. **创建虚拟环境**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动开发服务器**
```bash
python main.py
```

后端服务将在 http://localhost:8000 启动

4. **访问 API 文档**
- Swagger UI: http://localhost:8000/docs
- `ReDoc`: http://localhost:8000/redoc

### 前端开发环境

1. **安装依赖**
```bash
cd frontend
npm install
```

2. **启动开发服务器**
```bash
npm run dev
```

前端应用将在 http://localhost:5173 启动

3. **构建生产版本**
```bash
npm run build
```

4. **预览生产构建**
```bash
npm run preview
```

## 开发工作流

### 添加新功能

1. **后端开发**
   - 在 `main.py` 中添加新的 API 端点
   - 实现业务逻辑
   - 添加数据验证
   - 编写测试

2. **前端开发**
   - 在 `services/api.js` 中添加 API 调用函数
   - 创建或修改 React 组件
   - 更新状态管理（如需要）
   - 添加样式

3. **测试**
   - 测试 API 端点
   - 测试前端组件
   - 测试集成流程

### 调试技巧

#### 后端调试

1. **使用 print 语句**
```python
print(f"Debug info: {variable}")
```

2. **使用 logging 模块**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

3. **使用 FastAPI 的调试模式**
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
```

#### 前端调试

1. **使用 React DevTools**
   - 安装 React DevTools 浏览器扩展
   - 检查组件状态和 props

2. **使用 console.log**
```javascript
console.log('Debug info:', variable)
```

3. **使用浏览器开发者工具**
   - 检查网络请求
   - 查看控制台错误
   - 调试 JavaScript 代码

## 代码规范

### Python 代码规范

1. **遵循 PEP 8**
   - 使用 4 个空格缩进
   - 行长度不超过 79 字符
   - 使用有意义的变量名

2. **类型提示**
```python
from typing import Dict, List, Optional

def parse_graph(file_path: str) -> Dict[str, Any]:
    """解析图文件"""
    pass
```

3. **文档字符串**
```python
def upload_file(file: UploadFile) -> Dict[str, Any]:
    """
    上传文件到服务器
    
    Args:
        file: 上传的文件对象
        
    Returns:
        包含文件信息的字典
        
    Raises:
        HTTPException: 文件类型不支持时抛出
    """
    pass
```

### JavaScript/React 代码规范

1. **使用 ESLint**
```bash
npm run lint
```

2. **组件命名**
   - 使用 PascalCase 命名组件
   - 使用 camelCase 命名函数和变量

3. **使用函数组件**
```javascript
function MyComponent({ prop1, prop2 }) {
  return <div>{prop1}</div>
}
```

4. **使用 Hooks**
```javascript
import { useState, useEffect } from 'react'

function MyComponent() {
  const [state, setState] = useState(null)
  
  useEffect(() => {
    // 副作用
  }, [])
  
  return <div>{state}</div>
}
```

## API 开发

### 创建新 API 端点

1. **定义路由**
```python
@app.get("/api/endpoint")
async def get_endpoint(param: str):
    """获取端点数据"""
    return {"data": "value"}
```

2. **添加参数验证**
```python
from pydantic import BaseModel

class RequestModel(BaseModel):
    param1: str
    param2: int = 0

@app.post("/api/endpoint")
async def post_endpoint(request: RequestModel):
    """处理 POST 请求"""
    return {"result": "success"}
```

3. **错误处理**
```python
fromfastapi import HTTPException

@app.get("/api/endpoint/{id}")
async def get_endpoint(id: str):
    if not id:
        raise HTTPException(status_code=400, detail="ID is required")
    return {"id": id}
```

### 前端 API 调用

1. **添加 API 函数**
```javascript
export const getEndpoint = async (param) => {
  const response = await api.get(`/api/endpoint/${param}`)
  return response.data
}
```

2. **在组件中使用**
```javascript
import { getEndpoint } from '../services/api'

function MyComponent() {
  const [data, setData] = useState(null)
  
  useEffect(() => {
    const fetchData = async () => {
      const result = await getEndpoint('param')
      setData(result)
    }
    fetchData()
  }, [])
  
  return <div>{data}</div>
}
```

## 组件开发

### 创建新组件

1. **创建组件文件**
```javascript
// components/MyComponent.jsx
import { useState } from 'react'
import './MyComponent.css'

function MyComponent({ prop1, onAction }) {
  const [state, setState] = useState(null)
  
  const handleClick = () => {
    onAction(state)
  }
  
  return (
    <div className="my-component">
      <h2>{prop1}</h2>
      <button onClick={handleClick}>Action</button>
    </div>
  )
}

export default MyComponent
```

2. **添加样式**
```css
/* components/MyComponent.css */
.my-component {
  padding: 20px;
  border: 1px solid #ccc;
}

.my-component h2 {
  color: #333;
}
```

3. **使用组件**
```javascript
import MyComponent from './components/MyComponent'

function App() {
  const handleAction = (data) => {
    console.log('Action triggered:', data)
  }
  
  return (
    <MyComponent 
      prop1="Hello"
      onAction={handleAction}
    />
  )
}
```

## 状态管理

### 使用 Zustand Store

1. **更新 Store**
```javascript
// stores/useStore.js
const useStore = create((set) => ({
  // 现有状态
  currentFile: null,
  
  // 新增状态
  newField: null,
  
  // 新增操作
  setNewField: (value) => set({ newField: value }),
}))
```

2. **在组件中使用**
```javascript
import useStore from '../stores/useStore'

function MyComponent() {
  const { newField, setNewField } = useStore()
  
  return (
    <div>
      <input 
        value={newField || ''}
        onChange={(e) => setNewField(e.target.value)}
      />
    </div>
  )
}
```

## 测试

### 后端测试

1. **安装测试依赖**
```bash
pip install pytest pytest-asyncio httpx
```

2. **编写测试**
```python
# tests/test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

3. **运行测试**
```bash
pytest
```

### 前端测试

1. **安装测试依赖**
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

2. **编写测试**
```javascript
// tests/FileUpload.test.jsx
import { render, screen } from '@testing-library/react'
import FileUpload from '../src/components/FileUpload'

test('renders file upload component', () => {
  render(<FileUpload onFileUploaded={() => {}} />)
  expect(screen.getByText(/点击选择或拖拽文件到此处/)).toBeInTheDocument()
})
```

3. **运行测试**
```bash
npm test
```

## 性能优化

### 后端优化

1. **异步处理**
```python
import asyncio

async def process_large_file(file_path: str):
    """异步处理大文件"""
    # 异步操作
    pass
```

2. **缓存**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_data(key: str):
    """缓存数据"""
    pass
```

### 前端优化

1. **使用 React.memo**
```javascript
const MyComponent = React.memo(function MyComponent({ prop }) {
  return <div>{prop}</div>
})
```

2. **使用 useMemo 和 useCallback**
```javascript
import { useMemo, useCallback } from 'react'

function MyComponent({ items }) {
  const processedItems = useMemo(() => {
    return items.map(item => item.value * 2)
  }, [items])
  
  const handleClick = useCallback(() => {
    console.log('Clicked')
  }, [])
  
  return <div onClick={handleClick}>{processedItems.join(', ')}</div>
}
```

3. **代码分割**
```javascript
const GraphVisualizer = lazy(() => import('./components/GraphVisualizer'))

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <GraphVisualizer />
    </Suspense>
  )
}
```

## 部署

### 后端部署

1. **使用 Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

2. **使用 Docker**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
```

### 前端部署

1. **构建生产版本**
```bash
npm run build
```

2. **使用 Nginx 提供静态文件**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

## 故障排除

### 常见问题

1. **CORS 错误**
   - 检查后端 CORS 配置
   - 确保前端 URL 在允许的源列表中

2. **文件上传失败**
   - 检查文件大小限制
   - 检查文件类型验证
   - 检查 uploads 目录权限

3. **图渲染问题**
   - 检查 AntV G6 版本兼容性
   - 检查数据格式
   - 检查容器尺寸

## 贡献指南

1. **Fork 项目**
2. **创建功能分支**
3. **提交更改**
4. **推送到分支**
5. **创建 Pull Request**

## 资源链接

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [React 文档](https://react.dev/)
- [AntV G6 文档](https://g6.antv.antgroup.com/)
- [Vite 文档](https://vitejs.dev/)
- [Zustand 文档](https://zustand-demo.pmnd.rs/)