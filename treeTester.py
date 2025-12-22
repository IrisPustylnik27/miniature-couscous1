# ---------------------------------------------------------
# avl_tree_visualizer.py
# Standalone AVL tree visualization tool.
# Works with your AVLTree.py implementation.
# ---------------------------------------------------------

from AVLTree import AVLTree, AVLNode


# =========================================================
#   ROTATED (VERTICAL) TREE PRINT
# =========================================================

def _print_subtree_vertical(node, indent="", last=True):
    """Pretty-print the AVL subtree vertically (rotated)."""
    if node is None or not node.is_real_node():
        return

    print(indent + ("`-- " if last else "|-- ") + f"{node.key} (h={node.height})")

    indent += "    " if last else "|   "

    children = []
    if node.left and node.left.is_real_node():
        children.append(node.left)
    if node.right and node.right.is_real_node():
        children.append(node.right)

    for i, child in enumerate(children):
        _print_subtree_vertical(child, indent, i == len(children) - 1)


def print_tree_vertical(tree: AVLTree):
    """Public wrapper for vertical tree printing."""
    if tree.root is None or not tree.root.is_real_node():
        print("<empty AVL>")
        return
    _print_subtree_vertical(tree.root)


# =========================================================
#   ASCII (HORIZONTAL) TREE PRINT
# =========================================================

def _build_ascii_tree(node):
    """
    Recursive ASCII tree builder.
    Returns (lines, width, height, middle_position)
    """
    if node is None or not node.is_real_node():
        return [], 0, 0, 0

    label = f"{node.left.height - node.right.height,node.key , node.height}"
    label_width = len(label)

    # Leaf node
    if (node.left is None or not node.left.is_real_node()) and \
       (node.right is None or not node.right.is_real_node()):
        return [label], label_width, 1, label_width // 2

    # Recursively build left subtree
    left_lines, left_w, left_h, left_mid = _build_ascii_tree(node.left)

    # Recursively build right subtree
    right_lines, right_w, right_h, right_mid = _build_ascii_tree(node.right)

    # Node center position
    root_mid = label_width // 2

    # First line: the label
    first_line = (" " * left_w) + label + (" " * right_w)

    # Second line: left and right connectors
    left_connector  = ( " " * left_mid ) + ("/" if left_w > 0 else " ")
    left_connector += (" " * (label_width - root_mid - 1))

    right_connector  = (" " * (root_mid))
    right_connector += ("\\" if right_w > 0 else " ")
    right_connector += (" " * (right_w - right_mid - 1))

    second_line = left_connector + right_connector

    # Merge subtrees line-by-line
    height = max(left_h, right_h)
    merged_lines = []
    for i in range(height):
        left_part  = left_lines[i] if i < left_h else " " * left_w
        right_part = right_lines[i] if i < right_h else " " * right_w
        merged_lines.append(left_part + (" " * label_width) + right_part)

    # Final block
    return [first_line, second_line] + merged_lines, left_w + label_width + right_w, len(merged_lines)+2, left_w + root_mid


def print_tree_ascii(tree: AVLTree):
    """Prints the tree using a horizontal ASCII diagram."""
    if tree.root is None or not tree.root.is_real_node():
        print("<empty AVL>")
        return

    lines, *_ = _build_ascii_tree(tree.root)
    for line in lines:
        print(line)


# =========================================================
#   DEMO (RUN THIS FILE DIRECTLY)
# =========================================================

if __name__ == "__main__":
    print("Building sample AVL tree...\n")
    T = AVLTree()
    l = [76, 41, 28, 46, 39, 11, 48, 1, 6, 62]
    pivot = 39
    for i in l:
        T.insert(i,str(i))

    print_tree_ascii(T)
    a = T.root.left.left
    b = T.root.left

    t1, t2 = T.split(T.root.left.right)

    print("\n===== ASCII Horizontal Tree =====\n")
    print("t1 - ")

    print_tree_ascii(t1)

    print("**********")
    print("t2 - ")
    print_tree_ascii(t2)
    # print("\n===== Rotated (Vertical) Print =====\n")
    # print_tree_vertical(t1)