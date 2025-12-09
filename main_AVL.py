from AVLTree import AVLTree
# test_avl.py




# ---------- helpers ----------

def inorder_keys(node):
    if node is None:
        return []
    return inorder_keys(node.left) + [node.key] + inorder_keys(node.right)


def bst_insert_edges_from(start, key):
    """
    Number of EDGES from starting node to where a new node with 'key'
    would be inserted in a plain BST, BEFORE balancing.
    """
    if start is None:
        return 0  # empty tree → new root, 0 edges

    curr = start
    edges = 0
    while True:
        if key < curr.key:
            if curr.left is None:
                return edges + 1
            curr = curr.left
        else:
            if curr.right is None:
                return edges + 1
            curr = curr.right
        edges += 1


def finger_insert_expected_edges(tree, key):
    """
    Number of EDGES from max node (finger) to new node,
    simulating finger_insert BEFORE balancing.
    """
    start = tree.max_node()
    if start is None:
        return 0  # empty tree

    x = start
    edgesUp = 0
    edgesDown = 0

    # case 1: key > max → insert as right child of max
    if x.key < key:
        return 1

    # case 2: key <= max → climb up while x.key > key
    while x.key > key and x.parent is not None:
        x = x.parent
        edgesUp += 1

    # simulate searching_for_insert(x, key)
    curr = x
    while True:
        if key < curr.key:
            if curr.left is None:
                edgesDown += 1
                break
            curr = curr.left
        else:
            if curr.right is None:
                edgesDown += 1
                break
            curr = curr.right
        edgesDown += 1

    return edgesUp + edgesDown


def print_tree_info(tree, title):
    print(f"\n=== {title} ===")
    keys = inorder_keys(tree.root)
    root_key = tree.root.key if tree.root is not None else None
    print("in-order keys:", keys)
    print("root key:", root_key)
    height = tree.root.height if tree.root is not None else -1
    print("tree height:", height)


def print_test_header(name, func_name):
    print("\n==============================")
    print(name)
    print(f"Function tested: {func_name}")
    print("==============================")


# ---------- tests ----------

def test_insert_basic():
    print_test_header("Test 1: basic insert from root", "insert")

    t = AVLTree()

    # insert(10)
    start = t.root
    wanted_e = bst_insert_edges_from(start, 10)  # BEFORE balancing
    node, e, h = t.insert(10, "10")
    print("insert(10):")
    print(f"  wanted: node.key=10, edges={wanted_e}")
    print(f"  real  : node.key={node.key if node else None}, edges={e}, promotes={h}")

    # insert(5)
    start = t.root
    wanted_e = bst_insert_edges_from(start, 5)
    node, e, h = t.insert(5, "5")
    print("insert(5):")
    print(f"  wanted: node.key=5, edges={wanted_e}")
    print(f"  real  : node.key={node.key if node else None}, edges={e}, promotes={h}")

    # insert(15)
    start = t.root
    wanted_e = bst_insert_edges_from(start, 15)
    node, e, h = t.insert(15, "15")
    print("insert(15):")
    print(f"  wanted: node.key=15, edges={wanted_e}")
    print(f"  real  : node.key={node.key if node else None}, edges={e}, promotes={h}")

    print_tree_info(t, "After basic insert")


def test_insert_with_rotation():
    print_test_header("Test 2: insert causing rotation", "insert")

    t = AVLTree()

    # 10
    start = t.root
    w1 = bst_insert_edges_from(start, 10)
    n1, e1, h1 = t.insert(10, "10")
    print("insert(10):")
    print(f"  wanted: node.key=10, edges={w1}")
    print(f"  real  : node.key={n1.key if n1 else None}, edges={e1}, promotes={h1}")

    # 20
    start = t.root
    w2 = bst_insert_edges_from(start, 20)
    n2, e2, h2 = t.insert(20, "20")
    print("insert(20):")
    print(f"  wanted: node.key=20, edges={w2}")
    print(f"  real  : node.key={n2.key if n2 else None}, edges={e2}, promotes={h2}")

    # 30 – should cause rotation
    start = t.root
    w3 = bst_insert_edges_from(start, 30)
    n3, e3, h3 = t.insert(30, "30")
    print("insert(30):")
    print(f"  wanted: node.key=30, edges={w3}")
    print(f"  real  : node.key={n3.key if n3 else None}, edges={e3}, promotes={h3}")

    print_tree_info(t, "After rotation test inserts")


def test_search():
    print_test_header("Test 3: search from root", "search")

    t = AVLTree()
    for k in [10, 5, 15, 2, 7]:
        t.insert(k, str(k))

    # search(10)
    node, e = t.search(10)
    print("search(10):")
    print("  wanted: found=True, node.key=10, edges according to spec")
    print(f"  real  : found={node is not None}, node.key={node.key if node else None}, edges={e}")

    # search(7)
    node, e = t.search(7)
    print("search(7):")
    print("  wanted: found=True, node.key=7, edges for path root→5→7")
    print(f"  real  : found={node is not None}, node.key={node.key if node else None}, edges={e}")

    # search(100)
    node, e = t.search(100)
    print("search(100):")
    print("  wanted: found=False, node.key=None, edges=-1")
    print(f"  real  : found={node is not None}, node.key={node.key if node else None}, edges={e}")

    print_tree_info(t, "After search test")


def test_finger_insert():
    print_test_header("Test 4: finger_insert from max", "finger_insert")

    t = AVLTree()
    for k in [10, 5, 15]:
        t.insert(k, str(k))

    print_tree_info(t, "Before finger_insert")

    # finger_insert(20)
    wanted_e = finger_insert_expected_edges(t, 20)  # BEFORE balancing
    node, e, h = t.finger_insert(20, "20")
    print("finger_insert(20):")
    print(f"  wanted: node.key=20, edges={wanted_e}")
    print(f"  real  : node.key={node.key if node else None}, edges={e}, promotes={h}")

    # finger_insert(17)
    wanted_e = finger_insert_expected_edges(t, 17)
    node, e, h = t.finger_insert(17, "17")
    print("finger_insert(17):")
    print(f"  wanted: node.key=17, edges={wanted_e}")
    print(f"  real  : node.key={node.key if node else None}, edges={e}, promotes={h}")

    print_tree_info(t, "After finger_insert")


def test_finger_search():
    print_test_header("Test 5: finger_search from max", "finger_search")

    t = AVLTree()
    for k in [10, 5, 15, 2, 7, 12, 20]:
        t.insert(k, str(k))

    # finger_search(20)
    node, e = t.finger_search(20)
    print("finger_search(20):")
    print("  wanted: found=True, node.key=20, edges_from_max according to spec")
    print(f"  real  : found={node is not None}, node.key={node.key if node else None}, edges_from_max={e}")

    # finger_search(12)
    node, e = t.finger_search(12)
    print("finger_search(12):")
    print("  wanted: found=True, node.key=12, edges_from_max according to spec")
    print(f"  real  : found={node is not None}, node.key={node.key if node else None}, edges_from_max={e}")

    # finger_search(100)
    node, e = t.finger_search(100)
    print("finger_search(100):")
    print("  wanted: found=False, node.key=None, edges_from_max=-1")
    print(f"  real  : found={node is not None}, node.key={node.key if node else None}, edges_from_max={e}")

    print_tree_info(t, "After finger_search test")


def main():
    test_insert_basic()
    test_insert_with_rotation()
    test_search()
    test_finger_insert()
    test_finger_search()


main()