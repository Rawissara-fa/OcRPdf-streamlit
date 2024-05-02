########################################################################
    # Import library
########################################################################

import cv2
import os
import ast
import json
import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO

import fitz  # PyMuPDF 
import streamlit as st
from datetime import datetime
    
from streamlit_cropper import st_cropper
from streamlit_pdf_viewer import pdf_viewer
# from paddleocr import PaddleOCR
# #, draw_ocr

# import components.ocr2result as ocr2result




########################################################################
    # Set header page
########################################################################

st.set_page_config(page_title="OoCcRr", page_icon=" ", layout="wide")
st.title("ARUNSAWAD")
# st.markdown("_________________________________________________")




########################################################################
    # Set Authenticate in this page
########################################################################

# if st.session_state["login_user"]["Status"] is False:
#     st.warning('Please enter your username and password')
# elif st.session_state["login_user"]["Status"] is True:
#     st.sidebar.write("Welcome: "+st.session_state["login_user"]["TITLE_OF_COURTESY_NAME"] +st.session_state["login_user"]["FIRST_NAME"]+ \
#                     "\n"+ "Department: " + st.session_state["login_user"]["SECTION_NAME"])
#     logout_btn = st.sidebar.button("Logout")
#     if logout_btn:
#         print("User logout")
#         st.session_state["login_user"]["Status"] = False
#         st.rerun()



########################################################################
    # Set addition for use
########################################################################

def get_page_no(pdf_path):
    with fitz.open(pdf_path) as pdf_document:
        return pdf_document.page_count 

def load_dict_from_txt(file_path):
    # Read the contents of the JSON file
        with open(file_path, "r") as file:
            json_str = file.read()

        # Convert the JSON string to a dictionary
        dictionary = json.loads(json_str)
        return dictionary
    
def save_dict_to_txt(dictionary, file_path):
    # Convert the dictionary to a JSON string
        json_str = json.dumps(dictionary, indent=4)  # Indent for better readability

        # Write the JSON string to a text file
        with open(file_path, "w") as file:
            file.write(json_str)
            
def delete_file(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)


def clear_form():
    st.session_state["tab1_01"] = ""
    st.session_state["tab1_01"] = ""
    st.session_state["tab1_02"] = ""
    
    st.session_state["sub1_00"] = ""
    st.session_state["sub1_01"] = ""
    st.session_state["sub1_02"] = ""
    st.session_state["sub1_03"] = ""
    
    # st.session_state["tab2_00"] = ""




    

########################################################################
    # Select image input
    # Tab 1
########################################################################   

current_today = datetime.now()
current_folder = str(current_today).split(".")[0]

        
## file_image by filter 
tab1, tab2, tab3 = st.tabs(["config template", "read doc by one" ,"read doc by group"])

