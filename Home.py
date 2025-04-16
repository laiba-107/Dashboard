import streamlit as st

st.set_page_config(page_title="Algorithm Visualizer", layout="wide")

st.title("📚 Algorithm & Data Structures Visualizer")
st.markdown("---")

# Intro section
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    Welcome to the **Algorithm & Data Structures Visualizer** – an interactive dashboard built using **Streamlit** that helps you explore fundamental algorithms and data structures with visual feedback.

    🔍 **What You’ll Find Here**:
    - Step-by-step walkthroughs of classic algorithms
    - Animated and color-coded visualizations
    - Real-time performance measurement
    - Hands-on interaction for deeper understanding

    👇 Use the **sidebar** on the left to navigate through pages:
    - **Searching Algorithms**
    - **Sorting Algorithms**
    - **Tree Structures** (BST, AVL, Red-Black Tree)
    - **Other Data Structures** (Stack, Queue, Hash Table, Graphs)
    - **Graphs** (with BFS & DFS traversal)
    """)
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/2933/2933898.png", width=200)

# Project goals
st.markdown("---")
st.subheader("🎯 Project Objective")
st.markdown("""
The goal of this project is to provide an intuitive, educational, and interactive platform for learners and developers to:

- Understand how algorithms and data structures work under the hood
- Practice tracing and analyzing code behavior visually
- Compare algorithmic performance on different data sizes

Built with ❤️ using Python, [Streamlit](https://streamlit.io), and [Graphviz](https://graphviz.org).
""")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>Made for educational purposes by <b>Laiba Ali</b></p>",
    unsafe_allow_html=True
)
