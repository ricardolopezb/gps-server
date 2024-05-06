import xml.etree.ElementTree as ET
from gps.graph.node import Node


class XmlNodeMapReader:
    @staticmethod
    def read(file_path):
        nodes = {}
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Namespace dictionary for XPath queries
        ns = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}

        # Find all nodes in the graph
        for node in root.findall('.//graphml:node', ns):
            node_id = node.attrib['id']

            # Find x and y coordinates of the node
            x = None
            y = None
            for data in node.findall('.//graphml:data', ns):
                if data.attrib['key'] == 'd0':
                    x = float(data.text)
                elif data.attrib['key'] == 'd1':
                    y = float(data.text)

            if x is not None and y is not None:
                nodes[node_id] = Node(node_id, x, y)

        # Find all edges in the graph and add successors to nodes
        for edge in root.findall('.//graphml:edge', ns):
            source_id = edge.attrib['source']
            target_id = edge.attrib['target']

            # Add target node as successor to source node
            if source_id in nodes and target_id in nodes:
                source_node = nodes[source_id]
                target_node = nodes[target_id]
                source_node.add_neighbor(target_node)

        return list(nodes.values())

xml_reader = XmlNodeMapReader()
nodes = xml_reader.read('xml_node_map.xml')
for node in nodes:
    print(f"Node {node.id}: x={node.x}, y={node.y}, Neighbors: {[neighbor.id for neighbor in node.neighbors]}")