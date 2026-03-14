
import json
import boto3
from langchain_aws import ChatBedrockConverse
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

# 1. Define the Printing Tool
@tool
def print_input_tool(user_text: str) -> str:
    """Useful for logging or printing the user input exactly as received."""
    print(f"--- TOOL EXECUTION LOG: {user_text} ---")
    return f"Processed and printed: {user_text}"

# 2. Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

def lambda_handler(event, context):
    try:
        # 3. Initialize Model and Bind Tool
        llm = ChatBedrockConverse(
            model_id="mistral.ministral-3-3b-instruct", 
            region_name="ap-south-1", # Replace with your region
            max_tokens=512,
            temperature=0.7
        )
        
        # Bind the tool so the model knows it exists
        tools = [print_input_tool]
        llm_with_tools = llm.bind_tools(tools)

        # 4. Build the Graph
        workflow = StateGraph(State)
        
        def chatbot(state: State):
            # Model decides if it needs to call the print_input_tool
            return {"messages": [llm_with_tools.invoke(state["messages"])]}

        # ToolNode handles the actual execution of the tool function
        tool_node = ToolNode(tools)

        workflow.add_node("chatbot", chatbot)
        workflow.add_node("tools", tool_node)

        # Logic: Start -> Chatbot -> (if tool call) -> Tools -> Chatbot -> End
        workflow.add_edge(START, "chatbot")
        
        # Conditional edge: check if the model wants to call a tool
        def should_continue(state: State):
            messages = state["messages"]
            last_message = messages[-1]
            if last_message.tool_calls:
                return "tools"
            return END

        workflow.add_conditional_edges("chatbot", should_continue)
        workflow.add_edge("tools", "chatbot")
        
        app = workflow.compile()

        # 5. Execute
        body = event.get("body", "{}")
        if isinstance(body, str):
            body = json.loads(body)
            
        user_input = body.get("message", event.get("message", "Please print 'Venu Goapl Reddy ' using your tool"))
        inputs = {"messages": [("user", user_input)]}
        
        result = app.invoke(inputs)
        final_text = result["messages"][-1].content

        return {
            'statusCode': 200,
            'body': json.dumps({'response': final_text})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
