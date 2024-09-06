from fastapi import FastAPI, File, UploadFile
from rembg import remove, new_session
from fastapi.responses import FileResponse, JSONResponse
from io import BytesIO
from PIL import Image
import uuid
import os

api = FastAPI()


model_name = "u2net"
rembg_session = new_session(model_name)

# Get the absolute path for the output directory
output_dir = os.path.join(os.getcwd(), "images")
os.makedirs(output_dir, exist_ok=True)

@api.post('/remove-background')
async def remove_background(files: list[UploadFile]=File(...)):

    output_files = []

    for file in files:
        # save file by giving temp name
        output_filename = os.path.join(output_dir, f"{uuid.uuid4()}.png")

        # read uploaded image file
        input_image = await file.read()

        # Remove background using rembg with the session
        output_image = remove(input_image, session=rembg_session,
                              alpha_matting=True,
                              alpha_matting_foreground_threshold=270,
                              alpha_matting_background_threshold=20,
                              alpha_matting_erode_size=11)
        with open(output_filename, 'wb') as o:
            o.write(output_image)

        output_files.append(output_filename)

    if len(output_files) == 1:
        # return file response
        return FileResponse(output_files[0], media_type='image/png', filename=output_files[0])


    return JSONResponse({"processed_files":  output_files})
