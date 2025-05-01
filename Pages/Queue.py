import streamlit as st
import graphviz

# Page Configuration
st.set_page_config(page_title="Queue Visualizer", layout="wide", page_icon="📊")
st.title("📊 Queue Operations Visualizer")

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
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
    .queue-container {
        margin-top: 20px;
        padding: 15px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .highlight {
        background-color: #fffacd;
        padding: 2px 5px;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'linear_queue' not in st.session_state:
    st.session_state.linear_queue = []
if 'circular_queue' not in st.session_state:
    st.session_state.circular_queue = [None] * 5  # Fixed size circular queue
    st.session_state.front = -1
    st.session_state.rear = -1

# Queue visualization functions
def visualize_linear_queue(queue):
    if not queue:
        st.info("Linear Queue is empty")
        return
    
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR', size='8,2', margin='0.1')
    
    # Add nodes (queue elements)
    for i, val in enumerate(queue):
        dot.node(str(i), str(val), shape='box', style='filled', 
                fillcolor='#4CAF50', fontcolor='white',
                width='0.8', height='0.5', fixedsize='true',
                fontsize='14')
    
    # Add edges to show order
    for i in range(len(queue)-1):
        dot.edge(str(i), str(i+1), style='bold')
    
    # Add pointers
    if queue:
        with dot.subgraph() as s:
            s.attr(rank='same')
            s.node('front', 'Front', shape='none')
            s.node('rear', 'Rear', shape='none')
            s.edge('front', str(0), style='dashed', color='red')
            s.edge('rear', str(len(queue)-1), style='dashed', color='blue')
    
    st.graphviz_chart(dot, use_container_width=True)

def visualize_circular_queue(queue, front, rear):
    size = len(queue)
    if front == -1:
        st.info("Circular Queue is empty")
        return
    
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR', size='8,2', margin='0.1')
    
    # Add nodes (queue elements)
    for i in range(size):
        label = str(queue[i]) if queue[i] is not None else "NULL"
        color = '#4CAF50' if queue[i] is not None else 'lightgray'
        dot.node(str(i), label, shape='box', style='filled', 
                fillcolor=color, fontcolor='white' if queue[i] is not None else 'black',
                width='0.8', height='0.5', fixedsize='true',
                fontsize='14')
    
    # Connect nodes in circular fashion
    for i in range(size-1):
        dot.edge(str(i), str(i+1), style='bold')
    dot.edge(str(size-1), str(0), style='bold')
    
    # Add pointers
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('front_ptr', 'Front', shape='none')
        s.node('rear_ptr', 'Rear', shape='none')
        s.edge('front_ptr', str(front), style='dashed', color='red')
        s.edge('rear_ptr', str(rear), style='dashed', color='blue')
    
    st.graphviz_chart(dot, use_container_width=True)

# Queue operations
def linear_enqueue(value):
    st.session_state.linear_queue.append(value)
    st.success(f"Enqueued {value} to linear queue")

def linear_dequeue():
    if not st.session_state.linear_queue:
        st.warning("Linear Queue is empty")
        return None
    value = st.session_state.linear_queue.pop(0)
    st.success(f"Dequeued {value} from linear queue")
    return value

def circular_enqueue(value):
    size = len(st.session_state.circular_queue)
    if (st.session_state.rear + 1) % size == st.session_state.front:
        st.warning("Circular Queue is full")
        return False
    
    if st.session_state.front == -1:  # First element
        st.session_state.front = st.session_state.rear = 0
    else:
        st.session_state.rear = (st.session_state.rear + 1) % size
    
    st.session_state.circular_queue[st.session_state.rear] = value
    st.success(f"Enqueued {value} to circular queue at position {st.session_state.rear}")
    return True

def circular_dequeue():
    if st.session_state.front == -1:
        st.warning("Circular Queue is empty")
        return None
    
    value = st.session_state.circular_queue[st.session_state.front]
    st.session_state.circular_queue[st.session_state.front] = None
    
    if st.session_state.front == st.session_state.rear:  # Last element
        st.session_state.front = st.session_state.rear = -1
    else:
        st.session_state.front = (st.session_state.front + 1) % len(st.session_state.circular_queue)
    
    st.success(f"Dequeued {value} from circular queue")
    return value

# Main Content
queue_type = st.selectbox(
    "Select Queue Type",
    ["Linear Queue", "Circular Queue"],
    index=0
)

if queue_type == "Linear Queue":
    st.subheader("Linear Queue Operations")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Queue Controls")
        value = st.text_input("Enter value to enqueue:", key="linear_value")
        
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            if st.button("Enqueue", key="linear_enqueue"):
                if value:
                    linear_enqueue(value)
                else:
                    st.warning("Please enter a value")
        with col1_2:
            if st.button("Dequeue", key="linear_dequeue"):
                linear_dequeue()
        
        if st.button("Clear Linear Queue", type="primary"):
            st.session_state.linear_queue = []
            st.success("Linear Queue cleared")
    
    with col2:
        st.markdown("### Queue Visualization")
        visualize_linear_queue(st.session_state.linear_queue)
        
        st.markdown("### Queue Contents")
        st.write(st.session_state.linear_queue)

else:  # Circular Queue
    st.subheader("Circular Queue Operations")
    st.markdown(f"Current size: {len(st.session_state.circular_queue)}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Queue Controls")
        value = st.text_input("Enter value to enqueue:", key="circular_value")
        
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            if st.button("Enqueue", key="circular_enqueue"):
                if value:
                    circular_enqueue(value)
                else:
                    st.warning("Please enter a value")
        with col1_2:
            if st.button("Dequeue", key="circular_dequeue"):
                circular_dequeue()
        
        if st.button("Clear Circular Queue", type="primary"):
            st.session_state.circular_queue = [None] * len(st.session_state.circular_queue)
            st.session_state.front = -1
            st.session_state.rear = -1
            st.success("Circular Queue cleared")
    
    with col2:
        st.markdown("### Queue Visualization")
        visualize_circular_queue(
            st.session_state.circular_queue,
            st.session_state.front,
            st.session_state.rear
        )
        
        st.markdown("### Queue Contents")
        st.write(st.session_state.circular_queue)
        
        st.markdown("### Queue Pointers")
        st.markdown(f"""
        - <span class="highlight">Front</span>: {st.session_state.front}
        - <span class="highlight">Rear</span>: {st.session_state.rear}
        """, unsafe_allow_html=True)

# Information Section
st.markdown("---")
with st.expander("ℹ️ About Queue Operations"):
    st.markdown("""
    **Queue Operations Visualizer** demonstrates:
    - **Linear Queue**: FIFO (First-In-First-Out) operations
    - **Circular Queue**: Efficient fixed-size queue implementation
    
    **Operations Supported:**
    - **Enqueue**: Add an element to the rear of the queue
    - **Dequeue**: Remove an element from the front of the queue
    
    **Key Concepts:**
    - **Linear Queue**: Simple implementation but can waste space
    - **Circular Queue**: Reuses empty spaces when elements are dequeued
    - **Front/Rear Pointers**: Track the start and end of the queue
    
    **Visualization Guide:**
    - Green boxes represent occupied queue slots
    - Gray boxes represent empty slots
    - Red dashed arrow shows Front pointer
    - Blue dashed arrow shows Rear pointer
    """)

# Queue implementation details
with st.expander("📝 Queue Implementation Details"):
    st.markdown("""
    ```python
    # Linear Queue Implementation
    queue = []  # Simple list
    
    def enqueue(value):
        queue.append(value)
    
    def dequeue():
        if not queue:
            return None
        return queue.pop(0)
    
    # Circular Queue Implementation
    SIZE = 5
    queue = [None] * SIZE
    front = rear = -1
    
    def circular_enqueue(value):
        if (rear + 1) % SIZE == front:
            return False  # Queue full
        
        if front == -1:  # First element
            front = rear = 0
        else:
            rear = (rear + 1) % SIZE
        
        queue[rear] = value
        return True
    
    def circular_dequeue():
        if front == -1:
            return None  # Queue empty
        
        value = queue[front]
        queue[front] = None
        
        if front == rear:  # Last element
            front = rear = -1
        else:
            front = (front + 1) % SIZE
        
        return value
    ```
    """)