# pages/3_🧩_Other_Data_Structures.py
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time
from collections import deque

# Initialize session state
def init_session_state():
    if 'stack' not in st.session_state:
        st.session_state.stack = []
    if 'queue' not in st.session_state:
        st.session_state.queue = deque()
    if 'hash_table' not in st.session_state:
        st.session_state.hash_table = [[] for _ in range(10)]
    if 'graph' not in st.session_state:
        st.session_state.graph = nx.Graph()

def visualize_stack():
    fig, ax = plt.subplots(figsize=(4,6))
    if st.session_state.stack:
        for i, val in enumerate(reversed(st.session_state.stack)):
            ax.barh(i, 1, height=0.8, color='skyblue')
            ax.text(0.5, i, str(val), ha='center', va='center')
        ax.set_title("Stack (Top to Bottom)")
        ax.axis('off')
    else:
        ax.text(0.5, 0.5, "Empty Stack", ha='center', va='center')
        ax.axis('off')
    st.pyplot(fig)

def visualize_queue():
    fig, ax = plt.subplots(figsize=(8,3))
    if st.session_state.queue:
        for i, val in enumerate(st.session_state.queue):
            ax.bar(i, 1, width=0.8, color='lightgreen')
            ax.text(i, 0.5, str(val), ha='center', va='center')
        ax.set_title("Queue (Front to Rear)")
        ax.axis('off')
    else:
        ax.text(0.5, 0.5, "Empty Queue", ha='center', va='center')
        ax.axis('off')
    st.pyplot(fig)

def visualize_hash_table():
    fig, ax = plt.subplots(figsize=(10,4))
    for i, bucket in enumerate(st.session_state.hash_table):
        ax.barh(i, len(bucket), height=0.6, color='salmon')
        ax.text(len(bucket)/2, i, f"Bucket {i}: {bucket}", ha='center', va='center')
    ax.set_title("Hash Table (Chaining Collision Resolution)")
    ax.set_yticks(range(len(st.session_state.hash_table)))
    ax.set_xticks([])
    st.pyplot(fig)

def visualize_graph():
    fig, ax = plt.subplots(figsize=(8,6))
    if st.session_state.graph.nodes():
        pos = nx.spring_layout(st.session_state.graph)
        nx.draw(st.session_state.graph, pos, with_labels=True, 
                node_color='lightblue', ax=ax)
        ax.set_title("Graph Visualization")
    else:
        ax.text(0.5, 0.5, "Empty Graph", ha='center', va='center')
        ax.axis('off')
    st.pyplot(fig)

def show():
    st.title("🧩 Other Data Structures")
    init_session_state()
    
    ds_type = st.sidebar.selectbox(
        "Select Data Structure:",
        ["Stack", "Queue", "Hash Table"]
    )
    
    if ds_type == "Stack":
        st.header("Stack (LIFO)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Operations")
            stack_value = st.text_input("Enter value to push:")
            if st.button("Push"):
                if stack_value:
                    st.session_state.stack.append(stack_value)
            
            if st.button("Pop"):
                if st.session_state.stack:
                    st.session_state.stack.pop()
                else:
                    st.warning("Stack is empty!")
            
            st.write("**Time Complexity:**")
            st.write("- Push: O(1)")
            st.write("- Pop: O(1)")
        
        with col2:
            st.subheader("Visualization")
            visualize_stack()
    
    elif ds_type == "Queue":
        st.header("Queue (FIFO)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Operations")
            queue_value = st.text_input("Enter value to enqueue:")
            if st.button("Enqueue"):
                if queue_value:
                    st.session_state.queue.append(queue_value)
            
            if st.button("Dequeue"):
                if st.session_state.queue:
                    st.session_state.queue.popleft()
                else:
                    st.warning("Queue is empty!")
            
            st.write("**Time Complexity:**")
            st.write("- Enqueue: O(1)")
            st.write("- Dequeue: O(1)")
        
        with col2:
            st.subheader("Visualization")
            visualize_queue()
    
    elif ds_type == "Hash Table":
        st.header("Hash Table with Chaining")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Operations")
            hash_key = st.text_input("Enter key:")
            hash_value = st.text_input("Enter value:")
            
            if st.button("Insert"):
                if hash_key and hash_value:
                    index = hash(hash_key) % len(st.session_state.hash_table)
                    st.session_state.hash_table[index].append((hash_key, hash_value))
            
            if st.button("Search"):
                if hash_key:
                    index = hash(hash_key) % len(st.session_state.hash_table)
                    found = None
                    for k, v in st.session_state.hash_table[index]:
                        if k == hash_key:
                            found = v
                            break
                    if found:
                        st.success(f"Found: {found}")
                    else:
                        st.warning("Key not found")
            
            st.write("**Time Complexity:**")
            st.write("- Insert: O(1) average")
            st.write("- Search: O(1) average")
        
        with col2:
            st.subheader("Visualization")
            visualize_hash_table()

        with col2:
            st.subheader("Visualization")
            visualize_graph()

if __name__ == "__main__":
    show()