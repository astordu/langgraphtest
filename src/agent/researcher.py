from typing import Annotated
from langchain_core.messages import HumanMessage
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from agent.utils import tavily_search,think_tool
from langchain.chat_models import init_chat_model
from agent.prompts import researcher_system_prompt
from agent.prompts import summarize_webpage_prompt


class State(TypedDict):
    messages: Annotated[list, add_messages]
    summary: str = "",
    search_data: str = "",


llm = init_chat_model("deepseek:deepseek-chat")

tools = [tavily_search,think_tool]
llm_with_tools = llm.bind_tools(tools)


def search_node(state: State):
    # 构建包含system prompt的消息列表
    messages = [{"role": "system", "content": researcher_system_prompt}] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def compase_node(state: State):
    
    summary_llm = init_chat_model("deepseek:deepseek-chat")
    summary = summary_llm.invoke([HumanMessage(content=summarize_webpage_prompt.format(webpage_content=state["search_data"]))])

    return {"summary":summary}

graph_builder = StateGraph(State)

graph_builder.add_node("search_node", search_node)
graph_builder.add_node("tools", ToolNode(tools=tools))
graph_builder.add_node("compase_node", compase_node)

graph_builder.add_conditional_edges(
    "search_node",
    tools_condition,
    {"tools": "tools", "__end__": "compase_node"}
)

# 工具调用后回到 search_node 继续决策
graph_builder.add_edge("tools", "search_node")
graph_builder.add_edge("compase_node", END)
graph_builder.add_edge(START, "search_node")
graph = graph_builder.compile()


"""
{
  "messages": [
    {"role": "user", "content": "谁赢得了2020年的世界职业棒球大赛?"}
  ]
}
"""