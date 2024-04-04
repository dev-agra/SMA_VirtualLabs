import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations, takewhile
from networkx.algorithms.community import girvan_newman

def app():
    def internal_edge_density(G, nodes_subset):
        subgraph = G.subgraph(nodes_subset)
        if len(nodes_subset) > 1:
            return 2 * subgraph.number_of_edges() / (len(nodes_subset) * (len(nodes_subset) - 1))
        else:
            return 0

    def brute_force_community_detection(G):
        nodes = list(G.nodes())
        all_communities = []
        for n in range(1, len(nodes) + 1):
            for subset in combinations(nodes, n):
                if internal_edge_density(G, subset) > 0.5:
                    if not any(set(subset).issubset(community) for community in all_communities):
                        all_communities.append(set(subset))
        final_communities = [community for community in all_communities if not any(community < other for other in all_communities if community != other)]
        return final_communities

    def girvan_newman_community_detection(G):
        comp = girvan_newman(G)
        limited = takewhile(lambda c: len(c) <= 10, comp)
        for communities in limited:
            return sorted(map(sorted, communities), key=len, reverse=True)

    def plot_communities(G, communities):
        plt.figure(figsize=(8, 8))
        pos = nx.spring_layout(G)
        for i, community in enumerate(communities):
            nx.draw_networkx_nodes(G, pos, nodelist=community, node_color=f"C{i}")
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        nx.draw_networkx_labels(G, pos)
        plt.axis('off')
        plt.legend([f"Community {i+1}" for i in range(len(communities))], loc='upper left')
        st.pyplot(plt)

    st.title("Community Detection in Graphs")

    method = st.sidebar.selectbox("Choose a community detection method", ["Brute Force", "Girvan-Newman"])
    num_nodes = st.sidebar.number_input("Number of Nodes", min_value=3, value=10, step=1)
    num_edges = st.sidebar.number_input("Number of Edges", min_value=3, max_value=num_nodes*(num_nodes-1)//2, value=min(15, num_nodes*(num_nodes-1)//2), step=1)

    # New Theory section
    st.sidebar.header("Theory")
    theory_method = st.sidebar.radio("Select an algorithm for theory", ["Brute Force", "Girvan-Newman"])

    if st.sidebar.button("Show Theory"):
        # Theory section for Brute Force Algorithm
        if theory_method == "Brute Force":
            st.subheader("Brute Force Algorithm for Community Detection")
            st.write("### Theory Overview")
            st.write("""
            The brute-force method for community detection in social networks attempts to identify the optimal division of nodes into communities by exhaustively exploring all possible combinations. Here’s a step-by-step breakdown of the algorithm:

            1. **Create or Use a Predefined Graph**: Start with a graph of N nodes and its edges. This can be a custom graph or an inbuilt graph like a barbell graph.
            
            2. **Initialize Two Lists for Communities**: Create two lists, named FirstCommunity and SecondCommunity, to hold the nodes belonging to each community.
            
            3. **Distribute Nodes into Communities**: Begin by placing the first node in FirstCommunity and the remaining N-1 nodes in SecondCommunity. Then, calculate the inter-community (between communities) and intra-community (within a community) edges.
            
            4. **Generate Combinations**: Create all possible combinations of nodes distributed between the two communities.
            
            5. **Evaluate All Combinations**: For every combination generated in step 4, repeat the process of evaluating inter and intra-community edges.
            
            6. **Determine the Best Division**: Identify which division of nodes into communities is optimal by calculating the ratio of intra-community edges to the number of inter-community edges.
            
            7. **Identify and Output Optimal Communities**: Find the configuration of FirstCommunity and SecondCommunity that yields the maximum ratio, indicating the most distinct division of communities, and print these values.
            """)
            st.image(r".\files\Screenshot 2024-04-04 153121.png", caption="Placeholder for Brute Force Community Detection Visualization")
            st.write("This method, while straightforward, can be computationally intensive as it requires examining every possible way of dividing the graph's nodes into two communities. However, for smaller networks, it provides a clear metric for determining the most meaningful community structure by maximizing internal connections within communities and minimizing connections between them.")

            st.write("### Example")
            st.write("""
            To illustrate the brute-force approach to community detection, let's consider a simple example with a small network graph:

            **Step 1: Define the Graph** - Imagine we have a graph with 5 nodes connected in a specific pattern. For simplicity, let’s say it's a line graph where each node is connected to its immediate neighbors.
            
            **Step 2: Initial Community Division** - We start by placing the first node (Node 1) in FirstCommunity and the rest (Nodes 2 to 5) in SecondCommunity. This initial division allows us to begin our exploration of community configurations.
            """)
            st.image(r".\files\Screenshot 2024-04-04 152855.png", caption="Initial Division of Nodes into Communities")
            
            st.write("""
            **Step 3: Calculate Edge Densities** - We calculate the intra-community edges (edges within each community) and inter-community edges (edges between the communities). For our initial division, let's say we have 1 intra-community edge in FirstCommunity and 3 in SecondCommunity, with 1 inter-community edge between them.
            
            **Step 4: Explore Combinations** - Next, we systematically generate all possible combinations of nodes into the two communities. For instance, the next combination might involve moving Node 2 to FirstCommunity and keeping Nodes 3 to 5 in SecondCommunity.
            """)
            st.image(r".\files\Screenshot 2024-04-04 152859.png", caption="Exploring Node Combinations")
            
            st.write("""
            **Step 5: Evaluate Combinations** - For each combination, we repeat the calculation of intra and inter-community edges. This process is exhaustive and considers all ways in which the nodes can be divided into the two communities.
            
            **Step 6: Identify Optimal Division** - After evaluating all combinations, we determine the division with the highest ratio of intra-community edges to inter-community edges. Suppose the optimal division ends up being Nodes 1 and 2 in FirstCommunity and Nodes 3 to 5 in SecondCommunity, with the highest ratio of intra to inter edges.
            """)
            st.image(r".\files\Screenshot 2024-04-04 152903.png", caption="Optimal Community Division")
            
            st.write("""
            **Step 7: Conclusion** - The optimal division of nodes into communities, as determined by our brute-force method, suggests a natural clustering within the graph based on the existing connections. This example demonstrates the algorithm's capability to identify community structures within a network, albeit with a computational complexity that scales poorly with the size of the network.
            """)
        if theory_method == "Girvan-Newman":
            st.subheader("Girvan-Newman Algorithm Theory")
            st.write("### Theory Overview")
            st.write("""
            The Girvan-Newman algorithm is a method used to detect communities within a graph by progressively removing edges. It can be broken down into four main steps:

            1. **Calculate the Edge Betweenness Centrality**: For every edge in the graph, calculate the edge betweenness centrality, which quantifies the number of shortest paths passing through an edge. This helps in identifying edges that serve as bridges between communities.
            
            2. **Remove the Edge with the Highest Betweenness**: Identify and remove the edge with the highest betweenness centrality score, as it's likely a connector between distinct communities.
            
            3. **Recalculate Betweenness Centrality**: After removing an edge, recalculate the betweenness centrality for all remaining edges. The structure of the graph has changed, which could affect the centrality scores.
            
            4. **Repeat**: Continue repeating steps 2 and 3 until no more edges are left in the graph.
            """)
            st.image(r".\files\Screenshot 2024-04-04 151701.png", caption="Girvan-Newman Algorithm")

            st.write("### Example")

            st.image(r'.\files\Screenshot 2024-04-04 152122.png', caption="Illustration Showing Betweenness Centrality")
            st.write("""
            Consider a graph where edges are weighted based on the number of shortest paths passing through them. To simplify, we only consider undirected shortest paths. For example, the edge between nodes A and B has a weight of 1, indicating a single shortest path, without counting A->B and B->A as distinct.

            The edge between nodes C and D, having the highest weight, signifies it as the most utilized bridge between communities, making it a prime target for removal in the Girvan-Newman algorithm. This step intuitively separates communities by cutting off the most significant connection between them.
            """)
            st.image(r'.\files\Screenshot 2024-04-04 152126.png', caption="Graph Illustration Showing Communities Detected")
            
            st.write("""
            Following the removal of an edge, the algorithm necessitates a recalculation of betweenness centrality for all remaining edges. This recalculation ensures the algorithm adapts to the evolving structure of the graph as edges are removed. In the provided example, we reach a point where all edges have equal betweenness centrality, indicating a balanced distribution of shortest paths among the remaining edges.
            """)

    if st.sidebar.button("Generate and Analyze Graph"):
        G = nx.gnm_random_graph(num_nodes, num_edges)
        if method == "Brute Force":
            communities = brute_force_community_detection(G)
        else:
            communities = girvan_newman_community_detection(G)
        communities = [list(community) for community in communities]
        plot_communities(G, communities)
        st.write("### Detected Communities")
        for i, community in enumerate(communities, start=1):
            st.write(f"**Community {i}:** {community}")

