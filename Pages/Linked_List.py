import streamlit as st
import graphviz

# Page Configuration
st.set_page_config(page_title="Linked List Visualizer", layout="wide", page_icon="🔗")
st.title("🔗 Linked List Operations Visualizer")

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton>button {
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .section {
        padding: 15px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 20px;
    }
    .result-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #e6f7ff;
        border-left: 4px solid #1890ff;
    }
    .highlight {
        background-color: #fffacd;
        padding: 2px 5px;
        border-radius: 3px;
    }
    .tab-content {
        padding: 15px;
        border-radius: 0 0 10px 10px;
        background-color: white;
        border: 1px solid #e6e6e6;
        border-top: none;
    }
</style>
""", unsafe_allow_html=True)

# Node classes
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

# Initialize session state
if 'singly_list' not in st.session_state:
    st.session_state.singly_list = None
if 'doubly_list' not in st.session_state:
    st.session_state.doubly_list = None
if 'circular_list' not in st.session_state:
    st.session_state.circular_list = None

# Visualization functions
def visualize_singly_linked_list(head):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')
    
    current = head
    index = 0
    while current:
        dot.node(str(index), str(current.data), shape='box', style='filled', 
                fillcolor='#4CAF50', fontcolor='white')
        if current.next:
            dot.edge(str(index), str(index+1), arrowhead='vee')
        current = current.next
        index += 1
    
    if head:
        dot.node('head', 'Head', shape='none')
        dot.edge('head', '0', style='dashed')
    
    st.graphviz_chart(dot)

def visualize_doubly_linked_list(head):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')
    
    current = head
    index = 0
    while current:
        # Node
        dot.node(str(index), str(current.data), shape='box', style='filled', 
                fillcolor='#FF9800', fontcolor='white')
        
        # Next pointer
        if current.next:
            dot.edge(str(index), str(index+1), arrowhead='vee', label='next')
        
        # Prev pointer
        if current.prev:
            dot.edge(str(index), str(index-1), arrowhead='vee', label='prev', 
                   color='blue', style='dashed')
        
        current = current.next
        index += 1
    
    if head:
        dot.node('head', 'Head', shape='none')
        dot.edge('head', '0', style='dashed')
    
    st.graphviz_chart(dot)

def visualize_circular_linked_list(head):
    if not head:
        st.info("Circular Linked List is empty")
        return
    
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')
    
    current = head
    index = 0
    nodes = {}
    
    # First pass to create all nodes
    while True:
        nodes[current] = index
        dot.node(str(index), str(current.data), shape='box', style='filled', 
                fillcolor='#9C27B0', fontcolor='white')
        current = current.next
        index += 1
        if current == head:
            break
    
    # Second pass to create edges
    current = head
    while True:
        next_index = nodes[current.next]
        dot.edge(str(nodes[current]), str(next_index), arrowhead='vee')
        current = current.next
        if current == head:
            break
    
    dot.node('head', 'Head', shape='none')
    dot.edge('head', '0', style='dashed')
    
    st.graphviz_chart(dot)

# Singly Linked List Operations
def singly_insert_at_end(data):
    new_node = Node(data)
    if not st.session_state.singly_list:
        st.session_state.singly_list = new_node
    else:
        current = st.session_state.singly_list
        while current.next:
            current = current.next
        current.next = new_node
    st.success(f"Inserted {data} at end")

def singly_delete_node(data):
    if not st.session_state.singly_list:
        st.warning("List is empty")
        return
    
    if st.session_state.singly_list.data == data:
        st.session_state.singly_list = st.session_state.singly_list.next
        st.success(f"Deleted {data} from head")
        return
    
    current = st.session_state.singly_list
    while current.next:
        if current.next.data == data:
            current.next = current.next.next
            st.success(f"Deleted {data}")
            return
        current = current.next
    
    st.warning(f"{data} not found in list")

def singly_search(data):
    current = st.session_state.singly_list
    index = 0
    while current:
        if current.data == data:
            return index
        current = current.next
        index += 1
    return -1

# Doubly Linked List Operations
def doubly_insert_at_end(data):
    new_node = DoublyNode(data)
    if not st.session_state.doubly_list:
        st.session_state.doubly_list = new_node
    else:
        current = st.session_state.doubly_list
        while current.next:
            current = current.next
        current.next = new_node
        new_node.prev = current
    st.success(f"Inserted {data} at end")

def doubly_delete_node(data):
    if not st.session_state.doubly_list:
        st.warning("List is empty")
        return
    
    current = st.session_state.doubly_list
    while current:
        if current.data == data:
            if current.prev:
                current.prev.next = current.next
            else:
                st.session_state.doubly_list = current.next
            
            if current.next:
                current.next.prev = current.prev
            
            st.success(f"Deleted {data}")
            return
        current = current.next
    
    st.warning(f"{data} not found in list")

# Circular Linked List Operations
def circular_insert_at_end(data):
    new_node = Node(data)
    if not st.session_state.circular_list:
        new_node.next = new_node
        st.session_state.circular_list = new_node
    else:
        current = st.session_state.circular_list
        while current.next != st.session_state.circular_list:
            current = current.next
        current.next = new_node
        new_node.next = st.session_state.circular_list
    st.success(f"Inserted {data} at end")

def circular_delete_node(data):
    if not st.session_state.circular_list:
        st.warning("List is empty")
        return
    
    # Case 1: Only one node
    if (st.session_state.circular_list.next == st.session_state.circular_list and 
        st.session_state.circular_list.data == data):
        st.session_state.circular_list = None
        st.success(f"Deleted {data}")
        return
    
    current = st.session_state.circular_list
    prev = None
    
    # Find the node to delete
    while True:
        if current.data == data:
            break
        prev = current
        current = current.next
        if current == st.session_state.circular_list:
            st.warning(f"{data} not found in list")
            return
    
    # If node is head
    if current == st.session_state.circular_list:
        # Find the last node to update its next pointer
        last = st.session_state.circular_list
        while last.next != st.session_state.circular_list:
            last = last.next
        st.session_state.circular_list = st.session_state.circular_list.next
        last.next = st.session_state.circular_list
    else:
        prev.next = current.next
    
    st.success(f"Deleted {data}")

# Main Content
list_type = st.selectbox(
    "Select Linked List Type",
    ["Singly Linked List", "Doubly Linked List", "Circular Linked List"],
    index=0
)

if list_type == "Singly Linked List":
    st.subheader("Singly Linked List Operations")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Operations")
        operation = st.radio(
            "Select operation:",
            ["Insert", "Delete", "Search"],
            horizontal=True
        )
        
        value = st.text_input("Enter value:")
        
        if st.button("Execute"):
            if value:
                if operation == "Insert":
                    singly_insert_at_end(value)
                elif operation == "Delete":
                    singly_delete_node(value)
                elif operation == "Search":
                    index = singly_search(value)
                    if index != -1:
                        st.success(f"Found {value} at position {index}")
                    else:
                        st.warning(f"{value} not found in list")
            else:
                st.warning("Please enter a value")
        
        if st.button("Clear List", type="primary"):
            st.session_state.singly_list = None
            st.success("List cleared")
    
    with col2:
        st.markdown("### Visualization")
        visualize_singly_linked_list(st.session_state.singly_list)
        
        st.markdown("### List Contents")
        current = st.session_state.singly_list
        items = []
        while current:
            items.append(str(current.data))
            current = current.next
        st.write(" → ".join(items) if items else "Empty list")

elif list_type == "Doubly Linked List":
    st.subheader("Doubly Linked List Operations")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Operations")
        operation = st.radio(
            "Select operation:",
            ["Insert", "Delete"],
            horizontal=True
        )
        
        value = st.text_input("Enter value:")
        
        if st.button("Execute"):
            if value:
                if operation == "Insert":
                    doubly_insert_at_end(value)
                elif operation == "Delete":
                    doubly_delete_node(value)
            else:
                st.warning("Please enter a value")
        
        if st.button("Clear List", type="primary"):
            st.session_state.doubly_list = None
            st.success("List cleared")
    
    with col2:
        st.markdown("### Visualization")
        visualize_doubly_linked_list(st.session_state.doubly_list)
        
        st.markdown("### List Contents (Forward)")
        current = st.session_state.doubly_list
        items_forward = []
        while current:
            items_forward.append(str(current.data))
            current = current.next
        st.write(" ↔ ".join(items_forward) if items_forward else "Empty list")

else:  # Circular Linked List
    st.subheader("Circular Linked List Operations")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Operations")
        operation = st.radio(
            "Select operation:",
            ["Insert", "Delete"],
            horizontal=True
        )
        
        value = st.text_input("Enter value:")
        
        if st.button("Execute"):
            if value:
                if operation == "Insert":
                    circular_insert_at_end(value)
                elif operation == "Delete":
                    circular_delete_node(value)
            else:
                st.warning("Please enter a value")
        
        if st.button("Clear List", type="primary"):
            st.session_state.circular_list = None
            st.success("List cleared")
    
    with col2:
        st.markdown("### Visualization")
        visualize_circular_linked_list(st.session_state.circular_list)
        
        st.markdown("### List Contents")
        if st.session_state.circular_list:
            current = st.session_state.circular_list
            items = []
            while True:
                items.append(str(current.data))
                current = current.next
                if current == st.session_state.circular_list:
                    break
            st.write(" → ".join(items) + " → ...")
        else:
            st.write("Empty list")

# Information Section
st.markdown("---")
with st.expander("ℹ️ About Linked Lists"):
    st.markdown("""
    **Linked List Visualizer** demonstrates:
    - **Singly Linked List**: Nodes with data and a next pointer
    - **Doubly Linked List**: Nodes with data, next and prev pointers
    - **Circular Linked List**: Last node points back to the first
    
    **Operations Supported:**
    - **Insert**: Add a new node at the end
    - **Delete**: Remove a node with specific value
    - **Search**: Find a node's position (Singly only)
    
    **Visualization Guide:**
    - **Singly**: Green boxes with right arrows
    - **Doubly**: Orange boxes with next (black) and prev (blue) arrows
    - **Circular**: Purple boxes with circular connections
    - Dashed arrow from Head indicates the start
    """)

with st.expander("📝 Linked List Implementation Details"):
    st.markdown("""
    ```python
    # Singly Linked List Node
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
    
    # Doubly Linked List Node
    class DoublyNode:
        def __init__(self, data):
            self.data = data
            self.next = None
            self.prev = None
    
    # Circular Linked List uses standard Node
    # but last node's next points to head
    
    # Common Operations:
    # 1. Insert at end:
    #    - Create new node
    #    - Traverse to end
    #    - Link last node to new node
    #    (For circular, new node points to head)
    
    # 2. Delete node:
    #    - Find node to delete
    #    - Update previous node's next pointer
    #    - (For doubly) Update next node's prev pointer
    #    - (For circular) Handle head deletion specially
    ```
    """)