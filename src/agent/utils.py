"""Utility functions and helpers for the Deep Research agent."""

import os
import asyncio
from typing import Literal
from langchain_core.tools import (
    tool,
)
from tavily import AsyncTavilyClient

##########################
# Tavily Search Tool Utils
##########################
@tool
def tavily_search(
    search_queries: list[str], 
    max_results: int = 5, 
    topic: Literal["general", "news", "finance"] = "general", 
    include_raw_content: bool = True
):
    """
    一个搜索引擎，用于收集与用户输入主题相关的信息。
    在需要回答关于当前事件的问题时非常有用。
    
    Args:
        search_queries: 要执行的搜索查询列表,最多5个,输入是中文的查询内容
        max_results: 每个查询返回的最大结果数
        topic: 搜索结果的主题过滤器 (general, news, or finance)
        include_raw_content: 是否包含完整的网页内容
        
    Returns:
        List of search result dictionaries from Tavily API
    """
    async def _tavily_search():
        # Initialize the Tavily client with API key from config
        tavily_client = AsyncTavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        # Create search tasks for parallel execution
        search_tasks = [
            tavily_client.search(
                query,
                max_results=max_results,
                include_raw_content=include_raw_content,
                topic=topic
            )
            for query in search_queries
        ]
        
        return await asyncio.gather(*search_tasks)

    search_results = asyncio.run(_tavily_search())

    format_msg_res = ""
    # search_results 是一个列表，每个元素是一个搜索结果的字典
    for result_set in search_results:
        for result in result_set.get('results', []):
            format_msg_res += "标题:" + result['title'] + "\n" + "内容:" + result['content'] + "\n\n"
    
    return format_msg_res
    

    

##########################
# Reflection Tool Utils
##########################

@tool
def think_tool(reflection: str) -> str:
    """用于研究进展与决策的战略反思工具.

    在每次搜索后使用此工具分析结果并系统地规划下一步步骤。
    这为研究工作流创建了一个有意的暂停，以进行质量决策。

    何时使用:
    - 在收到搜索结果后: 我找到了哪些关键信息?
    - 在决定下一步步骤前: 我是否有足够的信息来全面回答?
    - 在评估研究差距时: 我仍然缺少哪些具体信息?
    - 在总结研究前: 我是否可以现在提供一个完整的答案?

    应该考虑:
    1. 当前发现的分析 - 我收集了哪些具体信息?
    2. 差距评估 - 我仍然缺少哪些关键信息?
    3. 质量评估 - 我是否有足够的证据/例子来提供一个完整的答案?
    4. 战略决策 - 我应该继续搜索还是提供我的答案?

    Args:
        reflection: 你对研究进展、发现、差距和下一步步骤的详细反思

    Returns:
        确认反思已记录以进行决策
    """
    return f"Reflection recorded: {reflection}"



# 测试代码（可选）
# 取消注释下面的代码来测试 Tavily 搜索功能
if __name__ == "__main__":
    # a = tavily_search.invoke({
    #     "search_queries": ["什么是python"],
    #     "max_results": 5, 
    #     "topic": "general", 
    #     "include_raw_content": True
    # })
    # print(a)

    print(tavily_search.description)
    print(tavily_search.args_schema.model_json_schema())
    # print(think_tool.args_schema.model_json_schema())
