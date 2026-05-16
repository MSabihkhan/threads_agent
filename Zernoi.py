import requests
import dotenv
import os
from zernio import Zernio
dotenv.load_dotenv()

client = Zernio(
    api_key=os.getenv("ZERNIO_API_KEY"),
    base_url="https://zernio.com/api",
    timeout=30.0,
)

def post(content: str) -> dict:
    try:
        # Publish to multiple platforms with one call
        response = client.posts.create(
            content=content,
            platforms=[
                {
                    "platform": "threads",
                    "accountId": "6a010d4d92b3d8e85fb919dc"
                }
            ],
            publish_now=True,
        )

        # Safely convert the SDK response object into a standard Python dictionary
        # This prevents any "AttributeError" exceptions from strict typing
        response_dict = response.model_dump()

        # Extract the inner post data
        # Zernio wraps the post data inside a 'post' key in the payload dictionary
        post_data = response_dict.get("post", {})

        return {
            "success": True,
            "id": post_data.get("id") or response_dict.get("id"), # Check both places for ID
            "status": post_data.get("status", "unknown"),
            "platforms_count": len(post_data.get("platforms", []))
        }

    except Exception as e:
        # Handle API errors or connection failures gracefully
        return {
            "success": False,
            "status": "failed",
            "error": str(e)
        }

if __name__ == "__main__":    
    result = post("Hello worlddddd again from Zernio!")
    
    print("--- Post Result ---")
    print(f"Was successful?: {result['success']}")
    print(f"Current Status: {result['status']}")
    
    if result['success']:
        print(f"Post ID: {result['id']}")
    else:
        print(f"Error Message: {result['error']}")