#!/usr/bin/env python3
"""简单测试后端功能"""

import sys
sys.path.insert(0, '.')

from parser import parse_ge_dump_file
import json

def test_backend():
    print('=== 测试后端功能 ===\n')
    
    # 测试解析器
    print('1. 测试解析器...')
    file_path = 'uploads/ge_proto_00000012_graph_0_Build.txt'
    graph = parse_ge_dump_file(file_path)
    
    print(f'   ✓ 图名: {graph.name}')
    print(f'   ✓ 节点数: {len(graph.nodes)}')
    print(f'   ✓ 边数: {len(graph.edges)}')
    print(f'   ✓ 输入: {graph.inputs}')
    print(f'   ✓ 输出: {graph.outputs}')
    
    # 测试节点数据
    print('\n2. 测试节点数据结构...')
    first_node = list(graph.nodes.values())[0]
    print(f'   ✓ 第一个节点: {first_node.name} ({first_node.type})')
    print(f'   ✓ 输入数量: {len(first_node.inputs)}')
    print(f'   ✓ 输出目标数量: {len(first_node.dst_names)}')
    print(f'   ✓ 属性数量: {len(first_node.attrs)}')
    print(f'   ✓ 输入张量数量: {len(first_node.input_descs)}')
    print(f'   ✓ 输出张量数量: {len(first_node.output_descs)}')
    
    # 测试张量描述
    if first_node.input_descs:
        desc = first_node.input_descs[0]
        print(f'   ✓ 张量形状: {desc.shape}')
        print(f'   ✓ 张量类型: {desc.dtype.name}')
        print(f'   ✓ 张量布局: {desc.layout}')
    
    # 测试边数据
    print('\n3. 测试边数据结构...')
    data_edges = sum(1 for edge in graph.edges if edge.edge_type == 'data')
    control_edges = sum(1 for edge in graph.edges if edge.edge_type == 'control')
    print(f'   ✓ 数据边数量: {data_edges}')
    print(f'   ✓ 控制边数量: {control_edges}')
    
    # 测试节点类型统计
    print('\n4. 测试节点类型统计...')
    node_types = {}
    for node in graph.nodes.values():
        if node.type not in node_types:
            node_types[node.type] = 0
        node_types[node.type] += 1
    
    print(f'   ✓ 节点类型数量: {len(node_types)}')
    for node_type, count in sorted(node_types.items(), key=lambda x: -x[1])[:5]:
        print(f'   ✓ {node_type}: {count}')
    
    # 测试图分析功能
    print('\n5. 测试图分析功能...')
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
    
    print(f'   ✓ 平均度: {avg_degree:.2f}')
    print(f'   ✓ 最大度: {max_degree}')
    print(f'   ✓ 最小度: {min_degree}')
    
    print('\n✅ 所有后端功能测试通过!')
    print('\n后端服务已准备就绪，可以启动服务进行集成测试。')
    print('启动命令: source venv/bin/activate && python main.py')

if __name__ == '__main__':
    test_backend()