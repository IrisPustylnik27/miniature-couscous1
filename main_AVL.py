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

# ---------- more helpers (for split/join) ----------

def collect_node_ids(node):
    if node is None:
        return set()
    return {id(node)} | collect_node_ids(node.left) | collect_node_ids(node.right)

def is_bst(node, lo=float("-inf"), hi=float("inf")):
    if node is None:
        return True
    if not (lo < node.key < hi):
        return False
    return is_bst(node.left, lo, node.key) and is_bst(node.right, node.key, hi)

def parents_ok(node, parent=None):
    if node is None:
        return True
    if node.parent is not parent:
        return False
    return parents_ok(node.left, node) and parents_ok(node.right, node)

def avl_ok_and_height(node):
    """
    Checks:
      1) balance factor <= 1 everywhere
      2) stored node.height matches computed height
    Returns: (ok, computed_height)
    """
    if node is None:
        return True, -1
    okL, hL = avl_ok_and_height(node.left)
    okR, hR = avl_ok_and_height(node.right)
    h = 1 + max(hL, hR)
    bf_ok = abs(hL - hR) <= 1
    height_ok = (node.height == h)
    return (okL and okR and bf_ok and height_ok), h

def print_check(label, ok):
    print(f"  {label}: {'PASS' if ok else 'FAIL'}")

def keys_all_less_than(keys, x):
    return all(k < x for k in keys)

def keys_all_greater_than(keys, x):
    return all(k > x for k in keys)


# ---------- split/join tests ----------

def test_split_root():
    print_test_header("Test 6: split on root", "split")

    t = AVLTree()
    for k in [10, 5, 15, 2, 7, 12, 20]:
        t.insert(k, str(k))

    print_tree_info(t, "Before split(root)")

    root = t.root
    split_key = root.key
    left, right = t.split(root)

    left_keys = inorder_keys(left.root)
    right_keys = inorder_keys(right.root)

    print("split(root):")
    print("  split_key:", split_key)
    print("  left inorder:", left_keys)
    print("  right inorder:", right_keys)

    # expected: all left < split_key, all right > split_key
    print_check("left keys < split_key", keys_all_less_than(left_keys, split_key))
    print_check("right keys > split_key", keys_all_greater_than(right_keys, split_key))

    # AVL + BST + parents
    print_check("left is BST", is_bst(left.root))
    print_check("right is BST", is_bst(right.root))

    okL, _ = avl_ok_and_height(left.root)
    okR, _ = avl_ok_and_height(right.root)
    print_check("left is AVL (balance+heights)", okL)
    print_check("right is AVL (balance+heights)", okR)

    print_check("left parent pointers ok", parents_ok(left.root, None))
    print_check("right parent pointers ok", parents_ok(right.root, None))

    # no shared nodes
    idsL = collect_node_ids(left.root)
    idsR = collect_node_ids(right.root)
    print_check("no shared nodes between left/right", idsL.isdisjoint(idsR))

    # "tree and x are not usable"
    print_check("original tree invalidated (root is None)", t.root is None)
    print_check("original tree size == 0", getattr(t, "size", None) == 0)
    print_check("split node detached (parent/left/right None)",
                root.parent is None and root.left is None and root.right is None)

    print_tree_info(left, "Left tree after split(root)")
    print_tree_info(right, "Right tree after split(root)")


def test_split_leaf():
    print_test_header("Test 7: split on a leaf", "split")

    t = AVLTree()
    for k in [10, 5, 15, 2, 7, 12, 20]:
        t.insert(k, str(k))

    leaf_key = 2
    leaf, _ = t.search(leaf_key)
    print_tree_info(t, f"Before split(leaf={leaf_key})")

    left, right = t.split(leaf)

    left_keys = inorder_keys(left.root)
    right_keys = inorder_keys(right.root)

    print("split(leaf):")
    print("  leaf_key:", leaf_key)
    print("  left inorder:", left_keys)
    print("  right inorder:", right_keys)

    print_check("left keys < leaf_key", keys_all_less_than(left_keys, leaf_key))
    print_check("right keys > leaf_key", keys_all_greater_than(right_keys, leaf_key))

    print_check("left is BST", is_bst(left.root))
    print_check("right is BST", is_bst(right.root))

    okL, _ = avl_ok_and_height(left.root)
    okR, _ = avl_ok_and_height(right.root)
    print_check("left is AVL (balance+heights)", okL)
    print_check("right is AVL (balance+heights)", okR)

    idsL = collect_node_ids(left.root)
    idsR = collect_node_ids(right.root)
    print_check("no shared nodes between left/right", idsL.isdisjoint(idsR))

    print_check("original tree invalidated (root is None)", t.root is None)
    print_check("leaf node detached (parent/left/right None)",
                leaf.parent is None and leaf.left is None and leaf.right is None)


