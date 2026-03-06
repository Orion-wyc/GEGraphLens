#!/usr/bin/env python3
"""测试 protobuf 解析器功能"""

from proto_parser import parse_ge_dump_file

def test_parser():
    file_path = 'uploads/ge_proto_00000012_graph_0_Build.txt'
    
    print(f'开始解析文件: {file_path}')
    graph = parse_ge_dump_file(file_path)
    
    print(f'\n图名: {graph.name}')
    print(f'节点数: {len(graph.nodes)}')
    print(f'边数: {len(graph.edges)}')
    print(f'输入: {graph.inputs}')
    print(f'输出: {graph.outputs}')
    
    print('\n前5个节点:')
    for i, (name, node) in enumerate(list(graph.nodes.items())[:5]):
        print(f'  {i+1}. {name} ({node.type})')
        print(f'      输入: {node.inputs}')
        print(f'      输出目标: {node.dst_names}')
    
    print('\n前5条边:')
    for i, edge in enumerate(graph.edges[:5]):
        print(f'  {i+1}. {edge.source} -> {edge.target} ({edge.edge_type})')
    
    print('\n按类型统计节点:')
    node_types = {}
    for node in graph.nodes.values():
        if node.type not in node_types:
            node_types[node.type] = 0
        node_types[node.type] += 1
    
    for node_type, count in sorted(node_types.items(), key=lambda x: -x[1]):
        print(f'  {node_type}: {count}')
    
    print('\n解析完成!')

if __name__ == '__main__':
    test_parser()