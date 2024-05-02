# ########################################################################
#     # Import library
# ########################################################################

# import streamlit as st
# import numpy as np
# import yaml
# import cv2
# import pandas as pd
# import pybase64 as base64
# from datetime import datetime
    
# from PyPDF2 import PdfReader
# import fitz  # PyMuPDF

# from streamlit_cropper import st_cropper
# from streamlit_image_coordinates import streamlit_image_coordinates
# from PIL import Image
# from io import BytesIO

# from yaml.loader import SafeLoader 
# import streamlit_authenticator as stauth
# import components.ocr2result as ocr2result
# import components.result2db as updatadb




# ########################################################################
#     # Set header page
# ########################################################################

# st.set_page_config(page_title="OoCcRr", page_icon=" ", layout="wide")
# st.title("ARUNSAWAD")
# # st.markdown("_________________________________________________")




# ########################################################################
#     # Set addition for use
# ########################################################################

# # Check authentication when user lands on the page.
# with open("config.yaml") as file:
#     config = yaml.load(file, Loader=SafeLoader)
    
# authenticator = stauth.Authenticate(
# config['credentials'],
# config['cookie']['name'],
# config['cookie']['key'],
# config['cookie']['expiry_days']
# # config['preauthorized']
# )


# def get_page_no(pdf_path):
#     with fitz.open(pdf_path) as pdf_document:
#         return pdf_document.page_count 


# def clear_form():
#     st.session_state["tab1_00"] = ""
#     st.session_state["tab1_01"] = ""
#     st.session_state["tab1_02"] = ""
    
#     st.session_state["tab2_00"] = ""
#     st.session_state["tab2_01"] = ""
#     st.session_state["tab2_02"] = ""
    
#     st.session_state["tab3_00"] = ""
#     st.session_state["tab3_01"] = ""
#     st.session_state["tab3_02"] = ""


# table_col_name = ('Filename','Page',
#                   'ShippingInspectionDate','ProductName','LotNo','Project','Specification','Max','Min','Avg','CPK','Sigma','r_n','Judgment',
#                   'ShippingInspectionDate_Conf','ProductName_Conf','LotNo_Conf','Project_Conf','Specification_Conf','Max_Conf','Min_Conf','Avg_Conf',
#                   'CPK_Conf','Sigma_Conf','r_n_Conf','Judgment_Conf',
#                   'Inuse','UpdateTime','FilePath')

# ### table_col_name => SET by template page
    
# # if st.session_state["authentication_status"] is True:
            
# #     st.sidebar.write("Welcome: "+st.session_state.login_user["TITLE_OF_COURTESY_NAME"] +st.session_state.login_user["FIRST_NAME"]+ \
# #                     "\n"+ "Department: " + st.session_state.login_user["SECTION_NAME"])
# #     authenticator.logout('Logout', 'sidebar', key='unique_key')


        
 
# ########################################################################
#     # Select image input
#     # Tab 1
# ########################################################################   

# current_today = datetime.now()
# current_folder = str(current_today).split(".")[0]

        
# ## file_image by filter 
# tab1, tab2, tab3 = st.tabs(["config template", "read doc by one" ,"read doc by group"])
# with tab1:
    
  
#     uploaded_img = st.file_uploader("Choose a PDF file",accept_multiple_files=False,type=['pdf'], key="tab1_00")
#     if uploaded_img is not None:   
#         save_image_path = './input_PDFfile/' + uploaded_img.name
#         with open(save_image_path, "wb") as f:
#             f.write(uploaded_img.read())
#         file_path_to_img = '.\\input_PDFfile\\' + uploaded_img.name 
        
#         pdf_doc = fitz.open(file_path_to_img)
#         num_pages = get_page_no(file_path_to_img)
        
#         ## crop for select headbox -------------------------------------------------
#         headbox = st.toggle('crop for select headbox' ,key = "tab1_01")

#         if headbox:
#             cols4, cols5, cols6 = st.columns([2, 0.1, 3]) 
#             with cols4: 
#                 box_color = st.color_picker(label="Box Color", value='#0000FF')
#                 aspect_choice = st.radio(label="Aspect Ratio", options=["1:1", "5:1", "Free"])
#                 aspect_dict = {
#                     "1:1": (1, 1),
#                     "5:1": (5, 1),
#                     "Free": None
#                 }
#                 aspect_ratio = aspect_dict[aspect_choice]
#                 # aspect_ratio = None
                

#             with cols6:
        
#                 selected_page = st.selectbox("select page for use: ", range(1, num_pages + 1), index=0)
#                 page = pdf_doc[selected_page - 1]
                
