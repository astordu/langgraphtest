from agent.researcher import graph
import os
from langfuse.langchain import CallbackHandler

 

os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-e534064f-16e1-4229-9cb8-c9d84de5333b" 
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-3ef7ca50-55c4-4162-86ef-fd56431afa77" 
os.environ["LANGFUSE_HOST"] = "http://localhost:3001" # 🇪🇺 EU region
# os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com" # 🇺🇸 US region
 

# Initialize Langfuse CallbackHandler for Langchain (tracing)
langfuse_handler = CallbackHandler()


#  from langfuse import get_client
# langfuse = get_client()
# 通过注释的代码，可以验证langfuse是否连接成功
# if langfuse.auth_check():
#     print("Langfuse client is authenticated and ready!")
# else:
#     print("Authentication failed. Please check your credentials and host.")




def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config={"callbacks": [langfuse_handler]}):
        for node_name, value in event.items():
            print(f"Node: {node_name}")
            print(f"Value: {value}")
            
            # 安全地处理不同的状态格式
            if "messages" in value and value["messages"]:
                last_message = value["messages"][-1]
                if hasattr(last_message, 'content'):
                    print("Assistant:", last_message.content)
                elif isinstance(last_message, dict) and 'content' in last_message:
                    print("Assistant:", last_message['content'])
            elif "summary" in value:
                print("Summary:", value["summary"])
            print("-" * 50)

if __name__ == "__main__":
    stream_graph_updates("python是什么")