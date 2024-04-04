import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def app():
    # Function to create a random social network
    def create_random_social_network(num_nodes, probability):
        G = nx.erdos_renyi_graph(num_nodes, probability)
        return G

    # Function to find the influencer node
    def find_influencer_node(graph):
        centrality_scores = nx.degree_centrality(graph)
        influencer_node = max(centrality_scores, key=centrality_scores.get)
        return influencer_node

    # Function to calculate network measures
    def calculate_network_measures(graph):
        degree_centrality = nx.degree_centrality(graph)
        closeness_centrality = nx.closeness_centrality(graph)
        betweenness_centrality = nx.betweenness_centrality(graph)
        return degree_centrality, closeness_centrality, betweenness_centrality

    # Explanation of influencer nodes
    def influencer_node_explanation():
        st.write("An influencer node in a social network is a node that has a significant influence over other nodes. "
                "This influence is often measured based on the node's degree centrality, which represents the fraction "
                "of nodes it is connected to. In a directed network, the node's in-degree or out-degree can also be used "
                "to determine its influence.")
        st.write("Let's consider a small social network with 5 nodes:")

        # Create a sample graph for demonstration
        G = nx.erdos_renyi_graph(5, 0.5)
        influencer_node = find_influencer_node(G)

        # Display the sample graph
        fig, ax = plt.subplots()
        nx.draw(G, with_labels=True, ax=ax)
        st.pyplot(fig)

        st.write("In this example, node", influencer_node, "is the influencer node.")

    # Explanation of network measures
    def network_measures_explanation():
        st.write("Network measures are metrics used to analyze the structural properties of a network. "
                "Some commonly used network measures include:")
        st.markdown("- **Degree Centrality**: It measures the fraction of nodes a node is connected to. "
                    "The formula for degree centrality of a node `v` in an undirected graph is: "
                    "`degree_centrality(v) = deg(v) / (n-1)` where `deg(v)` is the degree of node `v` and `n` is "
                    "the total number of nodes in the network.")
        st.markdown("- **Closeness Centrality**: It measures how close a node is to all other nodes in the network. "
                    "The formula for closeness centrality of a node `v` is: "
                    "`closeness_centrality(v) = (n-1) / Σ d(v, u)` where `d(v, u)` is the shortest path distance "
                    "between nodes `v` and `u`, and `n` is the total number of nodes in the network.")
        st.markdown("- **Betweenness Centrality**: It measures the fraction of shortest paths that pass through a node. "
                    "The formula for betweenness centrality of a node `v` is: "
                    "`betweenness_centrality(v) = Σ σ(s, t|v) / σ(s, t)` where `σ(s, t)` is the number of shortest paths "
                    "between nodes `s` and `t`, and `σ(s, t|v)` is the number of those paths that pass through node `v`.")
        
        # Create a sample graph for demonstration
        G = nx.erdos_renyi_graph(5, 0.5)
        degree_centrality, closeness_centrality, betweenness_centrality = calculate_network_measures(G)

        # Display the sample graph
        fig, ax = plt.subplots()
        nx.draw(G, with_labels=True, ax=ax)
        st.pyplot(fig)

        st.write("Now, let's calculate the network measures for this example:")

        st.subheader("Degree Centrality:")
        st.write("Degree Centrality for each node:")
        st.write(degree_centrality)

        st.subheader("Closeness Centrality:")
        st.write("Closeness Centrality for each node:")
        st.write(closeness_centrality)

        st.subheader("Betweenness Centrality:")
        st.write("Betweenness Centrality for each node:")
        st.write(betweenness_centrality)

    # User guide
    def user_guide():
        st.write("Welcome to the Virtual Lab for Social Network Analysis!")
        st.write("This virtual lab allows you to generate random social networks and analyze their properties.")
        st.write("Here's how to use the lab:")
        st.markdown("1. **Generate Social Network Tab**: Adjust the parameters on the sidebar to specify the number of nodes and the probability of edge creation. Click on the 'Generate Social Network' button to generate the social network graph.")
        st.markdown("2. **Influencer Nodes Tab**: Learn about influencer nodes in social networks and how they are identified.")
        st.markdown("3. **Network Measures Tab**: Understand the various network measures used to analyze social networks, including degree centrality, closeness centrality, and betweenness centrality.")
        st.markdown("4. **User Guide Tab**: You're here! This page provides information on how to use the virtual lab for social network analysis.")
        st.write("Enjoy exploring social networks with the virtual lab!")

    
    st.title('Social Network Analysis in Graphs')
    # Sidebar inputs
    st.sidebar.subheader('Navigation')
    tab_selection = st.sidebar.selectbox('Go to:', ['User Guide', 'Influencer Nodes', 'Network Measures', 'Social Network'])
    if tab_selection == 'User Guide':
        st.sidebar.markdown('---')
        st.sidebar.subheader('User Guide')
        user_guide()
    elif tab_selection == 'Social Network':
        st.sidebar.markdown('---')
        st.sidebar.subheader('Generate Social Network')
        num_nodes = st.sidebar.number_input('Number of Nodes', min_value=1, value=10)
        probability = st.sidebar.slider('Probability', min_value=0.0, max_value=1.0, value=0.1, step=0.01)
        # Generate social network
        G = create_random_social_network(num_nodes, probability)
        influencer_node = find_influencer_node(G)
        degree_centrality, closeness_centrality, betweenness_centrality = calculate_network_measures(G)
        # Display network measures
        st.subheader('Social Network')
        st.write(f'Influencer Node: {influencer_node}')
        st.write('Degree Centrality:', degree_centrality)
        st.write('Closeness Centrality:', closeness_centrality)
        st.write('Betweenness Centrality:', betweenness_centrality)
        # Draw the network graph
        fig, ax = plt.subplots()
        nx.draw(G, with_labels=True, ax=ax)
        st.pyplot(fig)
    elif tab_selection == 'Influencer Nodes':
        st.sidebar.markdown('---')
        st.sidebar.subheader('Influencer Nodes Explanation')
        influencer_node_explanation()
    elif tab_selection == 'Network Measures':
        st.sidebar.markdown('---')
        st.sidebar.subheader('Network Measures Explanation')
        network_measures_explanation()