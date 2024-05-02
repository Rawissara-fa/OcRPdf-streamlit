# ########################################################################
#     # Import library
# ########################################################################

# import streamlit as st
# import numpy as np
# import yaml
# import cv2
# import os
# import pandas as pd
# import base64
# from datetime import datetime
    
# # import PyPDF2 
# import fitz  # PyMuPDF

# from streamlit_cropper import st_cropper
# # from streamlit_image_coordinates import streamlit_image_coordinates
# from PIL import Image
# from io import BytesIO
# from paddleocr import PaddleOCR

# from yaml.loader import SafeLoader 
# import streamlit_authenticator as stauth
# # import components.ocr2result as ocr2result
# # import components.result2db as updatadb




# ########################################################################
#     # Set header page
# ########################################################################

# st.set_page_config(page_title="OoCcRr", page_icon=" ", layout="wide")
# st.title("ARUNSAWAD")
# st.text("document must be same formula")
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
#     st.session_state["tab1_01"] = ""
#     st.session_state["tab1_01"] = ""
#     st.session_state["tab1_02"] = ""
    
#     st.session_state["sub1_00"] = ""
#     st.session_state["sub1_01"] = ""
#     st.session_state["sub1_02"] = ""
    
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
    
#     ## upload file for prepare data -------------------------------------------------    
            
#     uploaded_img = st.file_uploader("**:black[Choose a PDF file]**",accept_multiple_files=False,type=['pdf'], key="tab1_00")
#     if uploaded_img is not None:   
#         save_image_path = './input_items/input_PDFfile/' + uploaded_img.name
#         with open(save_image_path, "wb") as f:
#             f.write(uploaded_img.read())
#         file_path_to_img = '\\input_items\\input_PDFfile\\' + uploaded_img.name 
        
#         pdf_doc = fitz.open(file_path_to_img)
#         num_pages = get_page_no(file_path_to_img)

       
                        
#         ## crop for select detail into box -------------------------------------------------

#         if num_pages is not None:

#             ## created table prepare fill position -------------------------------------------------
#             cols1HT1, cols1HT2, cols1HT3 = st.columns([1, 1, 2]) 
#             @st.cache   
#             def create_table(rows, columns):
#                 data = [[' '] * columns for _ in range(rows)]
#                 df = pd.DataFrame(data)
#                 st.dataframe(df)
                
#             with cols1HT1:
#                 rows = st.number_input("row:", min_value=0, step=1, key="sub1_01")  
#             with cols1HT2:
#                 columns = st.number_input("column:", min_value=0, step=1, key="sub1_02")


#             # Boolean to resize the dataframe, stored as a session state variable
#             st.checkbox("Use container width", value=False, key="use_container_width")
#             data = {'Column {}'.format(i+1): [' '] * columns for i in range(rows)}
#             df = pd.DataFrame(data)
#             st.dataframe(df)
                
                    
#             # ## crop for select detail into box -------------------------------------------------
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
#             original_image = rotated_back_image
            
            
#             ## display image after fill file -------------------------------------------------
            
#             cols1H1, cols1H2, cols1H3 = st.columns([1, 1.5, 2])              
#             # box_color = st.color_picker(label="Box Color", value='#0000FF')
#             aspect_ratio = (1, 1) #None    
#             with cols1H3: 
#                 # Load the image and resize to be no wider than the streamlit widget size
#                 box = st_cropper(original_image, realtime_update = True, box_color = '#4800FF', aspect_ratio= aspect_ratio, return_type = 'box')
#                 crop_arg = (box['left'],               box['top'],
#                             box['width']+ box['left'], box['height']+ box['top'])
                
#             with cols1H2: 
                
#                 cropped_image = original_image.crop(crop_arg)  
#                 st.markdown("**:blue[image in area crop]**")          
#                 _ = cropped_image.thumbnail((1920,1920))
#                 st.image(cropped_image)
                
#             with cols1H1:      
                
#                 read_preview = st.button("preview read", type="primary")
#                 if read_preview:
#                     if cropped_image is not None:
#                         preview_path = '/input_items/input_image/preview.jpg' 
#                         cv2.imwrite(preview_path, np.array(cropped_image))
                    
#                         ocr = PaddleOCR(lang='en')
#                         preview = ocr.ocr((preview_path), cls=False)
                        

#                 else:
#                     folder_path = "./input_items/input_image"
#                     files = os.listdir(folder_path)
#                     for file in files:
#                         if file.endswith(".pdf"):
#                             file_path = os.path.join(folder_path, file)
#                             os.remove(file_path)
#                         else:
#                             pass
                        
#             with cols1H2:
#                 if read_preview:
#                     for res in preview[0]:
#                         st.text(res[1][0])

                
#         else:
#             st.info("wait input document file")   
            
 
#         ## sample fill data in box -------------------------------------------------
                 

        
        
#         ## crop for select headbox -------------------------------------------------
            
#     else:
#         pass
    
   
    
    
    
    
# ########################################################################
#     # Select image input
#     # Tab 2
# ######################################################################## 

# ## กำหนดจุดที่อ่านเฉพาะเเบบ form ทั้ง header content -> save form
# ## https://docs.streamlit.io/develop/api-reference/data/st.data_editor

# ## ออกแบบ การใช้งานก่อน ว่า sideber มีอะไร เลือกยังไง
# ## เลือก form ก่อน read document โดยที่ form สามารถ เพิ่ม-ลดได้
# ## แก้ tab 2-3 ด้วย
# ## ตกเเต่ง UI


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

