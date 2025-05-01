import streamlit as st
import graphviz

# Page Configuration
st.set_page_config(page_title="Hash Function Visualizer", layout="wide", page_icon="🔑")
st.title("🔑 Hash Function Visualizer")

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
    .hash-table {
        margin: 10px 0;
        padding: 10px;
        border-radius: 5px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .collision {
        background-color: #ffcdd2;
    }
    .occupied {
        background-color: #c8e6c9;
    }
    .empty {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'open_hash_table' not in st.session_state:
    st.session_state.open_hash_table = [[] for _ in range(10)]
if 'closed_hash_table' not in st.session_state:
    st.session_state.closed_hash_table = [None] * 10
if 'closed_method' not in st.session_state:
    st.session_state.closed_method = "Linear Probing"
if 'hash_table_size' not in st.session_state:
    st.session_state.hash_table_size = 10

# Hash functions
def simple_hash(key, size):
    return sum(ord(c) for c in str(key)) % size

def double_hash(key, size, attempt):
    h1 = simple_hash(key, size)
    h2 = 1 + sum(ord(c) * (i+1) for i, c in enumerate(str(key))) % (size - 1)
    return (h1 + attempt * h2) % size

# Hashing techniques
def open_hashing_insert(key, value):
    index = simple_hash(key, st.session_state.hash_table_size)
    st.session_state.open_hash_table[index].append((key, value))

def open_hashing_search(key):
    index = simple_hash(key, st.session_state.hash_table_size)
    for k, v in st.session_state.open_hash_table[index]:
        if k == key:
            return v
    return None

def linear_probing_insert(key, value):
    index = simple_hash(key, st.session_state.hash_table_size)
    attempt = 0
    while attempt < st.session_state.hash_table_size:
        new_index = (index + attempt) % st.session_state.hash_table_size
        if st.session_state.closed_hash_table[new_index] is None:
            st.session_state.closed_hash_table[new_index] = (key, value)
            return new_index
        attempt += 1
    raise Exception("Hash table is full")

def quadratic_probing_insert(key, value):
    index = simple_hash(key, st.session_state.hash_table_size)
    attempt = 0
    while attempt < st.session_state.hash_table_size:
        new_index = (index + attempt**2) % st.session_state.hash_table_size
        if st.session_state.closed_hash_table[new_index] is None:
            st.session_state.closed_hash_table[new_index] = (key, value)
            return new_index
        attempt += 1
    raise Exception("Hash table is full")

def double_hashing_insert(key, value):
    index = simple_hash(key, st.session_state.hash_table_size)
    attempt = 0
    while attempt < st.session_state.hash_table_size:
        new_index = double_hash(key, st.session_state.hash_table_size, attempt)
        if st.session_state.closed_hash_table[new_index] is None:
            st.session_state.closed_hash_table[new_index] = (key, value)
            return new_index
        attempt += 1
    raise Exception("Hash table is full")

def closed_hashing_search(key):
    method = st.session_state.closed_method
    index = simple_hash(key, st.session_state.hash_table_size)
    attempt = 0
    
    while attempt < st.session_state.hash_table_size:
        if method == "Linear Probing":
            new_index = (index + attempt) % st.session_state.hash_table_size
        elif method == "Quadratic Probing":
            new_index = (index + attempt**2) % st.session_state.hash_table_size
        else:  # Double Hashing
            new_index = double_hash(key, st.session_state.hash_table_size, attempt)
        
        if st.session_state.closed_hash_table[new_index] is None:
            return None
        if st.session_state.closed_hash_table[new_index][0] == key:
            return st.session_state.closed_hash_table[new_index][1]
        
        attempt += 1
    return None

# Visualization functions
def visualize_open_hashing():
    dot = graphviz.Digraph()
    dot.attr(rankdir='TB', size='8,5')
    
    for i in range(st.session_state.hash_table_size):
        chain = st.session_state.open_hash_table[i]
        with dot.subgraph(name=f'cluster_{i}') as c:
            c.attr(label=f'Index {i}', style='filled', fillcolor='#e1f5fe', color='lightgray')
            for j, (key, value) in enumerate(chain):
                if j == 0:
                    c.node(f'{i}_{j}', f"{key}: {value}", shape='box')
                else:
                    c.node(f'{i}_{j}', f"{key}: {value}", shape='box', style='filled', fillcolor='#ffccbc')
                if j > 0:
                    c.edge(f'{i}_{j-1}', f'{i}_{j}')
    
    st.graphviz_chart(dot)

def visualize_closed_hashing():
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR', size='8,2')
    
    for i in range(st.session_state.hash_table_size):
        entry = st.session_state.closed_hash_table[i]
        if entry is None:
            dot.node(str(i), "NULL", shape='box', style='filled', fillcolor='#f5f5f5')
        else:
            key, value = entry
            original_index = simple_hash(key, st.session_state.hash_table_size)
            if i == original_index:
                dot.node(str(i), f"{key}: {value}", shape='box', style='filled', fillcolor='#c8e6c9')
            else:
                dot.node(str(i), f"{key}: {value}", shape='box', style='filled', fillcolor='#ffccbc')
    
    st.graphviz_chart(dot)

# Main Content
hash_type = st.selectbox(
    "Select Hashing Technique",
    ["Open Hashing (Separate Chaining)", "Closed Hashing (Open Addressing)"],
    index=0
)

st.session_state.hash_table_size = st.slider(
    "Hash Table Size", 
    min_value=5, 
    max_value=10, 
    value=10,
    help="Adjust the size of the hash table"
)

if hash_type == "Open Hashing (Separate Chaining)":
    st.subheader("Open Hashing (Separate Chaining)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Operations")
        key = st.text_input("Enter key:")
        value = st.text_input("Enter value:")
        
        if st.button("Insert"):
            if key and value:
                open_hashing_insert(key, value)
                st.success(f"Inserted ({key}, {value})")
            else:
                st.warning("Please enter both key and value")
        
        if st.button("Search"):
            if key:
                result = open_hashing_search(key)
                if result is not None:
                    st.success(f"Found: {result}")
                else:
                    st.warning("Key not found")
            else:
                st.warning("Please enter a key to search")
        
        if st.button("Clear Table", type="primary"):
            st.session_state.open_hash_table = [[] for _ in range(st.session_state.hash_table_size)]
            st.success("Hash table cleared")
    
    with col2:
        st.markdown("### Hash Table Visualization")
        visualize_open_hashing()
        
        st.markdown("### Hash Table Contents")
        for i in range(st.session_state.hash_table_size):
            chain = st.session_state.open_hash_table[i]
            st.markdown(f"""
            <div class="hash-table">
                <strong>Index {i}:</strong> {[f"{k}:{v}" for k, v in chain] or "Empty"}
            </div>
            """, unsafe_allow_html=True)

else:  # Closed Hashing
    st.subheader("Closed Hashing (Open Addressing)")
    
    st.session_state.closed_method = st.radio(
        "Select collision resolution method:",
        ["Linear Probing", "Quadratic Probing", "Double Hashing"],
        horizontal=True
    )
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Operations")
        key = st.text_input("Enter key:", key="closed_key")
        value = st.text_input("Enter value:", key="closed_value")
        
        if st.button("Insert", key="closed_insert"):
            if key and value:
                try:
                    if st.session_state.closed_method == "Linear Probing":
                        index = linear_probing_insert(key, value)
                    elif st.session_state.closed_method == "Quadratic Probing":
                        index = quadratic_probing_insert(key, value)
                    else:  # Double Hashing
                        index = double_hashing_insert(key, value)
                    st.success(f"Inserted at index {index}")
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Please enter both key and value")
        
        if st.button("Search", key="closed_search"):
            if key:
                result = closed_hashing_search(key)
                if result is not None:
                    st.success(f"Found: {result}")
                else:
                    st.warning("Key not found")
            else:
                st.warning("Please enter a key to search")
        
        if st.button("Clear Table", key="closed_clear", type="primary"):
            st.session_state.closed_hash_table = [None] * st.session_state.hash_table_size
            st.success("Hash table cleared")
    
    with col2:
        st.markdown("### Hash Table Visualization")
        visualize_closed_hashing()
        
        st.markdown("### Hash Table Contents")
        for i in range(st.session_state.hash_table_size):
            entry = st.session_state.closed_hash_table[i]
            status = "Occupied" if entry is not None else "Empty"
            original_index = simple_hash(entry[0], st.session_state.hash_table_size) if entry else -1
            is_collision = entry is not None and i != original_index
            
            st.markdown(f"""
            <div class="hash-table {'collision' if is_collision else 'occupied' if entry else 'empty'}">
                <strong>Index {i}:</strong> {f"{entry[0]}:{entry[1]}" if entry else "NULL"}
                {f"<br><small>(Originally hashed to {original_index})</small>" if is_collision else ""}
            </div>
            """, unsafe_allow_html=True)

# Information Section
st.markdown("---")
with st.expander("ℹ️ About Hashing Techniques"):
    st.markdown("""
    **Hash Function Visualizer** demonstrates:
    - **Open Hashing (Separate Chaining)**: Collisions resolved by linked lists
    - **Closed Hashing (Open Addressing)**: Collisions resolved by probing
    
    **Closed Hashing Methods:**
    - **Linear Probing**: Check next sequential slots (h(x) + i) % size
    - **Quadratic Probing**: Check slots with quadratic jumps (h(x) + i²) % size
    - **Double Hashing**: Use second hash function (h1(x) + i*h2(x)) % size
    
    **Visualization Guide:**
    - **Open Hashing**: Chains shown as linked lists
    - **Closed Hashing**: 
      - Green: Direct placement
      - Orange: Collision resolution
      - Gray: Empty slots
    """)

with st.expander("📝 Hash Function Implementation Details"):
    st.markdown("""
    ```python
    # Simple hash function
    def simple_hash(key, size):
        return sum(ord(c) for c in str(key)) % size
    
    # Double hash function for double hashing
    def double_hash(key, size, attempt):
        h1 = simple_hash(key, size)
        h2 = 1 + sum(ord(c) * (i+1) for i, c in enumerate(str(key))) % (size - 1)
        return (h1 + attempt * h2) % size
    
    # Open Hashing Insert
    def open_hashing_insert(key, value):
        index = simple_hash(key, size)
        table[index].append((key, value))
    
    # Linear Probing Insert
    def linear_probing_insert(key, value):
        index = simple_hash(key, size)
        attempt = 0
        while attempt < size:
            new_index = (index + attempt) % size
            if table[new_index] is None:
                table[new_index] = (key, value)
                return new_index
            attempt += 1
        raise Exception("Hash table is full")
    ```
    """)