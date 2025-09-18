from __future__ import annotations
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.tools import FunctionTool
from dotenv import load_dotenv
import os
from typing import AsyncGenerator, Dict, List
import arxiv


load_dotenv()
api_key = os.getenv("OPEN_API")


model_client = OpenAIChatCompletionClient(model="gpt-5-nano", api_key=api_key) 

#Tool Definition

def arxiv_search(query: str, max_results: int = 5) -> List[Dict]:
    client = arxiv.Client()
    search = arxiv.Search(
        query= query,
        max_results= max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers: List[Dict] = []

    for result in client.results(search):
        papers.append(
            {
                "title" : result.title,
                "authors" : [a.name for a in result.authors],
                "published": result.published.strftime("%Y-%m-%d"),
                "summary" : result.summary,
                "pdf_url": result.pdf_url
            }
        )
    return papers

arxiv_tool = FunctionTool(
    arxiv_search,
    description=(
        "Searches arXiv and returns up to *max_results* papers, each containing"
        "title, authors, publication date, abstract, and pdf_url."
    ),
)


#Agent And team building

def build_team(model: str = "gpt-5-nano") -> RoundRobinGroupChat:
    search_agent = AssistantAgent(
        name = "Search_Agent",
        model_client= model_client,
        description="Crafts arXiv queries and retrieves candidate papers.",
        system_message=(
            "Given a user topic, think of the best arXiv query and call the "
            "provided tool. Always fetch five‑times the papers requested so "
            "that you can down‑select the most relevant ones. When the tool "
            "returns, choose exactly the number of papers requested and pass "
            "them as concise JSON to the summarizer."
        ),
        tools=[arxiv_tool],
        reflect_on_tool_use= True
    )

    summarizer = AssistantAgent(
        name = "Summarizer",
        model_client= model_client,
        description = "Produce a short Markdown review from provided papers.",
         system_message=(
            "You are an expert researcher. When you receive the JSON list of "
            "papers, write a literature‑review style report in Markdown:\n" \
            "1. Start with a 2–3 sentence introduction of the topic.\n" \
            "2. Then include one bullet per paper with: title (as Markdown "
            "link), authors, the specific problem tackled, and its key "
            "contribution.\n" \
            "3. Close with a single‑sentence takeaway."
        ),  
    )

    return RoundRobinGroupChat(
        participants=[search_agent, summarizer],
        max_turns= 2
    )


#Orchestrator

async def run_litrev(
    topic: str,
    num_papers: int = 5,
    model: str = "gpt-5-nano"
) -> AsyncGenerator[str, None]:
    team = build_team(model = model)
    task_prompt = (
        f"Conduct a literature review on **{topic}** and return excatly {num_papers} papers "
    )

    async for msg in team.run_stream(task = task_prompt):
        if isinstance(msg, TextMessage):
            yield f"{msg.source}: {msg.content}\n\n"

#CLI TESTING

if __name__ == "__main__":
    async def _demo() -> None:
        async for line in run_litrev("Artificial Intelligence", num_papers=5):
            print(line)

    asyncio.run(_demo()) 
