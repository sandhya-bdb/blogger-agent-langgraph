import uvicorn
from fastapi import FastAPI, Request, HTTPException
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM

app = FastAPI()


@app.post("/blogs")
async def create_blogs(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    topic = data.get("topic")
    language = data.get("current_language")

    if not topic:
        raise HTTPException(status_code=400, detail="`topic` is required")

    llm = GroqLLM().get_llm()
    graph_builder = GraphBuilder(llm)

   
    if language:
        graph = graph_builder.build_language_graph()
        result = graph.invoke({
            "topic": topic,
            "current_language": language.lower()
        })
    else:
        graph = graph_builder.build_topic_graph()
        result = graph.invoke({
            "topic": topic
        })

    return {"data": result}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
