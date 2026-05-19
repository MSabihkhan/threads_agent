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

def post(content: str, image_path: str = None) -> dict:
    try:
        media_urls = []
        
        # If image is provided, upload it first to get public URL
        if image_path and os.path.exists(image_path):
            print(f"Uploading media: {image_path}")
            upload_result = client.media.upload(image_path)
            
            # Convert SDK response object to dict if needed
            if hasattr(upload_result, 'model_dump'):
                upload_dict = upload_result.model_dump()
            elif hasattr(upload_result, '__dict__'):
                upload_dict = upload_result.__dict__
            else:
                upload_dict = upload_result
            
            # Extract public URL
            media_url = upload_dict.get("publicUrl") or upload_dict.get("public_url") or upload_dict.get("url")
            
            if media_url:
                media_urls.append(media_url)
                print(f"Media uploaded successfully: {media_url}")
            else:
                print(f"Warning: Could not extract media URL from upload response: {upload_dict}")
        
        # Create post with text and media
        post_params = {
            "content": content,
            "platforms": [
                {
                    "platform": "threads",
                    "accountId": "6a010d4d92b3d8e85fb919dc"
                }
            ],
            "publish_now": True,
        }
        
        # Only add media_urls if we have any
        if media_urls:
            post_params["media_urls"] = media_urls
        
        response = client.posts.create(**post_params)

        # Safely convert the SDK response object into a dictionary
        response_dict = response.model_dump()
        post_data = response_dict.get("post", {})

        return {
            "success": True,
            "id": post_data.get("id") or response_dict.get("id"),
            "status": post_data.get("status", "unknown"),
            "platforms_count": len(post_data.get("platforms", [])),
            "has_media": len(media_urls) > 0
        }

    except Exception as e:
        # Print full error for debugging
        import traceback
        print(f"Error details: {traceback.format_exc()}")
        
        return {
            "success": False,
            "status": "failed",
            "error": str(e)
        }

if __name__ == "__main__":    
    # Test with text only
    result = post("Hello world from Zernio!")
    print("--- Text Post Result ---")
    print(f"Success: {result['success']}")
    print(f"Status: {result['status']}")
    if not result['success']:
        print(f"Error: {result['error']}")