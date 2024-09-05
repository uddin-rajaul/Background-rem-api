from urllib import response
import streamlit as st
from io import BytesIO
import requests

api_url = 'http://127.0.0.1:8000/remove-background'


uploaded_file = st.file_uploader("Upload an image:", type= ["jpg","jepg","png"])

if uploaded_file is not None:
    # display uploaded image
    st.image(uploaded_file, caption="Uploaded image", use_column_width=True)
    #prepare for api
    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
    #make a post req to api
    response = requests.post(api_url,files=files)
    st.success("Output")
    # check if req was success
    if response.status_code == 200:
        # display the processed image
        st.image(BytesIO(response.content), caption="Processed image with bg removed", use_column_width=True)
    else:
        st.error(f"Error: {response.status_code}")
