import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import random
import itertools
import math

st.set_page_config(page_title="Graph Algorithms", layout="wide")
st.title("📊 Graph Algorithms Visualizer")

# Initialize session state
if "graph" not in st.session_state:
    st.session_state.graph = nx.Graph()
if "weighted" not in st.session_state:
    st.session_state.weighted = False
if "directed" not in st.session_state:
    st.session_state.directed = False

# Sidebar - Graph Configuration
st.sidebar.header("Graph Builder")
graph_type = st.sidebar.radio("Graph Type", ["Undirected", "Directed"])
st.session_state.directed = graph_type == "Directed"
st.session_state.weighted = st.sidebar.checkbox("Weighted Graph")

# Node & Edge Management
node_input = st.sidebar.text_input("Add Node")
if st.sidebar.button("Add Node"):
    if node_input:
        st.session_state.graph.add_node(node_input)
        st.sidebar.success(f"Node '{node_input}' added!")

col1, col2 = st.sidebar.columns(2)
edge_start = col1.text_input("From")
edge_end = col2.text_input("To")
edge_weight = st.sidebar.number_input("Weight", min_value=1, value=1) if st.session_state.weighted else None

if st.sidebar.button("Add Edge"):
    if edge_start and edge_end:
        if st.session_state.weighted:
            st.session_state.graph.add_edge(edge_start, edge_end, weight=edge_weight)
            st.sidebar.success(f"Edge '{edge_start} → {edge_end}' (weight={edge_weight}) added!")
        else:
            st.session_state.graph.add_edge(edge_start, edge_end)
            st.sidebar.success(f"Edge '{edge_start} → {edge_end}' added!")

if st.sidebar.button("Generate Random Graph"):
    num_nodes = st.sidebar.slider("Number of nodes", 3, 10, 5)
    num_edges = st.sidebar.slider("Number of edges", num_nodes-1, num_nodes*(num_nodes-1)//2, num_nodes)
    
    st.session_state.graph = nx.DiGraph() if st.session_state.directed else nx.Graph()
    nodes = [str(i) for i in range(1, num_nodes+1)]
    st.session_state.graph.add_nodes_from(nodes)
    
    # Add random edges
    all_possible_edges = list(itertools.permutations(nodes, 2)) if st.session_state.directed else list(itertools.combinations(nodes, 2))
    random.shuffle(all_possible_edges)
    
    for i in range(min(num_edges, len(all_possible_edges))):
        u, v = all_possible_edges[i]
        weight = random.randint(1, 10) if st.session_state.weighted else None
        st.session_state.graph.add_edge(u, v, weight=weight)
    
    st.sidebar.success(f"Random graph with {num_nodes} nodes and {num_edges} edges created!")

if st.sidebar.button("Clear Graph"):
    st.session_state.graph.clear()
    st.sidebar.success("Graph cleared.")

# Algorithm selection
algorithm = st.selectbox(
    "Select Algorithm",
    [
        "Breadth-First Search (BFS)",
        "Depth-First Search (DFS)",
        "Dijkstra's Algorithm",
        "Bellman-Ford Algorithm",
        "Kruskal's Algorithm",
        "Prim's Algorithm",
        "Floyd-Warshall Algorithm",
        "TSP - Brute Force",
        "TSP - Greedy",
        "TSP - Branch and Bound"
    ]
)

# Visualization function with enhanced styling
def draw_graph(graph, highlight_nodes=[], highlight_edges=[], path=[], title="Graph", pos=None):
    plt.figure(figsize=(8, 6))
    
    # Create position if not provided
    if pos is None:
        pos = nx.spring_layout(graph, seed=42)  # Fixed seed for consistent layouts
    
    # Node colors
    node_colors = []
    for node in graph.nodes():
        if node in path:
            node_colors.append('red')
        elif node in highlight_nodes:
            node_colors.append('orange')
        else:
            node_colors.append('lightblue')
    
    # Edge colors and widths
    edge_colors = []
    edge_widths = []
    for u, v in graph.edges():
        if (u, v) in highlight_edges or (v, u) in highlight_edges:
            edge_colors.append('red')
            edge_widths.append(3.0)
        else:
            edge_colors.append('gray')
            edge_widths.append(1.0)
    
    # Draw the graph
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=800)
    nx.draw_networkx_labels(graph, pos, font_size=12, font_weight='bold')
    
    if st.session_state.weighted:
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10)
    
    nx.draw_networkx_edges(
        graph, pos, 
        edge_color=edge_colors, 
        width=edge_widths, 
        arrows=st.session_state.directed,
        arrowstyle='-|>',
        arrowsize=20
    )
    
    plt.title(title, fontsize=14)
    plt.axis('off')
    return plt, pos

