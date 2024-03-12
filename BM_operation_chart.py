import graphviz

# Create a Digraph object
dot = graphviz.Digraph(comment='Balancing Mechanism Operation')

# Define nodes and edges with additional details
dot.node('A', 'Continuous Auction\nThousands of trades daily\n30-minute trading periods')
dot.node('B', 'Decision Making\nReview technical parameters\nEfficient bids and offers accepted')
dot.node('C', 'Continuous Monitoring\nReview BM data, bids, and offers\n24/7 instructions for balance')
dot.node('D', 'Wider Access\nExplore BM guidance document library')

# Define edges using pairs of nodes
dot.edges([('A', 'B'), ('B', 'C'), ('C', 'D')])

# Save the flow chart as a PNG file
dot.render('balancing_mechanism_flow_chart', format='png', cleanup=True)
