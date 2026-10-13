import os
import aiohttp
from youtubesearchpython import VideosSearch
from config import YOUTUBE_IMG_URL


async def get_thumb(
    videoid,
    progress_percent=0,
    use_cache=True,
    user_name="AxiomUser",
):
    try:
        os.makedirs("cache", exist_ok=True)

        thumb_path = f"cache/thumb_{videoid}.jpg"
        thumbnail_url = f"https://img.youtube.com/vi/{videoid}/maxresdefault.jpg"

        async with aiohttp.ClientSession() as session:
            async with session.get(
                thumbnail_url,
                timeout=aiohttp.ClientTimeout(total=20),
            ) as response:
                if response.status != 200:
                    return YOUTUBE_IMG_URL

                content_type = response.headers.get(
                    "Content-Type", ""
                )
                if not content_type.startswith("image/"):
                    return YOUTUBE_IMG_URL

                image_data = await response.read()

                if not image_data:
                    return YOUTUBE_IMG_URL

                with open(thumb_path, "wb") as file:
                    file.write(image_data)

        return thumb_path

    except Exception as e:
        print(f"Thumbnail error: {e}")
        return YOUTUBE_IMG_URL
