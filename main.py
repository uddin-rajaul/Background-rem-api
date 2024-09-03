from fastapi import FastAPI, File, UploadFile
from rembg import remove
from fastapi.responses import FileResponse
from io import BytesIO
from PIL import Image
import uuid

api = FastAPI()

@api.post('/remove-background')
async def remove_background(file: UploadFile=File(...)):
    input_image = Image.open(BytesIO(await file.read()))

    output_image = remove(input_image)

    output_filename = f"{uuid.uuid4()}.png"
    output_image.save(output_filename,format="png")

    return FileResponse(output_filename, media_type='image/png', filename=output_filename)
