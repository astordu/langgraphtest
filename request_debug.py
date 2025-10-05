from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
import json
from langchain_core.messages import HumanMessage
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

class DebugCallbackHandler(BaseCallbackHandler):
    """自定义回调处理器，用于查看发送给模型的请求"""
    
    def on_llm_start(self, serialized, prompts, **kwargs):
        """当 LLM 开始调用时触发"""
        print("\n" + "="*60)
        print("🚀 LLM 调用开始")
        print("="*60)
        
        print("\n📝 发送的提示词:")
        for i, prompt in enumerate(prompts):
            print(f"\n--- 提示词 {i+1} ---")
            print(prompt)
        
        print("\n🔧 工具定义:")
        if 'tools' in kwargs:
            tools_info = kwargs['tools']
            for tool_info in tools_info:
                print(f"- 工具名: {tool_info.get('name', 'Unknown')}")
                print(f"  描述: {tool_info.get('description', 'No description')}")
                if 'parameters' in tool_info:
                    print(f"  参数: {json.dumps(tool_info['parameters'], indent=2, ensure_ascii=False)}")
        
        print("\n📊 其他参数:")
        for key, value in kwargs.items():
            if key != 'tools' and key != 'prompt':
                print(f"  {key}: {value}")
    
    def on_llm_end(self, response: LLMResult, **kwargs):
        """当 LLM 调用结束时触发"""
        print("\n" + "="*60)
        print("✅ LLM 调用结束")
        print("="*60)
        
        for generation in response.generations:
            for gen in generation:
                print(f"\n🤖 模型回复:")
                print(f"内容: {gen.text}")
                
                if hasattr(gen, 'message') and hasattr(gen.message, 'tool_calls'):
                    if gen.message.tool_calls:
                        print(f"\n🔨 工具调用:")
                        for tool_call in gen.message.tool_calls:
                            print(f"  工具: {tool_call['name']}")
                            print(f"  参数: {tool_call['args']}")
                            print(f"  ID: {tool_call['id']}")

@tool(return_direct=True)
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def debug_with_callback():
    """使用回调处理器调试"""
    print("=== 创建带回调的 Agent ===")
    
    # 创建回调处理器
    debug_handler = DebugCallbackHandler()
    
    # 创建 agent
    agent = create_react_agent(
        model="deepseek:deepseek-chat",
        tools=[add]
    )
    
    print("\n=== 发送请求 ===")
    result = agent.invoke(
        {"messages": [HumanMessage(content="what's 3 + 5?")]},
        config={"callbacks": [debug_handler]}
    )
    
    print("\n=== 最终结果 ===")
    print(json.dumps({
        "messages": [
            {
                "type": type(msg).__name__,
                "content": msg.content if hasattr(msg, 'content') else str(msg)
            } for msg in result["messages"]
        ]
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    debug_with_callback()