# Algorithm implementations and visualizations
if algorithm == "Breadth-First Search (BFS)":
    st.subheader("Breadth-First Search (BFS)")
    start_node = st.selectbox("Start Node", list(st.session_state.graph.nodes()))
    
    if st.button("Run BFS"):
        if st.session_state.graph.nodes():
            visited = []
            queue = deque([start_node])
            bfs_steps = []
            
            while queue:
                node = queue.popleft()
                if node not in visited:
                    visited.append(node)
                    neighbors = list(st.session_state.graph.neighbors(node))
                    queue.extend(neighbors)
                    bfs_steps.append((list(visited), list(queue)))
            
            st.success(f"BFS Traversal Order: {' → '.join(visited)}")
            
            # Create animation of BFS steps
            for i, (visited_nodes, queue_nodes) in enumerate(bfs_steps):
                fig, pos = draw_graph(
                    st.session_state.graph,
                    highlight_nodes=visited_nodes + queue_nodes,
                    title=f"BFS Step {i+1}: Visiting {visited_nodes[-1]}"
                )
                st.pyplot(fig)
        else:
            st.error("Graph is empty!")

elif algorithm == "Depth-First Search (DFS)":
    st.subheader("Depth-First Search (DFS)")
    start_node = st.selectbox("Start Node", list(st.session_state.graph.nodes()))
    
    if st.button("Run DFS"):
        if st.session_state.graph.nodes():
            visited = []
            stack = [start_node]
            dfs_steps = []
            
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.append(node)
                    neighbors = list(st.session_state.graph.neighbors(node))
                    stack.extend(reversed(neighbors))
                    dfs_steps.append((list(visited), list(stack)))
            
            st.success(f"DFS Traversal Order: {' → '.join(visited)}")
            
            # Create animation of DFS steps
            for i, (visited_nodes, stack_nodes) in enumerate(dfs_steps):
                fig, pos = draw_graph(
                    st.session_state.graph,
                    highlight_nodes=visited_nodes + stack_nodes,
                    title=f"DFS Step {i+1}: Visiting {visited_nodes[-1]}"
                )
                st.pyplot(fig)
        else:
            st.error("Graph is empty!")

elif algorithm == "Dijkstra's Algorithm":
    st.subheader("Dijkstra's Algorithm (Shortest Path)")
    
    if not st.session_state.weighted:
        st.warning("Please enable weighted edges in the sidebar")
    else:
        source = st.selectbox("Source Node", list(st.session_state.graph.nodes()))
        target = st.selectbox("Target Node", list(st.session_state.graph.nodes()))
        
        if st.button("Find Shortest Path"):
            try:
                path = nx.dijkstra_path(st.session_state.graph, source, target)
                length = nx.dijkstra_path_length(st.session_state.graph, source, target)
                
                # Highlight the path edges
                path_edges = list(zip(path[:-1], path[1:]))
                
                fig, pos = draw_graph(
                    st.session_state.graph,
                    highlight_nodes=path,
                    highlight_edges=path_edges,
                    title=f"Shortest Path from {source} to {target} (Length: {length})"
                )
                st.pyplot(fig)
                
                st.success(f"Shortest Path: {' → '.join(path)} (Total weight: {length})")
            except nx.NetworkXNoPath:
                st.error(f"No path exists between {source} and {target}")

