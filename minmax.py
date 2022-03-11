class Node:

    def __init__(self, value=-1, relations=[]):
        self.relations = relations
        self.value = value

def min_max_node(node, depth=4, maximise=True):
    pass

        

if __name__ == '__main__':
    node_aaa = Node(value=10)
    node_aab = Node(value=11)
    node_aba = Node(value=9)
    node_abb = Node(value=12)
    node_baa = Node(value=14)
    node_bab = Node(value=15)
    node_bba = Node(value=13)
    node_bbb = Node(value=14)
    node_aa = Node(relations=[node_aaa, node_aab])
    node_ab = Node(relations=[node_aba, node_abb])
    node_ba = Node(relations=[node_baa, node_bab])
    node_bb = Node(relations=[node_bba, node_bbb])
    node_a = Node(relations=[node_aa, node_ab])
    node_b = Node(relations=[node_ba, node_bb])
    master_node = Node(relations=[node_a, node_b])

    print(min_max_node(master_node))
    

