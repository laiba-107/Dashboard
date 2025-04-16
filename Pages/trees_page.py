import streamlit as st
import graphviz
from collections import deque
import time

st.set_page_config(page_title="Tree Structures", layout="wide")
st.title("🌲 Tree Structures (BST, AVL, Red-Black)")

# ---------- TREE CLASSES ---------- #

class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None

class AVLNode(BSTNode):
    def __init__(self, key):
        super().__init__(key)
        self.height = 1

class RBNode:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None
        self.parent = None
        self.color = 'R'  # R = Red, B = Black

# ---------- BST ---------- #
class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return BSTNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    def delete(self, root, key):
        if not root:
            return None
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            temp = self.min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)
        return root

    def min_value_node(self, node):
        while node.left:
            node = node.left
        return node

# ---------- AVL ---------- #
class AVL:
    def insert(self, root, key):
        if not root:
            return AVLNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Rotations
        if balance > 1:
            if key < root.left.key:  # LL
                return self.rotate_right(root)
            else:  # LR
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)

        if balance < -1:
            if key > root.right.key:  # RR
                return self.rotate_left(root)
            else:  # RL
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

        return root

    def delete(self, root, key):
        if not root:
            return root
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            temp = self.min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1:
            if self.get_balance(root.left) >= 0:
                return self.rotate_right(root)
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)

        if balance < -1:
            if self.get_balance(root.right) <= 0:
                return self.rotate_left(root)
            else:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

        return root

    def rotate_left(self, z):
        y = z.right
        T = y.left
        y.left = z
        z.right = T
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def rotate_right(self, z):
        y = z.left
        T = y.right
        y.right = z
        z.left = T
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

# ---------- Red-Black Tree (Insertion Only) ---------- #
class RBTree:
    def __init__(self):
        self.TNULL = RBNode(0)
        self.TNULL.color = 'B'
        self.root = self.TNULL

    def insert(self, key):
        node = RBNode(key)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if not y:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        node.color = 'R'
        self.fix_insert(node)

    def fix_insert(self, k):
        while k.parent and k.parent.color == 'R':
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 'R':
                    k.parent.color = 'B'
                    u.color = 'B'
                    k.parent.parent.color = 'R'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        k = self.rotate_right(k)
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    self.rotate_left(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 'R':
                    k.parent.color = 'B'
                    u.color = 'B'
                    k.parent.parent.color = 'R'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        k = self.rotate_left(k)
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    self.rotate_right(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'B'

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        return y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        return y

# ---------- Tree Visualization ---------- #
def render_tree(root, tree_type="BST"):
    def traverse(node, dot, label_func):
        if not node:
            return
        label = label_func(node)
        dot.node(str(id(node)), label)
        if node.left:
            dot.edge(str(id(node)), str(id(node.left)), label="L")
            traverse(node.left, dot, label_func)
        if node.right:
            dot.edge(str(id(node)), str(id(node.right)), label="R")
            traverse(node.right, dot, label_func)

    dot = graphviz.Digraph()
    label_func = lambda n: str(n.key) if tree_type == "BST" else f"{n.key} ({getattr(n, 'color', 'B')})"
    traverse(root, dot, label_func)
    return dot

# ---------- UI ---------- #
tree_option = st.sidebar.radio("Choose Tree Type", ["Binary Search Tree", "AVL Tree", "Red-Black Tree"])
action = st.sidebar.radio("Action", ["Insert", "Delete"])
value = st.sidebar.number_input("Value", step=1, format="%d")

if 'bst_tree' not in st.session_state: st.session_state.bst_tree = BST()
if 'bst_root' not in st.session_state: st.session_state.bst_root = None

if 'avl_tree' not in st.session_state: st.session_state.avl_tree = AVL()
if 'avl_root' not in st.session_state: st.session_state.avl_root = None

if 'rb_tree' not in st.session_state: st.session_state.rb_tree = RBTree()

if st.sidebar.button("Submit"):
    if tree_option == "Binary Search Tree":
        if action == "Insert":
            st.session_state.bst_root = st.session_state.bst_tree.insert(st.session_state.bst_root, value)
        else:
            st.session_state.bst_root = st.session_state.bst_tree.delete(st.session_state.bst_root, value)

    elif tree_option == "AVL Tree":
        if action == "Insert":
            st.session_state.avl_root = st.session_state.avl_tree.insert(st.session_state.avl_root, value)
        else:
            st.session_state.avl_root = st.session_state.avl_tree.delete(st.session_state.avl_root, value)

    elif tree_option == "Red-Black Tree":
        if action == "Insert":
            st.session_state.rb_tree.insert(value)
        else:
            st.warning("Red-Black Tree deletion not implemented")

st.subheader(f"Visualization - {tree_option}")
if tree_option == "Binary Search Tree" and st.session_state.bst_root:
    st.graphviz_chart(render_tree(st.session_state.bst_root))
elif tree_option == "AVL Tree" and st.session_state.avl_root:
    st.graphviz_chart(render_tree(st.session_state.avl_root))
elif tree_option == "Red-Black Tree" and st.session_state.rb_tree.root != st.session_state.rb_tree.TNULL:
    st.graphviz_chart(render_tree(st.session_state.rb_tree.root, "RB"))

