import boto3
import json
from botocore.exceptions import ClientError

# Initialize the client outside the handler for better performance (TCP connection reuse)
client = boto3.client("bedrock-runtime", region_name="us-east-1")

def lambda_handler(event, context):
    # 1. Set the model ID (Claude 3 Haiku)
    model_id = "mistral.devstral-2-123b"

    # 2. Get the prompt from the event, or use a default
    user_prompt = event.get("prompt", "Describe the purpose of a 'hello world' program in one line.")

    # 3. Format the native Anthropic Claude 3 structure
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_prompt}],
            }
        ],
    }

    try:
        # 4. Invoke the model
        response = client.invoke_model(
            modelId=model_id, 
            body=json.dumps(native_request)
        )

        # 5. Decode and parse the response
        model_response = json.loads(response["body"].read())
        

        return {
            'statusCode': 200,
            'body': json.dumps({
                'prompt': user_prompt,
                'completion': model_response
            })
        }

    except ClientError as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
