from langgraph.graph import StateGraph, START, END
from src.nodes.blog_node import BlogNode
from src.states.blogstate import BlogState


class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)

    def build_language_graph(self):
        blog_node = BlogNode(self.llm)

       
        self.graph.add_node("title_creation", blog_node.title_creation)
        self.graph.add_node("content_generation", blog_node.content_generation)

        self.graph.add_node(
            "hindi_translation",
            lambda s: blog_node.translation({**s, "current_language": "hindi"})
        )

        self.graph.add_node(
            "french_translation",
            lambda s: blog_node.translation({**s, "current_language": "french"})
        )

        self.graph.add_node(
            "assamese_translation",
            lambda s: blog_node.translation({**s, "current_language": "assamese"})
        )

        self.graph.add_node("route", blog_node.route)

        
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "route")

        self.graph.add_conditional_edges(
            "route",
            blog_node.route_decision,
            {
                "hindi": "hindi_translation",
                "french": "french_translation",
                "assamese": "assamese_translation"
            }
        )

        self.graph.add_edge("hindi_translation", END)
        self.graph.add_edge("french_translation", END)
        self.graph.add_edge("assamese_translation", END)

        return self.graph.compile()



from src.llms.groqllm import GroqLLM

llm = GroqLLM().get_llm()
builder = GraphBuilder(llm)

graph = builder.build_language_graph()
