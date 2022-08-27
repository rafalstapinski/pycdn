from io import BytesIO

import httpx
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from PIL.Image import Image as PILImage
from PIL.Image import open as pil_open

app = FastAPI()

MEMORY: dict[str, PILImage] = {}


@app.get("/")
async def get_resource(image_url: str):

    if image_url in MEMORY:
        print("GOT CACHE")
        image = MEMORY[image_url]

    else:
        print("GOT NETWORK")
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)

            image = bytes_to_pil_image(
                response.content,
            )

            MEMORY[image_url] = image

    return StreamingResponse(pil_image_to_bytes_io(image, format="jpeg", quality=95), media_type="image/jpeg")


def pil_image_to_bytes_io(image: PILImage, format: str = "jpeg", **pil_save_params) -> bytes:
    buffer = BytesIO()
    image.convert("RGB").save(buffer, format=format, **pil_save_params)
    buffer.seek(0)
    return buffer


def bytes_to_pil_image(im_bytes: bytes) -> PILImage:
    return pil_open(BytesIO(im_bytes))
