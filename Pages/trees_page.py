import streamlit as st
import graphviz
from collections import deque

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

    def search(self, root, key):
        if not root or root.key == key:
            return root
        if key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

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

        if balance > 1:
            if key < root.left.key:
                return self.rotate_right(root)
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)

        if balance < -1:
            if key > root.right.key:
                return self.rotate_left(root)
            else:
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

# ---------- Red-Black Tree ---------- #
class RBNode:
    def __init__(self, key):
        self.key = key
        self.color = 'R'
        self.left = None
        self.right = None
        self.parent = None

class RBTree:
    def __init__(self):
        self.TNULL = RBNode(0)
        self.TNULL.color = 'B'
        self.TNULL.left = self.TNULL.right = None
        self.root = self.TNULL

    def insert(self, key):
        node = RBNode(key)
        node.left = node.right = self.TNULL
        node.parent = None

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

        if not node.parent:
            node.color = 'B'
            return

        if not node.parent.parent:
            return

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
                        self.rotate_right(k)
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
                        self.rotate_left(k)
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    self.rotate_right(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'B'

    def delete_node(self, key):
        self.delete_node_helper(self.root, key)

    def delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.key == key:
                z = node
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        if z == self.TNULL:
            return  # Node to delete not found

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == 'B':
            self.fix_delete(x)

    def rb_transplant(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def fix_delete(self, x):
        while x != self.root and x.color == 'B':
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 'R':
                    s.color = 'B'
                    x.parent.color = 'R'
                    self.rotate_left(x.parent)
                    s = x.parent.right

                if s.left.color == 'B' and s.right.color == 'B':
                    s.color = 'R'
                    x = x.parent
                else:
                    if s.right.color == 'B':
                        s.left.color = 'B'
                        s.color = 'R'
                        self.rotate_right(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 'B'
                    s.right.color = 'B'
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 'R':
                    s.color = 'B'
                    x.parent.color = 'R'
                    self.rotate_right(x.parent)
                    s = x.parent.left

                if s.left.color == 'B' and s.right.color == 'B':
                    s.color = 'R'
                    x = x.parent
                else:
                    if s.left.color == 'B':
                        s.right.color = 'B'
                        s.color = 'R'
                        self.rotate_left(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 'B'
                    s.left.color = 'B'
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = 'B'

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

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

    def search(self, key):
        return self.search_helper(self.root, key)

    def search_helper(self, node, key):
        if node == self.TNULL or key == node.key:
            return node
        if key < node.key:
            return self.search_helper(node.left, key)
        return self.search_helper(node.right, key)


# ---------- Tree Visualization ---------- #
def render_tree(root, tree_type="BST"):
    def traverse(node, dot, label_func, color_func):
        if not node or (tree_type == "RB" and node.key == 0):
            return
        label = label_func(node)
        color = color_func(node)
        dot.node(str(id(node)), label, style="filled", fillcolor=color, fontcolor="white" if color == "black" else "black")

        if node.left and (tree_type != "RB" or node.left.key != 0):
            dot.edge(str(id(node)), str(id(node.left)), label="L")
            traverse(node.left, dot, label_func, color_func)
        if node.right and (tree_type != "RB" or node.right.key != 0):
            dot.edge(str(id(node)), str(id(node.right)), label="R")
            traverse(node.right, dot, label_func, color_func)

    dot = graphviz.Digraph()
    label_func = lambda n: str(n.key)
    color_func = (lambda n: "red" if getattr(n, 'color', 'B') == 'R' else "black") if tree_type == "RB" else (lambda n: "lightblue")
    traverse(root, dot, label_func, color_func)
    return dot

# ---------- UI Setup ---------- #
tree_option = st.sidebar.radio("Choose Tree Type", ["Binary Search Tree", "AVL Tree", "Red-Black Tree"])

action = st.sidebar.radio("Action", ["Insert", "Delete", "Search"])

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
        elif action == "Delete":
            st.session_state.bst_root = st.session_state.bst_tree.delete(st.session_state.bst_root, value)
        elif action == "Search":
            result = st.session_state.bst_tree.search(st.session_state.bst_root, value)
            if result:
                st.success(f"🔍 Value {value} found in the BST!")
            else:
                st.error(f"❌ Value {value} not found in the BST.")

    elif tree_option == "AVL Tree":
        if action == "Insert":
            st.session_state.avl_root = st.session_state.avl_tree.insert(st.session_state.avl_root, value)
        elif action == "Delete":
            st.session_state.avl_root = st.session_state.avl_tree.delete(st.session_state.avl_root, value)
        elif action == "Search":
            result = st.session_state.avl_tree.search(st.session_state.avl_root, value)
            if result:
                st.success(f"🔍 Value {value} found in the AVL Tree!")
            else:
                st.error(f"❌ Value {value} not found in the AVL Tree.")

    elif tree_option == "Red-Black Tree":
        if action == "Insert":
            st.session_state.rb_tree.insert(value)
        elif action == "Delete":
            st.session_state.rb_tree.delete_node(value)
        elif action == "Search":
            result = st.session_state.rb_tree.search(value)
            if result != st.session_state.rb_tree.TNULL:
                st.success(f"🔍 Value {value} found in the Red-Black Tree!")
            else:
                st.error(f"❌ Value {value} not found in the Red-Black Tree.")

if st.sidebar.button("Reset Tree"):
    st.session_state.bst_root = None
    st.session_state.avl_root = None
    st.session_state.rb_tree = RBTree()

# ---------- Visualization ---------- #
st.subheader(f"Visualization - {tree_option}")
if tree_option == "Binary Search Tree" and st.session_state.bst_root:
    st.graphviz_chart(render_tree(st.session_state.bst_root))
elif tree_option == "AVL Tree" and st.session_state.avl_root:
    st.graphviz_chart(render_tree(st.session_state.avl_root))
elif tree_option == "Red-Black Tree" and st.session_state.rb_tree.root != st.session_state.rb_tree.TNULL:
    st.graphviz_chart(render_tree(st.session_state.rb_tree.root, "RB"))