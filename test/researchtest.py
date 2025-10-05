from agent.researcher import graph


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
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