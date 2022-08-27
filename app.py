from io import BytesIO

import httpx
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from PIL.Image import Image as PILImage
from PIL.Image import open as pil_open

app = FastAPI()

MEMORY: dict[str, BytesIO] = {}


@app.get("/")
async def get_resource(image_url: str):

    if image_url in MEMORY:
        print("GOT CACHE")
        buffer = MEMORY[image_url]

    else:
        print("GOT NETWORK")
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)

            image = pil_open(BytesIO(response.content))
            image = image.convert("RGB")
            buffer = BytesIO()
            image.save(buffer, format="jpeg", quality=80)

            MEMORY[image_url] = buffer

    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/jpeg")