elif algorithm == "Bellman-Ford Algorithm":
    st.subheader("Bellman-Ford Algorithm (Handles Negative Weights)")
    
    if not st.session_state.weighted:
        st.warning("Please enable weighted edges in the sidebar")
    else:
        source = st.selectbox("Source Node", list(st.session_state.graph.nodes()))
        
        if st.button("Run Bellman-Ford"):
            try:
                # Run Bellman-Ford
                pred, dist = nx.bellman_ford_predecessor_and_distance(st.session_state.graph, source)
                
                # Create a subgraph showing all shortest paths
                shortest_paths = nx.DiGraph() if st.session_state.directed else nx.Graph()
                
                for target in dist:
                    if target != source:
                        try:
                            path = nx.reconstruct_path(source, target, pred)
                            for u, v in zip(path[:-1], path[1:]):
                                shortest_paths.add_edge(u, v, weight=st.session_state.graph[u][v]['weight'])
                        except nx.NetworkXNoPath:
                            pass
                
                # Draw the original graph with shortest paths highlighted
                fig, pos = draw_graph(
                    st.session_state.graph,
                    highlight_edges=shortest_paths.edges(),
                    title=f"Bellman-Ford Results from {source}"
                )
                st.pyplot(fig)
                
                # Show distances table
                st.subheader("Shortest Path Distances")
                dist_table = {"Node": [], "Distance": [], "Path": []}
                for node in sorted(dist.keys()):
                    dist_table["Node"].append(node)
                    dist_table["Distance"].append(dist[node])
                    try:
                        path = nx.reconstruct_path(source, node, pred)
                        dist_table["Path"].append(" → ".join(path))
                    except nx.NetworkXNoPath:
                        dist_table["Path"].append("No path")
                
                st.table(dist_table)
                
            except nx.NetworkXUnbounded:
                st.error("Graph contains a negative weight cycle")

elif algorithm in ["Kruskal's Algorithm", "Prim's Algorithm"]:
    st.subheader(f"{algorithm} (Minimum Spanning Tree)")
    
    if not nx.is_connected(st.session_state.graph.to_undirected()):
        st.error("Graph must be connected for MST algorithms")
    else:
        if st.button(f"Run {algorithm}"):
            if algorithm == "Kruskal's Algorithm":
                mst = nx.minimum_spanning_edges(st.session_state.graph.to_undirected(), algorithm='kruskal', data=True)
            else:  # Prim's
                mst = nx.minimum_spanning_edges(st.session_state.graph.to_undirected(), algorithm='prim', data=True)
            
            mst_edges = list(mst)
            mst_graph = nx.Graph()
            
            for u, v, d in mst_edges:
                mst_graph.add_edge(u, v, weight=d['weight'])
            
            total_weight = sum(d['weight'] for _, _, d in mst_edges)
            
            fig, pos = draw_graph(
                st.session_state.graph,
                highlight_edges=[(u, v) for u, v, _ in mst_edges],
                title=f"{algorithm} - MST (Total Weight: {total_weight})"
            )
            st.pyplot(fig)
            
            st.success(f"MST Edges: {[(u, v, d['weight']) for u, v, d in mst_edges]}")
            st.success(f"Total MST Weight: {total_weight}")