#                 # Get image bytes from the page
#                 pixmap = page.get_pixmap()
#                 #-- img    = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
#                 img_array = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape((pixmap.height, pixmap.width, pixmap.n))
                
#                 # Rotate the page by the calculated rotation angle
#                 rotation_angle = ocr2result.calculate_rotation_angle(img_array)
#                 if rotation_angle is not None :
#                     inclination_dgree = rotation_angle
#                 else:
#                     inclination_dgree = 0
#                 rotated_back_image = Image.fromarray(cv2.warpAffine(img_array, 
#                                                                 cv2.getRotationMatrix2D((pixmap.width // 2, pixmap.height // 2), 
#                                                                                         inclination_dgree-90.05, 1), (pixmap.width, pixmap.height)))

#                 # Save the image to BytesIO buffer
#                 img_bytes_io = BytesIO()
#                 rotated_back_image.save(img_bytes_io, format="PNG")
#                 img_bytes = img_bytes_io.getvalue()

#                 # Display the image
#                 # st.image(img_bytes, caption=f"page {selected_page}/{num_pages}")
                
#                 original_image = rotated_back_image
                
#                 # Load the image and resize to be no wider than the streamlit widget size
#                 box = st_cropper(original_image, realtime_update = True, box_color = box_color, aspect_ratio= aspect_ratio, return_type = 'box')
#                 crop_arg = (box['left'],               box['top'],
#                             box['width']+ box['left'], box['height']+ box['top'])
                
#             with cols4:
#                 st.write("Position")
#                 cols11, cols12 = st.columns([1, 1])
#                 with cols11:
#                     left = st.number_input("X", value = box['left'])
#                     width = st.number_input("Width", value = box['width'])
#                 with cols12:
#                     top = st.number_input("Y", value = box['top'])
#                     height = st.number_input("Height", value = box['height'])
            
            
#             with cols6:
#                 if (box['left'] != left) | (box['top'] != top) | (box['width'] != width) | (box['height'] != height)  : 
#                     box = (left, left + width, top, top + height)
                    
#                     box = st_cropper(original_image, realtime_update = True, default_coords=box, box_color = box_color, aspect_ratio= aspect_ratio, return_type = 'box' )
#                     crop_arg = (box['left'],               box['top'],
#                                 box['width']+ box['left'], box['height']+ box['top'])
#                     cropped_image = original_image.crop(crop_arg)
#                     print(crop_arg)
#                 else:
#                     crop_arg = (box['left'],               box['top'],
#                                 box['width']+ box['left'], box['height']+ box['top'])
                    

#             with cols4:      
#                 cropped_image = original_image.crop(crop_arg)               
#                 st.write("Preview")
#                 _ = cropped_image.thumbnail((1920,1920))
#                 st.image(cropped_image)
                
                
                
#         else:
#             pass
        
#         ## crop for select headbox -------------------------------------------------
            
#     else:
#         pass
    
    
            
#     # if uploaded_img is not None: 
#     #     crop_fuc_img = st.toggle('crop image input')  
#     #     if crop_fuc_img:
#     #         status_crop = True
#     #         with st.container(border=True):
#     #             cols4, cols5 = st.columns([1, 4]) 
#     #             with cols4: 
#     #                 box_color = st.color_picker(label="Box Color", value='#0000FF')
#     #                 # aspect_choice = st.radio(label="Aspect Ratio", options=["1:1", "16:9", "Free"])
#     #                 # aspect_dict = {
#     #                 #     "1:1": (1, 1),
#     #                 #     "16:9": (16, 9),
#     #                 #     "Free": None
#     #                 # }
#     #                 # aspect_ratio = aspect_dict[aspect_choice]
#     #                 aspect_ratio = None

#     #             # with cols5:
#     #             #     img = open_img_input
#     #             #     realtime_update = st.checkbox(label="Update in Real Time", value=True, disabled=False)
#     #             #     if not realtime_update:
#     #             #         st.write("Double click to save crop")
#     #             #     cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color,aspect_ratio=aspect_ratio)
                
#     #             # with cols4:
#     #             #     st.write("Preview")
#     #             #     _ = cropped_img.thumbnail((150,150))
#     #             #     st.image(cropped_img)
#     #             #     st.text("")

#     #             #     if st.button("Reset image!!!", type="primary"):
#     #             #         img_preview = img_arr
#     #             #     elif st.button("UPdate image", type="secondary"):
#     #             #         img_preview = cropped_img.save("cropped_img.jpg")
#     #             #     else:
#     #             #         img_preview = image_input
#     #     else:
#     #         status_crop = False
#     # st.text ("con")
    
    
    
    
# ########################################################################
#     # Select image input
#     # Tab 2
# ######################################################################## 