def test_split_min_max():
    print_test_header("Test 8: split on min and max", "split")

    keys = [10, 5, 15, 2, 7, 12, 20]
    min_k = min(keys)
    max_k = max(keys)

    # split on min
    t1 = AVLTree()
    for k in keys:
        t1.insert(k, str(k))
    node_min, _ = t1.search(min_k)
    left1, right1 = t1.split(node_min)

    left1_keys = inorder_keys(left1.root)
    right1_keys = inorder_keys(right1.root)
    print("split(min):")
    print("  min_k:", min_k)
    print("  left inorder:", left1_keys)
    print("  right inorder:", right1_keys)
    print_check("left is empty", left1.root is None)
    print_check("right keys > min_k", keys_all_greater_than(right1_keys, min_k))

    # split on max
    t2 = AVLTree()
    for k in keys:
        t2.insert(k, str(k))
    node_max, _ = t2.search(max_k)
    left2, right2 = t2.split(node_max)

    left2_keys = inorder_keys(left2.root)
    right2_keys = inorder_keys(right2.root)
    print("split(max):")
    print("  max_k:", max_k)
    print("  left inorder:", left2_keys)
    print("  right inorder:", right2_keys)
    print_check("right is empty", right2.root is None)
    print_check("left keys < max_k", keys_all_less_than(left2_keys, max_k))


def test_join_basic():
    print_test_header("Test 9: join basic (ordered trees)", "join")

    left = AVLTree()
    right = AVLTree()

    left_keys = [1, 2, 3, 4, 5, 6, 7]
    right_keys = [9, 10, 11, 12, 13, 14, 15]
    mid = 8

    for k in left_keys:
        left.insert(k, str(k))
    for k in right_keys:
        right.insert(k, str(k))

    print_tree_info(left, "Left before join")
    print_tree_info(right, "Right before join")

    left.join(right, mid, str(mid))

    got = inorder_keys(left.root)
    expected = sorted(left_keys + [mid] + right_keys)

    print("join(left, right, 8):")
    print("  expected inorder:", expected)
    print("  real inorder    :", got)
    print_check("inorder matches expected", got == expected)

    print_check("is BST", is_bst(left.root))
    ok, _ = avl_ok_and_height(left.root)
    print_check("is AVL (balance+heights)", ok)
    print_check("parent pointers ok", parents_ok(left.root, None))


def test_join_with_empty_side():
    print_test_header("Test 10: join when one side is empty", "join")

    # case A: self empty
    a = AVLTree()
    b = AVLTree()
    for k in [10, 12, 15]:
        b.insert(k, str(k))
    a.join(b, 9, "9")
    gotA = inorder_keys(a.root)
    print("join(empty, b, 9): inorder:", gotA)
    print_check("contains 9 and b keys", gotA == [9, 10, 12, 15])
    print_check("is BST", is_bst(a.root))
    okA, _ = avl_ok_and_height(a.root)
    print_check("is AVL (balance+heights)", okA)

    # case B: tree2 empty
    c = AVLTree()
    d = AVLTree()
    for k in [1, 2, 3]:
        c.insert(k, str(k))
    c.join(d, 4, "4")
    gotB = inorder_keys(c.root)
    print("join(c, empty, 4): inorder:", gotB)
    print_check("contains c keys and 4", gotB == [1, 2, 3, 4])
    print_check("is BST", is_bst(c.root))
    okB, _ = avl_ok_and_height(c.root)
    print_check("is AVL (balance+heights)", okB)


def test_split_then_join_roundtrip():
    print_test_header("Test 11: split then join (roundtrip)", "split + join")

    keys = [10, 5, 15, 2, 7, 12, 20, 6, 8, 11, 13]
    t = AVLTree()
    for k in keys:
        t.insert(k, str(k))

    pivot = 10
    node, _ = t.search(pivot)

    original_sorted = sorted(keys)
    print_tree_info(t, "Original tree before split")
    left, right = t.split(node)

    # roundtrip rebuild: left + pivot + right
    left.join(right, pivot, str(pivot))
    rebuilt = inorder_keys(left.root)

    print("roundtrip split+join:")
    print("  expected inorder:", original_sorted)
    print("  rebuilt inorder :", rebuilt)
    print_check("rebuilt equals original keys", rebuilt == original_sorted)

    print_check("rebuilt is BST", is_bst(left.root))
    ok, _ = avl_ok_and_height(left.root)
    print_check("rebuilt is AVL (balance+heights)", ok)
    print_check("rebuilt parent pointers ok", parents_ok(left.root, None))


def main():
    test_insert_basic()
    test_insert_with_rotation()
    test_search()
    test_finger_insert()
    test_finger_search()
        # new:
    test_split_root()
    test_split_leaf()
    test_split_min_max()
    test_join_basic()
    test_join_with_empty_side()
    test_split_then_join_roundtrip()

main()