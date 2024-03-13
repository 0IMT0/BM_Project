from graphviz import Digraph

def create_flowchart():
    # Create a directed graph
    flowchart = Digraph('Flowchart', format='png')

    # Define nodes and edges
    flowchart.node('A', 'Start')
    flowchart.node('B', 'Step 1')
    flowchart.node('C', 'Step 2')
    flowchart.node('D', 'End')

    flowchart.edges(['AB', 'BC', 'CD'])

    # Save the graph to a file
    flowchart.render('flowchart', format='png', cleanup=True)

if __name__ == "__main__":
    create_flowchart()

create_flowchart()