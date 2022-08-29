from collections import Counter
from WeTest.util.algorithm import Node, upstream_round_robin


def test_upstream_round_robin():

    result = upstream_round_robin([Node(0, 20), Node(1, 30), Node(2, 50)], 100)
    assert Counter(result) == {2: 50, 1: 30, 0: 20}
