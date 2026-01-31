from typing import Dict
from src.states.blogstate import BlogState


class BlogNode:
    """
    Blog generation + translation node with router support
    """

    def __init__(self, llm):
        self.llm = llm

  
    def title_creation(self, state: BlogState) -> Dict:
        topic = state.get("topic")

        if not topic:
            return {}

        prompt = f"""
You are an expert blog content writer.
Use Markdown formatting.
Generate a creative and SEO-friendly blog title for:

{topic}
"""

        response = self.llm.invoke(prompt)

        return {
            "blog": {
                "title": response.content
            }
        }

   
    def content_generation(self, state: BlogState) -> Dict:
        topic = state.get("topic")
        title = state.get("blog", {}).get("title")

        if not topic:
            return {}

        prompt = f"""
You are an expert blog writer.
Use Markdown formatting.
Write a detailed blog with headings and a conclusion for:

{topic}
"""

        response = self.llm.invoke(prompt)

        return {
            "blog": {
                "title": title,
                "content": response.content
            }
        }

    
    def translation(self, state: BlogState) -> Dict:
        language = state.get("current_language")
        blog = state.get("blog", {})
        content = blog.get("content")

        if not language or not content:
            return {}

        prompt = f"""
Translate the following content into {language}.
Maintain tone, structure, and Markdown formatting.

CONTENT:
{content}
"""

        response = self.llm.invoke(prompt)

       
        return {
            "blog": {
                "title": blog.get("title"),
                "content": response.content
            }
        }

   
    def route(self, state: BlogState) -> Dict:
        return state

   
    def route_decision(self, state: BlogState) -> str:
        language = state.get("current_language")

        if language == "hindi":
            return "hindi"
        elif language == "french":
            return "french"
        elif language == "assamese":
            return "assamese"
        else:
            return "__end__"