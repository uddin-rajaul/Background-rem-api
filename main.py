from fastapi import FastAPI, File, UploadFile
from rembg import remove
from fastapi.responses import FileResponse
from io import BytesIO
from PIL import Image
import uuid

api = FastAPI()

@api.post('/remove-background')
async def remove_background(file: UploadFile=File(...)):
    # read uploaded image file
    input_image = Image.open(BytesIO(await file.read()))

    #remove bg using rembg
    output_image = remove(input_image, alpha_matting=True, alpha_matting_foreground_threshold=270,alpha_matting_background_threshold=20, alpha_matting_erode_size=11)

    # save file by giving temp name
    output_filename = f"{uuid.uuid4()}.png"

    # save file
    output_image.save(output_filename,format="png")

    # return file response
    return FileResponse(output_filename, media_type='image/png', filename=output_filename)
