import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

#Now its all about streamlit app initlaize and showcase
st.set_page_config(page_title="Calories Advisor App")

background_image_url = 'bgimage.png'

# HTML and CSS code to set background image
background_image_code = f"""
<style>
    body {{
        background-image: url("{background_image_url}");
        background-size: cover;
    }}
</style>
"""

# Display background image using st.markdown
st.markdown(background_image_code, unsafe_allow_html=True)

st.header("Calories Advisor App")
uploaded_file=st.file_uploader("Choose an image....",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded_image",use_column_width=True)

submit=st.button("Tell me about the Total Calories")

#the front end done above streamlite me
#the backend done usse bhi above me jaha input bhejnege aur voh response banake bhejega 

#now thr main part how should we say gemini that he is nutrtionist 

input_prompt="""
Yor are an expert Nutritionist where you need to see the food items from image and calculate the total calories,also provide
details of every food item with calories intake 
in below format
            1.Item 1-no.of calories
            2.Item 2-no.of calories
            ........
            ........
Finally you can also mention whether the food is healthy or not and also mention the percentage split of the ratio
of carbs,fats,fibres,sugar and other important things required in our diet."""

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.header("The Response is:")
    st.write(response)