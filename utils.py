# utils.py (shared utilities)
import streamlit as st
import time
from graphviz import Digraph
import hashlib

def set_ui_theme():
    st.set_page_config(
        page_title="Algorithm Dashboard",
        page_icon="🧮",
        layout="wide"
    )
    
    # Custom CSS for consistent styling
    st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4f8bf9;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .css-1aumxhk {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def visualize_tree(tree, tree_type="BST"):
    dot = Digraph(comment=f'{tree_type} Visualization')
    dot.attr('node', shape='circle', width='1', fixedsize='true')
    
    if tree.root:
        nodes = [(tree.root, None)]
        while nodes:
            node, parent = nodes.pop(0)
            dot.node(str(node.value), str(node.value))
            
            if parent is not None:
                dot.edge(str(parent.value), str(node.value))
            
            if hasattr(node, 'left') and node.left:
                nodes.append((node.left, node))
            if hasattr(node, 'right') and node.right:
                nodes.append((node.right, node))
    
    return dot

def hash_function(key, size):
    return hash(key) % size

def animate_operation(placeholder, operation, *args):
    with placeholder:
        with st.spinner(f'Performing {operation}...'):
            time.sleep(0.5)  # Simulate operation time
            return operation(*args)