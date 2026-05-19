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
            media_url = upload_result["publicUrl"]
            media_urls.append(media_url)
            print(f"Media uploaded successfully: {media_url}")
        
        # Create post with text and media
        response = client.posts.create(
            content=content,
            media_urls=media_urls if media_urls else None,  # Only add if we have media
            platforms=[
                {
                    "platform": "threads",
                    "accountId": "6a010d4d92b3d8e85fb919dc"
                }
            ],
            publish_now=True,
        )

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
    
    # Test with image (uncomment and add your test image path)
    # result_with_image = post("Check out this image!", image_path="test_image.jpg")
    # print("\n--- Image Post Result ---")
    # print(f"Success: {result_with_image['success']}")
    # print(f"Has Media: {result_with_image['has_media']}")