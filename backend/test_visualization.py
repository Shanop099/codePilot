from app.services.chat_service import ChatService
from app.visualization.graph_visualizer import GraphVisualizer

print("Creating ChatService...")
chat = ChatService()

print("Creating Visualizer...")
visualizer = GraphVisualizer(
    chat.call_graph
)

print("Building Graph...")
file_path = visualizer.build_graph(
    "add_url_rule"
)

print("Generated:", file_path)