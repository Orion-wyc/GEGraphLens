import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  
  return response.data
}

export const parseFile = async (filename) => {
  const response = await api.post('/api/parse', { filename })
  return response.data
}

export const getGraph = async (graphId) => {
  const response = await api.get(`/api/graph/${graphId}`)
  return response.data
}

export const analyzeGraph = async (graphId) => {
  const response = await api.get(`/api/analyze/${graphId}`)
  return response.data
}

export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}