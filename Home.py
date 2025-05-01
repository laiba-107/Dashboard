import streamlit as st
from PIL import Image
import io
import base64

# Custom CSS for enhanced aesthetics
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page Configuration
st.set_page_config(
    page_title="Algorithm Visualizer",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

# Load custom CSS
local_css("style.css")  # You'll need to create this file (see CSS below)

# Gradient header with animated text
st.markdown("""
<div class="gradient-header">
    <h1 class="animated-text">🧠 Algorithm & Data Structures Visualizer</h1>
</div>
""", unsafe_allow_html=True)

# Hero section with columns
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div class="welcome-box">
        <h2>✨ Welcome to Your Interactive Learning Portal</h2>
        <p>Explore, visualize, and master algorithms and data structures through beautiful, interactive demonstrations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <h3>🔍 Visual Learning</h3>
            <p>Step-by-step animations with color-coded operations</p>
        </div>
        <div class="feature-card">
            <h3>📊 Performance Metrics</h3>
            <p>Real-time complexity analysis and comparisons</p>
        </div>
        <div class="feature-card">
            <h3>🛠️ Interactive</h3>
            <p>Adjust parameters and see immediate results</p>
        </div>
        <div class="feature-card">
            <h3>📚 Comprehensive</h3>
            <p>From basic to advanced algorithms</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Animated algorithm visualization placeholder
    st.markdown("""
    <div class="visualization-placeholder">
        <img src="https://media.giphy.com/media/3oKIPEqDGUULpEU0aQ/giphy.gif" class="hero-gif">
    </div>
    """, unsafe_allow_html=True)

# Navigation cards
st.markdown("---")
st.markdown("<h2 class='section-title'>📚 Explore Our Visualizations</h2>", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
with nav_col1:
    st.markdown("""
    <div class="nav-card" onclick="window.location.href='/?nav=searching'">
        <h3>🔎 Searching</h3>
        <ul>
            <li>Linear Search</li>
            <li>Binary Search</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    st.markdown("""
    <div class="nav-card" onclick="window.location.href='/?nav=sorting'">
        <h3>📊 Sorting</h3>
        <ul>
            <li>Bubble Sort</li>
            <li>Merge Sort</li>
            <li>Quick Sort</li>
            <li>Heap Sort</li>
            <li>Insertion Sort</li>
            <li>Counting Sort</li>
            <li>Radix Sort</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with nav_col3:
    st.markdown("""
    <div class="nav-card" onclick="window.location.href='/?nav=trees'">
        <h3>🌳 Tree Structures</h3>
        <ul>
            <li>Binary Search Tree</li>
            <li>AVL Tree</li>
            <li>Red-Black Tree</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with nav_col4:
    st.markdown("""
    <div class="nav-card" onclick="window.location.href='/?nav=graphs'">
        <h3>📈 Graph Algorithms</h3>
        <ul>
            <li>BFS/DFS</li>
            <li>Dijkstra's</li>
            <li>Minimum Spanning Tree</li>
            <li>Greedy Algorithm</li>
            <li>Brute Force Algorithm</li>
            <li>Kruskal's Algorithm</li>
            <li>Floyed Warshall</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with nav_col5:
    st.markdown("""
    <div class="nav-card">
        <h3>Other Data Structures</h3>
        <ul>>
            <li>Stack</li>
            <li>Queue</li>
            <li>Linked List</li>
            <li>Hash Function</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Built with ❤️ using <strong>Python</strong>, <strong>Streamlit</strong>, and <strong>Graphviz</strong></p>
    <p>© 2023 Algorithm Visualizer | Created by <strong>Laiba Ali</strong></p>
</div>
""", unsafe_allow_html=True)