with tab1:   
    
    ## upload file for prepare data -------------------------------------------------  
    
    clear_btn = st.button("clear cache/data", type="secondary")
    if clear_btn:
        folder_path = "input_items/input_PDFfiles"
        files = os.listdir(folder_path)
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(folder_path, file)
                os.remove(file_path)

                
    # Declare variable.
    if 'pdf_ref' not in st.session_state:
        st.session_state["pdf_ref"] = None 
    
    # Access the uploaded ref via a key.
    uploaded_img = st.file_uploader("**:black[Choose a PDF file]**", type=('pdf'), key='pdf', accept_multiple_files=False) # , key="tab1_00")

    if st.session_state["pdf_ref"]:
        st.session_state["pdf_ref"] = st.session_state["pdf_ref"]  # backup

    # Now you can access "pdf_ref" anywhere in your app.
    if st.session_state["pdf_ref"]:
        binary_data = st.session_state["pdf_ref"].pdf_ref.getvalue()
        pdf_viewer(input=binary_data, width=700) 
            
    if uploaded_img is not None:   
        save_image_path = './input_items/input_PDFfiles/' + uploaded_img.name
        with open(save_image_path, "wb") as f:
            f.write(uploaded_img.read()) 
        file_path_to_img = 'input_items/input_PDFfiles/' + uploaded_img.name 
        
        
        pdf_doc = fitz.open(file_path_to_img)
        num_pages = get_page_no(file_path_to_img)

    
                        
        # ## crop for select detail into box -------------------------------------------------
        # selected_pages = st.toggle('Selected pages' , key="tab1_00")
        # if selected_pages:
            
        #     if num_pages is not None:

        #         # ## created table prepare fill position -------------------------------------------------
        #         # cols1HT1, cols1HT2, cols1HT3 = st.columns([1, 1, 2])                 
        #         # with cols1HT1:
        #         #     rows = st.number_input("row:", min_value=0, step=1, key="sub1_01")  
        #         # with cols1HT2:
        #         #     columns = st.number_input("column:", min_value=0, step=1, key="sub1_02")


        #         # # Boolean to resize the dataframe, stored as a session state variable
        #         # # st.checkbox("Use container width", value=False, key="use_container_width")
        #         # data = {'Column {}'.format(i+1): [' '] * columns for i in range(rows)}
        #         # edited_df = st.data_editor(pd.DataFrame(data))
                    
                        
        #         # ## crop for select detail into box -------------------------------------------------
                
        #         headfile_menu = st.columns((1, 1))
        #         with headfile_menu[1]:
        #             selected_page = st.selectbox("**:black[Select page for use :]**", range(1, num_pages + 1), index=0)
        #             page = pdf_doc[selected_page - 1]
                    
        
        #             # Get image bytes from the page
        #             pixmap = page.get_pixmap()
        #             img_array = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape((pixmap.height, pixmap.width, pixmap.n))
                    
        #             # Rotate the page by the calculated rotation angle
        #             rotation_angle = ocr2result.calculate_rotation_angle(img_array)
        #             if rotation_angle is not None :
        #                 inclination_dgree = rotation_angle
        #             else:
        #                 inclination_dgree = 0
        #             rotated_back_image = Image.fromarray(cv2.warpAffine(img_array, 
        #                                                                 cv2.getRotationMatrix2D((pixmap.width // 2, pixmap.height // 2), 
        #                                                                                     inclination_dgree-90.05, 1), (pixmap.width, pixmap.height)))

        #             # Save the image to BytesIO buffer
        #             img_bytes_io = BytesIO()
        #             rotated_back_image.save(img_bytes_io, format="PNG")
        #             img_bytes = img_bytes_io.getvalue()

        #             ## Display the image
        #             # st.image(img_bytes, caption=f"page {selected_page}/{num_pages}")
                
        #         with headfile_menu[0]:
        #             st.markdown(f"Page **{selected_page}** of **{num_pages}** ")
            
            
        #     ## display image after fill file -------------------------------------------------
            
        #     cols1H0, cols1H3 = st.columns(2)           
        #     # box_color = st.color_picker(label="Box Color", value='#0000FF')
        #     aspect_ratio = (1, 1) #None    
        #     with cols1H3: 
        #         # Load the image and resize to be no wider than the streamlit widget size
        #         box = st_cropper(rotated_back_image, realtime_update = True, box_color = '#4800FF', aspect_ratio= aspect_ratio, return_type = 'box')
        #         crop_arg = (box['left'],               box['top'],
        #                     box['width']+ box['left'], box['height']+ box['top'])
                
        #     with cols1H0:
        #         cols1H1, cols1H2 = st.columns([1, 2]) 
        #         with cols1H2: 
        #             cropped_image = rotated_back_image.crop(crop_arg)  
        #             # st.markdown("**:blue[preview image]**")          
        #             _ = cropped_image.thumbnail((1080,1080))
        #             st.image(cropped_image, caption= "preview image")


        #         with cols1H1:      
        #             read_btn = st.button("preview read", type="primary")
        #             if read_btn:
        #                 # posi_btn = st.button("position save", type="primary")
        #                 clear_btn = st.button("clear image", type="secondary")
        #                 if cropped_image is not None:
        #                     preview_path = 'input_items/input_image/preview.jpg' 
        #                     cv2.imwrite(preview_path, np.array(cropped_image))
                    
        #                 ocr = PaddleOCR(lang='en')
        #                 preview = ocr.ocr((preview_path), cls=False)
                
                        
                    
        #         data = [] 
        #         if read_btn:
        #             with cols1H2:
        #                 st.text("--------------------------")
        #                 posi_ROI = crop_arg
        #                 st.text(f"position: {posi_ROI}")
                        
        #                 for line in preview[0]:
        #                     st.text(line[1][0])
        #                     # data.append([text,       score,      position])
        #                     # data.append([line[1][0], line[1][1], line[0]])
            
                            
        #                 ## clear image --------------------------------------------------
                        
        #                 if clear_btn:
        #                     folder_path = "input_items/input_image"
        #                     files = os.listdir(folder_path)
        #                     for file in files:
        #                         if file.endswith(".jpg"):
        #                             file_path = os.path.join(folder_path, file)
        #                             os.remove(file_path)


                
        # else:
        #     st.info("wait input document file")   
    
    # else:
    #     pass  
          
        
    ## created table prepare fill position -------------------------------------------------
    
    file_path = "updated_dictionary.txt"    
    cols1HT1, cols1HT2, cols1HT3, cols1HT4 = st.columns([1, 1, 1, 1])                 
    with cols1HT1:
        columns = st.number_input("column:", min_value=0, step=1, value =0, key="sub1_01")  
        
        button1, button2 = st.columns(2)
        with button1:
            create_btn = st.button('set column')
        with button2:
            clear_btn = st.button('clear')
            if clear_btn:
              delete_file(file_path)  
                
    with cols1HT2:
        rows = st.number_input("row:", min_value=0, step=1, value =0, key="sub1_02")
    if create_btn:
        dict_old = {'Column {}'.format(i+1): [None] * rows for i in range(columns)}
        save_dict_to_txt(dict_old, file_path) 

    
    try:          
        with cols1HT3:
            before = st.text_input('Before', value= "Column 1")
            colname_btn = st.button('update column name')
        with cols1HT4:
            after = st.text_input('After' , value= "Column 1")
        
        
        if colname_btn:     
            # Check if the key exists in the dictionary
            dict_name = load_dict_from_txt(file_path)
            header = list(dict_name.keys())
            # print("Before:", header)

            if before in dict_name:
                # Find the index of the 'before' key in the list
                index = header.index(before)
                # Replace the 'before' key with the 'after' key in the list
                header[index] = after
                
                # Create a new dictionary with the updated headers
                dict_new = {}
                for old_header, new_header in zip(list(dict_name.keys()), header):
                    dict_new[new_header] = dict_name.pop(old_header)
                
                # Assign dict_new to dict_old to update it
                dict_cols = save_dict_to_txt(dict_new, file_path) 
                st.rerun()
                # Print the updated header and the new dictionary
                # print("After:", header)
                # print("New Dictionary:", dict_new)
            else:
                # print(f"The key '{before}' does not exist in the dictionary.")
                st.warning(f"The key '{before}' does not exist in the dictionary.")
    
    
        dict_cols = load_dict_from_txt(file_path)      
        st.data_editor(pd.DataFrame(dict_cols), num_rows="fixed",hide_index=False, key='demo_df')
           
    
    
        
        ## sample after setup position -------------------------------------------------------
        
        table_col_name = list(dict_cols.keys())
        st.text("xxxxxx")
        
    

    except FileNotFoundError as e:
        # print(f"FileNotFoundError: {e}") 
        pass  
    
    
    
    
########################################################################
    # Select image input
    # Tab 2
######################################################################## 
    
# else:
#     st.error('Username/password is incorrect')
