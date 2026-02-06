def describe_algorithm(graph) -> str:
    if not graph.nodes:
        return ""

    node_map = {node.id: node for node in graph.nodes}
    edges = graph.edges

    visited_nodes = set()
    visited_edges = set()
    output_lines = []

    step_number = 1

    def walk_from(start_node_id):
        nonlocal step_number

        current_node_id = start_node_id

        while current_node_id and current_node_id not in visited_nodes:
            node = node_map.get(current_node_id)
            if not node:
                break

            text = node.text if node.text else f"Шаг {step_number}"
            output_lines.append(
                f"{step_number}. {text}"
            )

            visited_nodes.add(current_node_id)
            step_number += 1

            next_edge = None
            for edge in edges:
                edge_key = (edge.source, edge.target)
                if edge_key in visited_edges:
                    continue

                if edge.source == current_node_id or edge.target == current_node_id:
                    next_edge = edge
                    visited_edges.add(edge_key)
                    break

            if not next_edge:
                break

            current_node_id = (
                next_edge.target
                if next_edge.source == current_node_id
                else next_edge.source
            )

    if edges:
        walk_from(edges[0].source)

    for node in graph.nodes:
        if node.id not in visited_nodes:
            walk_from(node.id)

    return "\n".join(output_lines)
