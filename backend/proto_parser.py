"""
GE使用 Protobuf 解析 GE Dump 文件
"""
import ge_ir_pb2
from google.protobuf import text_format
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class Node:
    """图节点"""
    id: str
    name: str
    type: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    attrs: Dict[str, Any] = field(default_factory=dict)
    input_descs: List[Dict] = field(default_factory=list)
    output_descs: List[Dict] = field(default_factory=list)
    dst_names: List[str] = field(default_factory=list)
    dst_indices: List[int] = field(default_factory=list)


@dataclass
class Edge:
    """图边"""
    id: str
    source: str
    target: str
    source_port: int = 0
    target_port: int = 0
    edge_type: str = "data"
    label: str = ""


@dataclass
class Graph:
    """图结构"""
    name: str = ""
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)
    attrs: Dict[str, Any] = field(default_factory=dict)


class GEProtoParser:
    """GE Protobuf 解析器"""
    
    def __init__(self):
        self.graph = Graph()
    
    def parse_file(self, file_path: str) -> Graph:
        """使用 protobuf 解析 GE Dump 文件"""
        # 创建 ModelDef 对象
        model = ge_ir_pb2.ModelDef()
        
        # 使用 text_format 解析文本格式的 protobuf
        with open(file_path, 'r', encoding='utf-8') as f:
            text_format.Merge(f.read(), model)
        
        # 解析模型中的图
        if model.graph:
            self._parse_graph(model.graph[0])  # 通常第一个图是主图
        
        self._build_edges()
        return self.graph
    

    
    def _parse_graph(self, graph_def):
        """解析图定义"""
        self.graph.name = graph_def.name
        self.graph.inputs = list(graph_def.input)
        self.graph.outputs = list(graph_def.output)
        
        # 解析节点
        for op_def in graph_def.op:
            node = self._parse_op(op_def)
            self.graph.nodes[node.id] = node
        
        # 解析图属性
        self.graph.attrs = self._parse_attrs(graph_def.attr)
    
    def _parse_op(self, op_def) -> Node:
        """解析操作定义"""
        node = Node(
            id=op_def.name,
            name=op_def.name,
            type=op_def.type,
            inputs=list(op_def.input),
            dst_names=list(op_def.dst_name),
            dst_indices=list(op_def.dst_index)
        )
        
        # 解析属性
        node.attrs = self._parse_attrs(op_def.attr)
        
        # 解析输入张量描述
        for input_desc in op_def.input_desc:
            node.input_descs.append(self._parse_tensor_desc(input_desc))
        
        # 解析输出张量描述
        for output_desc in op_def.output_desc:
            node.output_descs.append(self._parse_tensor_desc(output_desc))
        
        return node
    
    def _parse_tensor_desc(self, tensor_desc) -> Dict:
        """解析张量描述"""
        desc = {
            "name": tensor_desc.name,
            "dtype": self._get_data_type_name(tensor_desc.dtype),
            "shape": list(tensor_desc.shape.dim),
            "layout": tensor_desc.layout,
            "size": tensor_desc.size,
            "device_type": tensor_desc.device_type,
            "attrs": self._parse_attrs(tensor_desc.attr)
        }
        return desc
    
    def _parse_attrs(self, attrs_map) -> Dict:
        """解析属性字典"""
        result = {}
        for key, attr_def in attrs_map.items():
            result[key] = self._parse_attr_value(attr_def)
        return result
    
    def _parse_attr_value(self, attr_def) -> Any:
        """解析属性值"""
        if attr_def.HasField('s'):
            return attr_def.s.decode('utf-8') if attr_def.s else ""
        elif attr_def.HasField('i'):
            return attr_def.i
        elif attr_def.HasField('f'):
            return attr_def.f
        elif attr_def.HasField('b'):
            return attr_def.b
        elif attr_def.HasField('bt'):
            return attr_def.bt.hex()
        elif attr_def.HasField('list'):
            return self._parse_list_value(attr_def.list)
        elif attr_def.HasField('dt'):
            return self._get_data_type_name(attr_def.dt)
        elif attr_def.HasField('func'):
            return self._parse_attrs(attr_def.func.attr)
        elif attr_def.HasField('td'):
            return self._parse_tensor_desc(attr_def.td)
        else:
            return str(attr_def)
    
    def _parse_list_value(self, list_value) -> List:
        """解析列表值"""
        result = []
        
        if list_value.s:
            result = [s.decode('utf-8') if s else "" for s in list_value.s]
        elif list_value.i:
            result = list(list_value.i)
        elif list_value.f:
            result = list(list_value.f)
        elif list_value.b:
            result = list(list_value.b)
        elif list_value.bt:
            result = [bt.hex() for bt in list_value.bt]
        elif list_value.dt:
            result = [self._get_data_type_name(dt) for dt in list_value.dt]
        
        return result
    
    def _get_data_type_name(self, dtype_value) -> str:
        """获取数据类型名称"""
        dtype_names = {
            0: 'DT_UNDEFINED',
            1: 'DT_FLOAT',
            2: 'DT_FLOAT16',
            3: 'DT_INT8',
            4: 'DT_UINT8',
            5: 'DT_INT16',
            6: 'DT_UINT16',
            7: 'DT_INT32',
            8: 'DT_INT64',
            9: 'DT_UINT32',
            10: 'DT_UINT64',
            11: 'DT_BOOL',
            12: 'DT_DOUBLE',
            13: 'DT_STRING',
        }
        return dtype_names.get(dtype_value, f'DT_UNKNOWN_{dtype_value}')
    
    def _build_edges(self):
        """构建边关系"""
        edge_id = 0
        
        for node_name, node in self.graph.nodes.items():
            # 处理输入边（数据边）
            for input_str in node.inputs:
                if not input_str:
                    continue
                
                # 解析输入字符串，格式为 "op_name:output_index"
                if ':' in input_str:
                    source_name, output_idx = input_str.rsplit(':', 1)
                    source_port = int(output_idx)
                else:
                    source_name = input_str
                    source_port = 0
                
                # 创建数据边
                edge = Edge(
                    id=f"edge_{edge_id}",
                    source=source_name,
                    target=node_name,
                    source_port=source_port,
                    target_port=0,
                    edge_type="data",
                    label=f"{source_port}"
                )
                self.graph.edges.append(edge)
                edge_id += 1
            
            # 处理输出边（包括控制边）
            for i, dst_name in enumerate(node.dst_names):
                if i < len(node.dst_indices):
                    dst_index = node.dst_indices[i]
                    
                    # dst_index 为 -1 表示控制边
                    if dst_index == -1:
                        edge_type = "control"
                        label = "control"
                    else:
                        edge_type = "data"
                        label = str(dst_index)
                    
                    edge = Edge(
                        id=f"edge_{edge_id}",
                        source=node_name,
                        target=dst_name,
                        source_port=0,
                        target_port=dst_index if dst_index != -1 else 0,
                        edge_type=edge_type,
                        label=label
                    )
                    self.graph.edges.append(edge)
                    edge_id += 1


def parse_ge_dump_file(file_path: str) -> Graph:
    """使用 protobuf 解析 GE Dump 文件的便捷函数"""
    parser = GEProtoParser()
    return parser.parse_file(file_path)