elif algorithm == "Floyd-Warshall Algorithm":
    st.subheader("Floyd-Warshall Algorithm (All Pairs Shortest Paths)")
    
    if not st.session_state.weighted:
        st.warning("Please enable weighted edges in the sidebar")
    else:
        if st.button("Run Floyd-Warshall"):
            # Compute shortest paths
            dist, paths = nx.floyd_warshall_predecessor_and_distance(st.session_state.graph)
            
            # Show distance matrix
            st.subheader("Distance Matrix")
            nodes = sorted(st.session_state.graph.nodes())
            distance_matrix = []
            
            for u in nodes:
                row = []
                for v in nodes:
                    if u == v:
                        row.append(0)
                    else:
                        row.append(dist[u][v] if v in dist[u] else math.inf)
                distance_matrix.append(row)
            
            st.table(distance_matrix)
            
            # Visualize paths between all nodes
            st.subheader("Shortest Paths Visualization")
            for i, u in enumerate(nodes):
                for j, v in enumerate(nodes):
                    if i < j and v in paths[u]:  # Only show each pair once
                        try:
                            path = nx.reconstruct_path(u, v, paths)
                            path_edges = list(zip(path[:-1], path[1:]))
                            
                            fig, _ = draw_graph(
                                st.session_state.graph,
                                highlight_nodes=path,
                                highlight_edges=path_edges,
                                title=f"Shortest Path from {u} to {v} (Distance: {dist[u][v]})"
                            )
                            st.pyplot(fig)
                        except nx.NetworkXNoPath:
                            pass

elif algorithm.startswith("TSP"):
    st.subheader(f"Traveling Salesman Problem ({algorithm.split(' - ')[1]})")
    
    if len(st.session_state.graph.nodes()) < 3:
        st.error("Need at least 3 nodes for TSP")
    else:
        nodes = list(st.session_state.graph.nodes())
        
        if algorithm == "TSP - Brute Force":
            if len(nodes) > 8:
                st.warning("Brute force is impractical for more than 8 nodes")
            else:
                if st.button("Run Brute Force"):
                    # Generate all possible tours
                    all_tours = list(itertools.permutations(nodes))
                    
                    # Calculate tour lengths
                    tours_with_length = []
                    for tour in all_tours:
                        # Complete the cycle
                        tour = list(tour) + [tour[0]]
                        length = 0
                        valid = True
                        
                        for i in range(len(tour)-1):
                            u, v = tour[i], tour[i+1]
                            if st.session_state.graph.has_edge(u, v):
                                if st.session_state.weighted:
                                    length += st.session_state.graph[u][v]['weight']
                                else:
                                    length += 1
                            else:
                                valid = False
                                break
                        
                        if valid:
                            tours_with_length.append((tour, length))
                    
                    if tours_with_length:
                        # Find the optimal tour
                        optimal_tour, optimal_length = min(tours_with_length, key=lambda x: x[1])
                        
                        # Visualize
                        tour_edges = list(zip(optimal_tour[:-1], optimal_tour[1:]))
                        
                        fig, pos = draw_graph(
                            st.session_state.graph,
                            highlight_nodes=optimal_tour,
                            highlight_edges=tour_edges,
                            title=f"Optimal TSP Tour (Length: {optimal_length})"
                        )
                        st.pyplot(fig)
                        
                        st.success(f"Optimal Tour: {' → '.join(optimal_tour)} (Length: {optimal_length})")
                        st.write(f"Evaluated {len(tours_with_length)} possible tours")
                    else:
                        st.error("No valid tours found (some edges are missing)")
        
        elif algorithm == "TSP - Greedy":
            if st.button("Run Greedy Algorithm"):
                start_node = random.choice(nodes)
                unvisited = set(nodes)
                unvisited.remove(start_node)
                tour = [start_node]
                current = start_node
                total_length = 0
                
                while unvisited:
                    # Find nearest neighbor
                    neighbors = []
                    for v in unvisited:
                        if st.session_state.graph.has_edge(current, v):
                            weight = st.session_state.graph[current][v]['weight'] if st.session_state.weighted else 1
                            neighbors.append((v, weight))
                    
                    if not neighbors:
                        st.error("Graph is not complete - greedy approach failed")
                        failed = True
                        break
                    
                    next_node, weight = min(neighbors, key=lambda x: x[1])
                    total_length += weight
                    tour.append(next_node)
                    unvisited.remove(next_node)
                    current = next_node
                
                # Return to start
                if st.session_state.graph.has_edge(current, start_node):
                    if st.session_state.weighted:
                        total_length += st.session_state.graph[current][start_node]['weight']
                    else:
                        total_length += 1
                    tour.append(start_node)
                    
                    # Visualize
                    tour_edges = list(zip(tour[:-1], tour[1:]))
                    
                    fig, pos = draw_graph(
                        st.session_state.graph,
                        highlight_nodes=tour,
                        highlight_edges=tour_edges,
                        title=f"Greedy TSP Tour (Length: {total_length})"
                    )
                    st.pyplot(fig)
                    
                    st.success(f"Greedy Tour: {' → '.join(tour)} (Length: {total_length})")
                else:
                    st.error("Cannot complete the tour (missing return edge)")
        
        elif algorithm == "TSP - Branch and Bound":
            st.warning("Branch and Bound implementation would go here")
            st.info("This is a more complex algorithm that would require additional implementation")

