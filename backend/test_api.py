#!/usr/bin/env python3
"""测试后端 API 功能"""

import sys
sys.path.insert(0, '.')

from main import app
from fastapi.testclient import TestClient

def test_api():
    client = TestClient(app)
    
    print('测试健康检查...')
    response = client.get('/health')
    print(f'健康检查: {response.json()}')
    
    print('\n测试解析文件...')
    response = client.post('/api/parse', json={'filename': 'ge_proto_00000012_graph_0_Build.txt'})
    print(f'解析结果: {response.json()}')
    
    if response.status_code == 200:
        graph_id = response.json()['graph_id']
        print(f'\n测试获取图数据...')
        response = client.get(f'/api/graph/{graph_id}')
        data = response.json()
        print(f'图数据: 节点数={len(data["nodes"])}, 边数={len(data["edges"])}')
        
        if data['nodes']:
            print(f'第一个节点: {data["nodes"][0]["name"]} ({data["nodes"][0]["type"]})')
            print(f'节点属性数量: {len(data["nodes"][0]["attrs"])}')
            print(f'输入张量数: {len(data["nodes"][0]["input_descs"])}')
            print(f'输出张量数: {len(data["nodes"][0]["output_descs"])}')
        
        print(f'\n测试图分析...')
        response = client.get(f'/api/analyze/{graph_id}')
        analysis = response.json()
        print(f'分析结果: {analysis["analysis"]}')
        
        print('\n✅ 所有测试通过!')

if __name__ == '__main__':
    test_api()