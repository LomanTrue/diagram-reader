def describe_algorithm(graph):
    lines = []

    for node in graph.nodes:
        lines.append(str(node))

    lines.append("Конец алгоритма.")
    return "\n".join(lines)