# Graph Visualization
st.markdown("---")
st.subheader("🧭 Current Graph")
if st.session_state.graph.nodes():
    fig, _ = draw_graph(st.session_state.graph, title="Current Graph")
    st.pyplot(fig)
    
    st.write("**Nodes:**", list(st.session_state.graph.nodes()))
    if st.session_state.weighted:
        st.write("**Edges:**", [(u, v, d['weight']) for u, v, d in st.session_state.graph.edges(data=True)])
    else:
        st.write("**Edges:**", list(st.session_state.graph.edges()))
else:
    st.info("Graph is empty. Add nodes and edges using the sidebar.")

# Algorithm Explanations
st.markdown("---")
st.subheader("📘 Algorithm Explanations")

expander = st.expander("Breadth-First Search (BFS)")
expander.markdown("""
- **Purpose**: Explore all nodes level by level
- **Approach**: Uses a queue to visit nodes in order of their distance from the start
- **Time Complexity**: O(V + E)
- **Use Cases**: Shortest path in unweighted graphs, web crawling
""")

expander = st.expander("Depth-First Search (DFS)")
expander.markdown("""
- **Purpose**: Explore as far as possible along each branch
- **Approach**: Uses a stack (recursively or iteratively) to go deep first
- **Time Complexity**: O(V + E)
- **Use Cases**: Topological sorting, maze solving, cycle detection
""")

expander = st.expander("Dijkstra's Algorithm")
expander.markdown("""
- **Purpose**: Find shortest paths from a single source in weighted graphs
- **Approach**: Greedy algorithm that always extends the shortest known path
- **Time Complexity**: O((V + E) log V) with priority queue
- **Limitations**: Doesn't work with negative weights
""")

expander = st.expander("Bellman-Ford Algorithm")
expander.markdown("""
- **Purpose**: Find shortest paths from a single source, works with negative weights
- **Approach**: Relaxes all edges repeatedly (V-1 times)
- **Time Complexity**: O(VE)
- **Use Cases**: Detecting negative weight cycles, routing protocols
""")

expander = st.expander("Kruskal's Algorithm")
expander.markdown("""
- **Purpose**: Find Minimum Spanning Tree (MST)
- **Approach**: Sort all edges and add them if they don't form a cycle
- **Time Complexity**: O(E log V)
- **Use Cases**: Network design, clustering
""")

expander = st.expander("Prim's Algorithm")
expander.markdown("""
- **Purpose**: Find Minimum Spanning Tree (MST)
- **Approach**: Grows the MST from an arbitrary starting node
- **Time Complexity**: O(E log V) with priority queue
- **Use Cases**: Similar to Kruskal's but often more efficient on dense graphs
""")

expander = st.expander("Floyd-Warshall Algorithm")
expander.markdown("""
- **Purpose**: Find shortest paths between all pairs of nodes
- **Approach**: Dynamic programming that considers all intermediate nodes
- **Time Complexity**: O(V³)
- **Use Cases**: Small graphs where all-pairs shortest paths are needed
""")

expander = st.expander("TSP Algorithms")
expander.markdown("""
- **Brute Force**: Examines all possible tours (O(n!))
- **Greedy**: Always chooses the nearest neighbor (not optimal but fast)
- **Branch and Bound**: More sophisticated approach that prunes the search space
""")