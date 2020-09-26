from typing import Dict, List

from Core.LevelGenerator.leaf import Leaf


def get_leaf_connections(leaf: Leaf):
    leafs: List[Leaf] = []
    for connection_id in leaf.connections:
        leafs.append(leaf.connections[connection_id][0])
    return leafs


def populate_subgraph(all_leafs: List[Leaf]):
    node_to_graph: Dict[int, int] = dict()

    graph_id = 0
    for leaf in all_leafs:
        if leaf.id is None:
            raise Exception("Called with missing node IDs")

        if leaf.room is None:
            continue

        if leaf.id in node_to_graph:
            continue

        node_to_graph[leaf.id] = graph_id
        connections_to_follow = get_leaf_connections(leaf)

        while len(connections_to_follow) > 0:
            connection = connections_to_follow.pop()
            # Skip already seen IDs
            if connection.id in node_to_graph:
                continue

            node_to_graph[connection.id] = graph_id
            new_connections = get_leaf_connections(connection)

            for new_connection in new_connections:
                if new_connection.id not in node_to_graph:
                    connections_to_follow.append(new_connection)

        graph_id = graph_id + 1

    return node_to_graph

