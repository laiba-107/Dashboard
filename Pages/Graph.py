import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

st.set_page_config(page_title="Graphs", layout="wide")
st.title("📊 Graph Traversal Algorithms (BFS & DFS)")

# Initialize session state
if "graph" not in st.session_state:
    st.session_state.graph = nx.Graph()

# Sidebar - Node & Edge Management
st.sidebar.header("Graph Builder")

node_input = st.sidebar.text_input("Add Node")
if st.sidebar.button("Add Node"):
    if node_input:
        st.session_state.graph.add_node(node_input)
        st.sidebar.success(f"Node '{node_input}' added!")

col1, col2 = st.sidebar.columns(2)
edge_start = col1.text_input("From")
edge_end = col2.text_input("To")

if st.sidebar.button("Add Edge"):
    if edge_start and edge_end:
        st.session_state.graph.add_edge(edge_start, edge_end)
        st.sidebar.success(f"Edge '{edge_start} - {edge_end}' added!")

if st.sidebar.button("Clear Graph"):
    st.session_state.graph.clear()
    st.sidebar.success("Graph cleared.")

# BFS and DFS Implementations
def bfs(graph, start):
    visited = set()
    queue = deque([start])
    traversal = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            traversal.append(node)
            queue.extend([n for n in graph.neighbors(node) if n not in visited])
    return traversal

def dfs(graph, start):
    visited = set()
    stack = [start]
    traversal = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            traversal.append(node)
            stack.extend([n for n in reversed(list(graph.neighbors(node))) if n not in visited])
    return traversal

# Traversal Controls
st.subheader("Run Traversal Algorithm")
start_node = st.text_input("Start Node for Traversal")

algo = st.radio("Choose Algorithm", ["Breadth-First Search (BFS)", "Depth-First Search (DFS)"])

highlight_nodes = []
if st.button("Run Traversal"):
    if start_node and start_node in st.session_state.graph.nodes():
        if algo.startswith("Breadth"):
            result = bfs(st.session_state.graph, start_node)
            st.success("BFS Traversal: " + " → ".join(result))
        else:
            result = dfs(st.session_state.graph, start_node)
            st.success("DFS Traversal: " + " → ".join(result))
        highlight_nodes = result
    else:
        st.error("Start node is not in the graph.")

# Explanation
st.markdown("---")
st.subheader("📘 About")
st.markdown("""
This page demonstrates **Graph Traversal Algorithms** using:
- **Breadth-First Search (BFS)** – explores neighbors first
- **Depth-First Search (DFS)** – explores deeper before backtracking

All graphs are unweighted and undirected. Use the sidebar to build the graph and explore traversals interactively!
""")

# Graph Visualization (moved to bottom, small size)
def draw_graph(graph, highlight_nodes=[], title="Graph"):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(5, 3))  # Smaller size
    nx.draw(
        graph,
        pos,
        with_labels=True,
        ax=ax,
        node_color=["orange" if n in highlight_nodes else "lightblue" for n in graph.nodes()],
        node_size=600,
        font_size=10
    )
    return fig

st.markdown("---")
st.subheader("🧭 Graph Visualization")
fig = draw_graph(st.session_state.graph, highlight_nodes)
st.pyplot(fig)
