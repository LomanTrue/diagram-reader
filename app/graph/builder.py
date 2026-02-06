from app.graph.model import Node, Edge, DiagramGraph
import numpy as np

def point_inside_bbox(point, bbox):
    x, y = point
    x1, y1, x2, y2 = bbox
    return x1 <= x <= x2 and y1 <= y <= y2

def center_of_bbox(bbox):
    x1, y1, x2, y2 = bbox
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def euclidean_distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def find_connected_nodes(arrow_bbox, nodes):
    x1, y1, x2, y2 = arrow_bbox
    start_point = (x1, y1)
    end_point = (x2, y2)

    source = None
    target = None

    for node in nodes:
        if point_inside_bbox(start_point, node.bbox):
            source = node
        if point_inside_bbox(end_point, node.bbox):
            target = node

    if source is None:
        distances = [(node, euclidean_distance(start_point, center_of_bbox(node.bbox))) for node in nodes]
        source = min(distances, key=lambda x: x[1])[0]

    if target is None:
        distances = [(node, euclidean_distance(end_point, center_of_bbox(node.bbox))) for node in nodes]
        target = min(distances, key=lambda x: x[1])[0]

    return source, target

def build_graph(detections, text_bboxes):
    nodes = []
    edges = []

    for det in detections:
        if det["class"] == 2:
            nodes.append(Node(
                id=f"n{len(nodes)}",
                type=det["class"],
                text="",
                bbox=det["bbox"]
            ))

    for text_dict in text_bboxes:
        text_bbox = text_dict['bbox']
        text_value = text_dict['text']
        for node in nodes:
            if node.type == 2 and \
               point_inside_bbox((text_bbox[0], text_bbox[1]), node.bbox) and \
               point_inside_bbox((text_bbox[2], text_bbox[3]), node.bbox):
                node.text = text_value
                break

    for det in detections:
        if det["class"] == 0:  # стрелка
            source, target = find_connected_nodes(det["bbox"], nodes)
            if source and target:
                edges.append(Edge(source.id, target.id))

    graph = DiagramGraph(nodes, edges)

    first_node = find_first_node(graph)

    for i, edge in enumerate(edges):
        if edge.source == first_node.id or edge.target == first_node.id:
            if edge.target == first_node.id:
                edge.source, edge.target = edge.target, edge.source
            edges.insert(0, edges.pop(i))
            break

    return graph

def find_first_node(graph: DiagramGraph) -> Node:
    nodes_with_one_edge = []

    # считаем количество edges для каждой ноды
    edge_counts = {node.id: 0 for node in graph.nodes}
    for edge in graph.edges:
        edge_counts[edge.source] += 1
        edge_counts[edge.target] += 1

    for node in graph.nodes:
        if edge_counts[node.id] == 1:
            nodes_with_one_edge.append(node)

    if not nodes_with_one_edge:
        nodes_with_one_edge = graph.nodes

    nodes_with_one_edge.sort(key=lambda n: (n.bbox[1], n.bbox[0]))
    return nodes_with_one_edge[0]