# with tab2: 
    
#     st.subheader("**:green[Update folder path :]**" ) 

#     with st.form("myform_T"):    
#         cols1, cols2 = st.columns([3, 2])
#         with cols1:
#             main_folder_path_T = st.text_input("Folder:  ", key="tab2_00")
#             name_file          = st.text_input("Scaned PDFfile: (include.pdf)", key="tab2_01")  
#             file_path_to_chk_T = main_folder_path_T +"\\"+ name_file 
#             st.text("")

#         with cols2:
#             uploaded_file = st.file_uploader("Choose a PDF file",accept_multiple_files=False,type=['pdf'])
#             if uploaded_file is not None:
#                 bytes_data          = uploaded_file.read()
#                 save_image_path = './input_PDFfile/' + uploaded_file.name
#                 with open(save_image_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())
#                 file_path_to_chk_T = '.\\input_PDFfile\\' + uploaded_file.name 
                
#             else:
#                 pass
    
#         f1, f2 = st.columns([1, 10]) 
#         with f1:
#             submit = st.form_submit_button(label="Submit")
#         with f2:
#             clear  = st.form_submit_button(label="Clear", on_click=clear_form)
        
        
#     if submit:
    
#         try:       
#             if (file_path_to_chk_T != "Path_Folder\PDFfile"):
#                 page_number = get_page_no(file_path_to_chk_T)
#                 cols3, cols4 = st.columns([1,2])
#                 with cols3:
#                     table_col = pd.DataFrame(table_col_name).iloc[1:]
#                     for i in range(page_number):      
#                         st.text(table_col)
#                         st.markdown("_________________________________________________")
#                 with cols4:
#                     for i in range(page_number):
#                         results, status_file = ocr2result.extract_text_from_pdf(file_path_to_chk_T, i, current_folder)
#                         data_to_insert = pd.DataFrame(results).iloc[1:]
#                         st.text(data_to_insert)
#                         print(status_file)

#                         st.markdown("_________________________________________________")               

#         except Exception as ex:
#                 print(f'Error: {file_path_to_chk_T} \nMessage: {ex}')
#                 st.text(f'Error: {file_path_to_chk_T} \nMessage: {ex}')
                
    
#     if clear:
#         st.write("")
#         st.cache_data.clear()
   
#     displaypdf = st.toggle('display PDFfile', key ="tab2_02")
#     if displaypdf:
#         if bytes_data is not None:
#             st.write("filename:", uploaded_file.name)
#             base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
#             pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
#             st.markdown(pdf_display, unsafe_allow_html=True)
#         else:
#             st.text("Empty")
        
    
    

# ########################################################################
#     # Select image input
#     # Tab 3
# ######################################################################## 
      
# with tab3: 

#     with st.form("myform_G"):
        
#         st.subheader("**:green[Update folder path :]**" )
#         main_folder_path = st.text_input("Folder:  ", key="tab3_00")
#         sub_folders      = st.text_input("Scaned PDF folder: ", key="tab3_01")
#         st.text("")
        
#         update_data = st.checkbox('update data in database')
#         if update_data:
#             update_db = True
#         else:
#             update_db = False
        
#         f3, f4 = st.columns([1, 10]) 
#         with f3:
#             submit = st.form_submit_button(label="Submit")
#         with f4:
#             clear  = st.form_submit_button(label="Clear", on_click=clear_form)
    
#     file_path_to_chk = main_folder_path +"\\"+ sub_folders
    
#     if submit:   
#         try:
                    
#             if (main_folder_path is not None) & (sub_folders is not None):    
#                 updatadb.result2db(main_folder_path, sub_folders, table_col_name, update_data)
#                 print(" :)* ")
    
#             else:
#                 pass

#         except Exception as ex:
#                 print(f'Error: {file_path_to_chk} \nMessage: {ex}')
#                 st.text(f'Error: {file_path_to_chk} \nMessage: {ex}')

#     if clear:
#         st.write("")
#         st.cache_data.clear()


        
    

# # elif st.session_state["authentication_status"] == False:
# #     st.error('Username/password is incorrect')
# # elif st.session_state["authentication_status"] == None:
# #     st.warning('Please enter your username and password')
    
    
# # # -----------------------------------------
# #   ## Remark select page
# # #------------------------------------------
# # # Rest of the page
# # # st.markdown("# Progams Judgement")
# # # st.sidebar.header(" ")

