from app.graph.model import Node, Edge, DiagramGraph

def build_graph(detections, texts):
    nodes = []
    edges = []

    for det, text in zip(detections, texts):
        if det["class"] != 0:
            nodes.append(Node(
                id=f"n{len(nodes)}",
                type=det["class"],
                text=text,
                bbox=det["bbox"]
            ))

    for det in detections:
        if det["class"] == 0:
            src, dst = find_connected_nodes(det, nodes)
            if src and dst:
                edges.append(Edge(src.id, dst.id))

    return DiagramGraph(nodes, edges)

def find_connected_nodes(arrow_det, nodes):
    ax1, ay1, ax2, ay2 = arrow_det["bbox"]
    arrow_center = ((ax1 + ax2) / 2, (ay1 + ay2) / 2)

    left_node = None
    right_node = None
    min_left_dist = float('inf')
    min_right_dist = float('inf')

    for node in nodes:
        nx1, ny1, nx2, ny2 = node.bbox
        node_center = ((nx1 + nx2) / 2, (ny1 + ny2) / 2)

        if node_center[0] < arrow_center[0]:
            dist = abs(arrow_center[0] - node_center[0])
            if dist < min_left_dist:
                min_left_dist = dist
                left_node = node
        else:
            dist = abs(arrow_center[0] - node_center[0])
            if dist < min_right_dist:
                min_right_dist = dist
                right_node = node

    return left_node, right_node
