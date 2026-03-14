import json
import boto3
from langchain_aws import ChatBedrockConverse # Use this for newer Mistral models
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# 1. Define State for LangGraph
class State(TypedDict):
    messages: Annotated[list, add_messages]

def lambda_handler(event, context):
    try:
        # 2. Initialize Model using ChatBedrockConverse
        # This wrapper automatically formats the 'messages' field for Bedrock
        llm = ChatBedrockConverse(
            model_id="mistral.ministral-3-3b-instruct", 
            region_name="ap-south-1", # Replace with your region
            max_tokens=512,
            temperature=0.7
        )

        # 3. Simple LangGraph Definition
        workflow = StateGraph(State)
        
        def chatbot(state: State):
            response = llm.invoke(state["messages"])
            return {"messages": [response]}

        workflow.add_node("chatbot", chatbot)
        workflow.add_edge(START, "chatbot")
        workflow.add_edge("chatbot", END)
        
        app = workflow.compile()

        # 4. Input Parsing
        body = event.get("body", "{}")
        if isinstance(body, str):
            body = json.loads(body)
            
        user_input = body.get("message", event.get("message", "Hello!"))
        inputs = {"messages": [("user", user_input)]}
        
        # 5. Execute
        result = app.invoke(inputs)

        # 6. Extract the string content
        final_text = result["messages"][-1].content

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'response': final_text,
                'status': 'success'
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
