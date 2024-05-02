# import streamlit as st
# import pandas as pd
# import pybase64 as base64

# from datetime import datetime
# import fitz  # PyMuPDF
# import numpy as np
# import yaml
# from yaml.loader import SafeLoader 
# import streamlit_authenticator as stauth
# # import components.ocr2result_pe as ocr2result
# import components.result2db_ans as updatadb



# st.set_page_config(page_title="Read scaned PDFfile", page_icon=" ", layout="wide")
# st.title("Read scaned PDFfile")
# # st.markdown("_________________________________________________")

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
#     st.session_state["path_T"] = ""
#     st.session_state["file_T"] = ""
#     st.session_state["path_G"] = ""
#     st.session_state["file_G"] = ""

# table_col_name = ('Filename','Page',
#                   'ShippingInspectionDate','ProductName','LotNo','Project','Specification','Max','Min','Avg','CPK','Sigma','r_n','Judgment',
#                   'ShippingInspectionDate_Conf','ProductName_Conf','LotNo_Conf','Project_Conf','Specification_Conf','Max_Conf','Min_Conf','Avg_Conf',
#                   'CPK_Conf','Sigma_Conf','r_n_Conf','Judgment_Conf',
#                   'Inuse','UpdateTime','FilePath')


    
# # if st.session_state["authentication_status"] is True:
            
# #     st.sidebar.write("Welcome: "+st.session_state.login_user["TITLE_OF_COURTESY_NAME"] +st.session_state.login_user["FIRST_NAME"]+ \
# #                     "\n"+ "Department: " + st.session_state.login_user["SECTION_NAME"])
# #     authenticator.logout('Logout', 'sidebar', key='unique_key')


        
    
# # -----------------------------------------
# ## Select image Path in server
# #------------------------------------------

# current_today = datetime.now()
# current_folder = str(current_today).split(".")[0]
# # print(current_folder)
        
# ## file_image by filter 
# tab1, tab2 = st.tabs(["read one by one" ,"read one by group"])
# with tab1: 
    
#     st.subheader("**:green[Update folder path :]**" ) 

#     with st.form("myform_T", border =False):    
#         cols1, cols2 = st.columns([3, 2])
#         with cols1:
#             main_folder_path_T = st.text_input("Folder:  ", key="path_T")
#             name_file          = st.text_input("Scaned PDFfile: (include.pdf)", key="file_T")  
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
#                         # results, status_file = ocr2result_ans.extract_text_from_pdf(file_path_to_chk_T, i, current_folder)
#                         # data_to_insert = pd.DataFrame(results).iloc[1:]
#                         # st.text(data_to_insert)
#                         # print(status_file)

#                         st.markdown("_________________________________________________")               

#         except Exception as ex:
#                 print(f'Error: {file_path_to_chk_T} \nMessage: {ex}')
#                 st.text(f'Error: {file_path_to_chk_T} \nMessage: {ex}')
                
    
#     if clear:
#         st.write("")
#         st.cache_data.clear()
   
#     displaypdf = st.toggle('display PDFfile')

#     if displaypdf:
#         if bytes_data is not None:
#             st.write("filename:", uploaded_file.name)
#             base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
#             pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
#             st.markdown(pdf_display, unsafe_allow_html=True)
#         else:
#             st.text("Empty")
        
#     # ##-------------------------------------------------------
#     # # UPCrop Image for SAVE JPEG File
#     # ##-------------------------------------------------------  
  
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

#     #             with cols5:
#     #                 img = open_img_input
#     #                 realtime_update = st.checkbox(label="Update in Real Time", value=True, disabled=False)
#     #                 if not realtime_update:
#     #                     st.write("Double click to save crop")
#     #                 cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color,aspect_ratio=aspect_ratio)
                
#     #             with cols4:
#     #                 st.write("Preview")
#     #                 _ = cropped_img.thumbnail((150,150))
#     #                 st.image(cropped_img)
#     #                 st.text("")

#     #                 if st.button("Reset image!!!", type="primary"):
#     #                     img_preview = img_arr
#     #                 elif st.button("UPdate image", type="secondary"):
#     #                     img_preview = cropped_img.save("cropped_img.jpg")
#     #                 else:
#     #                     img_preview = image_input
#     #     else:
#     #         status_crop = False
    
        
# with tab2: 

#     with st.form("myform_G", border =False,):
        
#         st.subheader("**:green[Update folder path :]**" )
#         main_folder_path = st.text_input("Folder:  ", key="path_G")
#         sub_folders      = st.text_input("Scaned PDF folder: ", key="file_G")
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

