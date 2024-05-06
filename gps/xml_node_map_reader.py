import xml.etree.ElementTree as ET
from gps.graph.node import Node


class XmlNodeMapReader:
    def read(self):
        tree = ET.parse('xml_node_map.xml')
        root = tree.getroot()

        # Define the namespace
        namespace = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}

        # Extract nodes
        nodes = {}
        for node_elem in root.findall('.//graphml:node', namespace):
            node_id = node_elem.attrib['id']
            x = float(node_elem.find('./graphml:data[@key="d0"]', namespace).text)
            y = float(node_elem.find('./graphml:data[@key="d1"]', namespace).text)
            nodes[node_id] = Node(node_id, x, y)

        # Extract edges
        for edge_elem in root.findall('.//graphml:edge', namespace):
            source_id = edge_elem.attrib['source']
            target_id = edge_elem.attrib['target']
            nodes[source_id].add_neighbor(nodes[target_id])

        # Add default edges for consecutive nodes
        node_ids = list(nodes.keys())
        for i in range(len(node_ids) - 1):
            source_id = node_ids[i]
            target_id = node_ids[i + 1]
            if target_id not in nodes[source_id].neighbors:
                nodes[source_id].add_neighbor(nodes[target_id])
        return nodes

    def parse_graphml(self, file_path):
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
#nodes = xml_reader.read()
nodes = xml_reader.parse_graphml('xml_node_map.xml')
for node in nodes:
    print(f"Node {node.id}: x={node.x}, y={node.y}, Neighbors: {[neighbor.id for neighbor in node.neighbors]}")