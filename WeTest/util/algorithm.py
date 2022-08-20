from typing import List
from dataclasses import dataclass


@dataclass
class Node:

    index: int
    weight: int
    current: int = 0


def upstream_round_robin(Nodes: List[Node], counts: int) -> list:
    """Nginx smooth weighted round-robin balancing"""

    target = []
    best = Nodes[0]

    for _ in range(counts):
        total = 0

        for node in Nodes:
            total += node.weight
            node.current += node.weight
            if node.current > best.current:
                best = node
        best.current -= total
        target.append(best.index)

    return target
