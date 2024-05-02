# from PIL import Image, ImageEnhance, ImageFilter
# import matplotlib.pyplot as plt
# from datetime import datetime
# import fitz  # PyMuPDF
# import numpy as np
# import cv2
# import os

# import streamlit as st
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\rawissara.bua\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


# ###  --------------------------------------------------------------------------------
# @st.cache_data
# def draw_lines(img, lines, angle_criteria=None):
#     filtered_lines = []
#     for line in lines:
#         rho, theta = line[0]
#         angle = theta * 180 / np.pi
#         if angle_criteria is None or (angle_criteria[0] <= angle <= angle_criteria[1]):  # Only consider lines within the specified angle range
#             filtered_lines.append((rho, theta))  # Store the lines that meet the condition
#             a = np.cos(theta)
#             b = np.sin(theta)
#             x0 = a * rho
#             y0 = b * rho
#             x1 = int(x0 + 1000 * (-b))
#             y1 = int(y0 + 1000 * (a))
#             x2 = int(x0 - 1000 * (-b))
#             y2 = int(y0 - 1000 * (a))
#             cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

#     return filtered_lines

# ###  --------------------------------------------------------------------------------
# @st.cache_data
# def calculate_rotation_angle(img_array, edge_distance=1):

#     gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     edges = cv2.Canny(blurred, 50, 150)
#     dilated_edges = cv2.dilate(edges, None)

#     # Find contours of dilated edges
#     contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     contour_img = np.zeros_like(img_array)
#     cv2.drawContours(contour_img, contours, -1, (255, 255, 255), thickness=edge_distance)

#     # Convert the contour image to grayscale
#     contour_gray = cv2.cvtColor(contour_img, cv2.COLOR_RGB2GRAY)
#     lines = cv2.HoughLines(contour_gray, 1, np.pi / 180, threshold=120)
    
#     # Draw lines on the image and get lines that meet the condition
#     line_img = np.zeros_like(img_array)
#     filtered_lines = draw_lines(line_img, lines, angle_criteria=(70, 110))

#     # Calculate average angle of detected lines
#     angles = [angle for _, angle in filtered_lines]
#     avg_angle = np.mean(angles) if angles else 0.0

#     return avg_angle / np.pi * 180.0


# ###  --------------------------------------------------------------------------------
# @st.cache_data
# def maching_to_crop_image(input_image,templateN,):
        
#     imageN = np.array(input_image).copy()
#     image_h, image_w = input_image.size
    
#     image_gray = cv2.cvtColor(imageN, cv2.COLOR_BGR2GRAY)
#     template_gray = cv2.cvtColor(templateN, cv2.COLOR_BGR2GRAY)
#     _, binary_image = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY_INV)
#     _, binary_template = cv2.threshold(template_gray, 100, 255, cv2.THRESH_BINARY_INV)

#     template_h, template_w = templateN.shape[:-1]
#     result = cv2.matchTemplate(binary_image, binary_template, cv2.TM_CCOEFF)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

#     # draw a rectangle around the best match
#     top_left = (max_loc[0], max_loc[1])
#     bottom_right = (top_left[0] +image_w, top_left[1])
#     crop_image = imageN[top_left[1] :top_left[1]+image_h , top_left[0] :bottom_right[0]]
    
#     # Matching only area
#     crop_image_gray = cv2.cvtColor(crop_image.copy(), cv2.COLOR_BGR2GRAY)
#     crop_image_roi = crop_image_gray[0 :template_h , 0:template_w]

#     # percent of similar after matching
#     result = cv2.matchTemplate(crop_image_roi, template_gray, cv2.TM_CCOEFF_NORMED)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#     percentage_similarity = round(max_val * 100, 2)

    
#     return crop_image, percentage_similarity


# ###  --------------------------------------------------------------------------------
# @st.cache_data
# def preprocess_image_for_read(images_input ,W,H):

#     image_input_h, image_input_w = images_input.shape[:-1]
#     avg_value = (np.average(np.sum(images_input, axis=0)*100)/(255.*image_input_h))
#     # print(avg_value)
    
#     if int(avg_value)*10 < 970:
    
#         # Prepocess  
#         image_h, image_w = images_input.shape[:-1]
#         kernel1 = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))

#         image = cv2.resize(images_input.copy(), (W*image_w, H*image_h), interpolation=cv2.INTER_LINEAR_EXACT)  
#         _,thres = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)
        
#         morpho_open = cv2.morphologyEx(thres, cv2.MORPH_OPEN, kernel1)
#         _,imageR = cv2.threshold(morpho_open, 0, 255, cv2.THRESH_BINARY_INV)
#         imageR = cv2.erode(imageR, kernel1, iterations = 1)
    
#     else:
#         _,thres = cv2.threshold(images_input, 150, 255, cv2.THRESH_BINARY)
#         imageR = thres

#     return  imageR


# ###  ------------------------------------------------------------------
# @st.cache_data
# def remove_vertical_lines(images_input):
    
#     image_input_h, image_input_w = images_input.shape[:-1]
#     gray_image = cv2.cvtColor(images_input, cv2.COLOR_BGR2GRAY)
#     _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

#     ### target_column ------------------------------------------------------
#     for column_index in enumerate(binary_image):
#         sumx_values = (np.sum(binary_image, axis=0)*100)/(255.*image_input_h)
#         posix_values = np.where(sumx_values< int(30/100*image_input_h))


#     for column in range (0, len(posix_values[0])):
#         target_column = posix_values[0][column]
#         if (target_column == "0") |(target_column == (image_input_w-3)):
#             for row, value in enumerate(binary_image[:, target_column]):
#                 gray_image[row, target_column ] = 255
#                 for i in range (0,3):
#                     gray_image[row, target_column+i] = 255
#         elif (target_column != "0") & (target_column != (image_input_w-1)):
#             for row, value in enumerate(binary_image[:, target_column]):
#                 gray_image[row, target_column  ] = 255
#                 for i in range (1,4):
#                     gray_image[row, target_column-i] = 255
#         else:
#             pass
    
#     image = cv2.cvtColor(gray_image , cv2.COLOR_GRAY2BGR)  
#     return image


# ###  ------------------------------------------------------------------
# @st.cache_data
# def remove_horizontal_lines(images_input):  
    
#     image_input_h, image_input_w = images_input.shape[:-1]
#     gray_image = cv2.cvtColor(images_input, cv2.COLOR_BGR2GRAY)
#     _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
    
#     ## target_row ------------------------------------------------------
#     for row_index in enumerate(binary_image):
#         sumy_values = (np.sum(binary_image, axis=1)*100)/(255.*image_input_w)
#         posiy_values = np.where(sumy_values< int(40/100*image_input_h))
    
#     for row in range (0, int(len(posiy_values[0]))):
#         target_row = posiy_values[0][row]
        
#         if (target_row == "0") |(target_row == (image_input_w-1)):
#             for column, value in enumerate(binary_image[target_row, :]):
#                 gray_image[target_row , column] = 255
#                 for i in range (0,3):
#                     gray_image[target_row +i, column  ] = 255
#         elif (target_row != "0") & (target_row <= (image_input_h-1)):
#             for column, value in enumerate(binary_image[target_row, :]):
#                 gray_image[target_row  , column] = 255
#                 for i in range (1,4):
#                     gray_image[target_row-i, column] = 255
#         else:
#             pass
    
#     image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)          
#     return image

# ###  ------------------------------------------------------------------
# @st.cache_data
# def separate_row_lines(image_input):
    
#     image_input_h, image_input_w = image_input.shape[:-1]
#     gray_image = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY)
#     _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
    
#     sumvalue_yaxis_edge = np.sum(binary_image, axis=1)/255.
#     upperedge = int(np.array(np.where(sumvalue_yaxis_edge > int(2/3*image_input_w))[0])[1])
#     loweredge = int(np.array(np.where(sumvalue_yaxis_edge > int(1/3*image_input_w))[0])[-2]) 
    
#     gray_image_crop = cv2.cvtColor(image_input[upperedge:loweredge, 0:image_input_w], cv2.COLOR_BGR2GRAY)
#     _, binary_image_crop = cv2.threshold(gray_image_crop, 200, 255, cv2.THRESH_BINARY)
    
#     sumvalue_yaxis = (np.sum(binary_image_crop, axis=1)*100)/(255.*image_input_w)
#     posiy = (np.where(sumvalue_yaxis< 20))[0]
#     # print(posiy)

#     if len(posiy)> 2:

#         print("Type split: splittype_1")
#         upline = [posiy[0]]
#         for ii in range (0, len(posiy)-1):
#             if (posiy[ii+1]- posiy[ii]) > 1:
#                 upline.append(posiy[ii+1])
#         if (upline[1] < int(1/2*image_input_h)):
#             image_au = binary_image_crop[upline[1]-20:upline[2]+20 , 0:image_input_w]
#         else:
#             image_au = binary_image_crop[upline[0]-20:upline[1]+20 , 0:image_input_w]
#     else:
#         print("Type split: splittype_2")
#         image_au = binary_image_crop[int(1/4*image_input_h):int(3/4*image_input_h)-15, 0:image_input_w]
    
#     image_au = cv2.cvtColor(image_au, cv2.COLOR_GRAY2BGR)
#     return image_au


# ###  ------------------------------------------------------------------
# @st.cache_data
# def crop_text_regions(image_input):
      
#     image_input_h, image_input_w = image_input.shape[:-1]
#     _, binary_image = cv2.threshold(image_input.copy(), 250, 255, cv2.THRESH_BINARY)   
#     binary_image = binary_image[5:image_input_h -5, 5:image_input_w -5]
        
#     sum_y = (np.sum(binary_image, axis=1)*100)/(image_input_w*255.)  # y axis   
#     sum_x = (np.sum(binary_image, axis=0)*100)/(image_input_h*255.)  # x axis
    
#     miny = np.array(np.where(sum_y <95)[0])[0]
#     maxy = np.array(np.where(sum_y <95)[0])[-1]       
#     minx = np.array(np.where(sum_x <95)[0])[0]
#     maxx = np.array(np.where(sum_x <95)[0])[-1]  

#     if (miny-10) <= 0:             diff_miny = 0          
#     else: diff_miny = 10
#     if (minx-10) <= 0:             diff_minx = 0
#     else: diff_minx = 10
#     if (maxy+10) >= image_input_h: diff_maxy = image_input_h
#     else: diff_maxy = 10
#     if (maxx+10) >= image_input_w: diff_maxx = image_input_w 
#     else: diff_maxx = 10
        
#     if (miny == 0) & (minx != 0) :
#         print("Type crop: croptype_1")
#         binary_image = binary_image[miny          :maxy +diff_maxy, minx -diff_minx:maxx +diff_maxx]
#     elif (miny != 0) & (minx == 0) :
#         print("Type crop: croptype_2")
#         binary_image = binary_image[miny-diff_miny:maxy +diff_maxy, minx           :maxx +diff_maxx]
#     else:
#         print("Type crop: croptype_3")
#         binary_image = binary_image[miny-diff_miny:maxy +diff_maxy, minx -diff_minx:maxx +diff_maxx]
        
#     return binary_image


# ## ---------------------------------------------------------------------------------
# @st.cache_data
# def only_float_from_str(str_input):
#     import re
#     return re.findall("\s+\.\s+", str_input)

# @st.cache_data
# def sort_str_input(str_input):
#     try:
#         str_splited = str_input.split(".")   
#         # print(str_splited)
#         if len(str_splited) > 2:
#             if len(str_splited[1])==3 and str_splited[1][0] == '0':
#                     str_sorted = str_splited[0] + "." + str_splited[1][-2:]
#             else:
#                 str_sorted = str_input
#         else:
#             str_sorted = str_input
#     except:
#         str_sorted = str_input
#     return str_sorted

# @st.cache_data
# def get_text_and_conf(img, filter_float=False):
#     text = pytesseract.image_to_data(img, output_type='data.frame', lang='jpn+eng', config='--psm 6')  # for float&character
#     text = text[text.conf > 0 ]

    
#     lines = text.groupby(['line_num'], 
#                          group_keys=True)['text'].apply(lambda x:''.join(str(item) for item in x).replace(" ","").replace(",", ".").replace("|", "1").replace("]", "1")).to_list()
#     confs = text.groupby(['line_num'], group_keys=True)['conf'].mean().tolist()
#     # print(lines, confs)
    
#     if len(lines)==0:
#         lines = [""]
#         confs = [""]
#         return lines[0], confs[0]
#     else:
#         lines = [sort_str_input(lines[0])]
    
#     if filter_float:
#         lines_float = []
#         for l in lines:
#             lines_float = only_float_from_str(l)#[.
#         return lines_float[0], confs[0]
 
#     else:            
#         return lines[0], confs[0]
    

# ## ---------------------------------------------------------------------------------
# @st.cache_data
# def extract_text_from_pdf(pdf_path, page_number, server_time):

#     with fitz.open(pdf_path) as pdf_document:
#     #     for page_number in range(pdf_document.page_count):
#             page = pdf_document[page_number]
#             pixmap = page.get_pixmap(dpi= 300)

#             # image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
#             img_array = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape((pixmap.height, pixmap.width, pixmap.n))  
#             name_file = (pdf_path.split('/')[-1]).split('\\')[-1]       
#             file_page = str(int(page_number)+1)
#             # opening = ("File: " +name_file + "  page " + str(page_number+1) + "...... is opening")

            
#             # Rotate the page by the calculated rotation angle
#             rotation_angle = calculate_rotation_angle(img_array)
#             if rotation_angle is not None :
#                 inclination_dgree = rotation_angle
#             else:
#                 inclination_dgree = 0
#             rotated_back_image = Image.fromarray(cv2.warpAffine(img_array, 
#                                                             cv2.getRotationMatrix2D((pixmap.width // 2, pixmap.height // 2), 
#                                                                                     inclination_dgree-90.05, 1), (pixmap.width, pixmap.height)))
             
            
#             # ###  --------------------------------------------------------------------------------

#             input_image = rotated_back_image.copy()
#             template_head1 = cv2.imread('./Template/tem_head1.png')
#             template_head2 = cv2.imread('./Template/tem_head2.png')
            
#             text_topic = "Au plating thickness (P)"
#             conf_topic = ""
#             text_jude  = "Pass"
#             conf_jude  = ""
#             Inuse      = ""

            
#             # character = name_file.split(".pdf")[0]
#             # if len(character) > 3:
#             #     if (int(character[0]) >= 2) & (int(character[1]) >= 2):
#             #         status_temp = 'tempver2'
#             #         opening = ("File: " +name_file + "  page " + str(page_number+1) + "...... read compeleted")
#             #     else:
#             #         status_temp = 'tempver1'
#             #         opening = ("File: " +name_file + "  page " + str(page_number+1) + "...... read compeleted")
#             # else:
#             #     opening = ("File: " +name_file + "  page " + str(page_number+1) + "...... can't opening")
                

#             input_head1, val_similarity1 = maching_to_crop_image(input_image,template_head1)
#             input_head2, val_similarity2 = maching_to_crop_image(input_image,template_head2)
#             print(type(val_similarity1), "Temp1:", val_similarity1, type(val_similarity2), "Temp2:", val_similarity2)
            
#             if val_similarity1 > val_similarity2:
#                 status_temp = "tempver1" 
#                 opening = ("File: " +name_file + "  page " + str(page_number+1) + "...... read compeleted")             
            
#             elif val_similarity1 < val_similarity2:
#                 status_temp = "tempver2"
#                 opening = ("File: " +name_file + "  page " + str(page_number+1) + "...... read compeleted")
            
#             else:
#                 opening = ("File: " +name_file + "  page " + str(page_number+1) + "...... can't opening")
            
            
#             if status_temp == "tempver1":

#                 print("Type temp: temptype_1")
#                 ## line date
#                 input_date = input_head1[20:110, 250:800]
#                 text_date, conf_date = get_text_and_conf(input_date, filter_float=False)
                
#                 ## line product
#                 input_product = input_head1[130:220, 300:850]
#                 text_product, conf_product = get_text_and_conf(input_product, filter_float=False)
                
#                 ## line lot
#                 input_lot = input_head1[20:110, 1100:1400]
#                 text_lot, conf_lot = get_text_and_conf(input_lot, filter_float=False)
#                 text_lot = text_lot[0:4]
                
#                 text_date = text_date
#                 text_product = text_product.split("F")[1]
#                 if text_product[-3:-1] == '20)':
#                     text_product = "F" +text_product.replace(")","")
#                 else:
#                     text_product = "F" +text_product.replace("-", "")
#                 text_lot = text_lot
                
                  
#             elif status_temp == "tempver2":

#                 print("Type temp: temptype_2")
#                 # line date
#                 input_date = input_head2[30:105, 1150:1400]
#                 text_date, conf_date = get_text_and_conf(input_date, filter_float=False)
                
#                 ## line product
#                 input_product = input_head2[120:210, 100:660]  #120:210, 160:600
#                 text_product, conf_product = get_text_and_conf(input_product, filter_float=False)
                
#                 ## line lot
#                 input_lot = input_head2[230:320, 880:1200]
#                 text_lot, conf_lot = get_text_and_conf(input_lot, filter_float=False)
#                 text_lot = text_lot[-4:]
                
#                 text_date = text_date
#                 text_product = text_product.split("F")[1]
#                 if text_product[-3:-1] == '20)':
#                     text_product = "F" +text_product.replace(")","")
#                 else:
#                     text_product = "F" +text_product.replace("-", "")
#                 text_lot = text_lot   
                
#             else:
#                 pass
            
            
#             ## line Au
#             # ## Topic % criteria ----------------------------------------------------------------------------------------------------
            
#             template_au = cv2.imread('./Template/tem_mau.png')
#             input_meau, val_similarity_meau = maching_to_crop_image(input_image,template_au)
#             print(type(val_similarity_meau), "Temp au: ", val_similarity_meau)
            
#             ## rotate again
#             input_meau_h, input_meau_w = input_meau.shape[:-1]
#             rotation_angle_part = calculate_rotation_angle(input_meau[0:input_meau_h, int(input_meau_w*2/3):input_meau_w])     
#             if rotation_angle_part >90:
#                 rotation_angle_parts = (-1)*(89.9-rotation_angle_part)
#             else:
#                 rotation_angle_parts = (rotation_angle_part-89.9)
#             print("rotation_angle mea: ", rotation_angle_part, rotation_angle_parts)

#             rotated_back_image_2 = cv2.warpAffine(input_meau.copy(), 
#                                                         cv2.getRotationMatrix2D((input_meau_w // 2, input_meau_h // 2), 
#                                                                                 rotation_angle_parts, 1), (input_meau_w, input_meau_h))
            
            
            
#             input_meaN =  rotated_back_image_2.copy()[0:input_meau_h, 0:input_meau_w]
#             input_mea = remove_vertical_lines(separate_row_lines(input_meaN))
#             input_mea_h, input_mea_w = input_mea.shape[:-1]    
            
#             results_read = []            
#             for ii in range (0,8):
#                 if   str(ii) == '0':  input_label = input_mea[0:input_mea_h,  550:1000]
#                 elif str(ii) == '1':  input_label = input_mea[0:input_mea_h, 1170:1350]
#                 elif str(ii) == '2':  input_label = input_mea[0:input_mea_h, 1320:1500]
#                 elif str(ii) == '3':  input_label = input_mea[0:input_mea_h, 1470:1660]
#                 elif str(ii) == '4':  input_label = input_mea[0:input_mea_h, 1620:1810]
#                 elif str(ii) == '5':  input_label = input_mea[0:input_mea_h, 1800:1980]
#                 elif str(ii) == '6':  input_label = input_mea[0:input_mea_h, 1940:2090]
                
#                 text_read, conf_criteria = get_text_and_conf(crop_text_regions(preprocess_image_for_read(remove_horizontal_lines(input_label) ,4,4)), filter_float=False)  
#                 if len(text_read) != 0:
#                     results_read.append([text_read, conf_criteria, ii])
#                 else:
#                     text_read, conf_criteria = get_text_and_conf( preprocess_image_for_read(remove_horizontal_lines(input_label) ,4,4), filter_float=False) 
#                     results_read.append([text_read, conf_criteria,ii])

#             text_criteria = (results_read[0][0].replace("..", "."))[0:7].replace("umMI", "")
#             text_max      = results_read[1][0][0:4].replace("/", "7")
#             text_min      = results_read[2][0][0:4].replace("/", "7")
#             text_avg      = results_read[3][0][0:4].replace("/", "7")
#             text_cpk      = results_read[4][0][0:4].replace("/", "7")
#             text_sig      = results_read[5][0][0:4].replace("/", "7")
#             text_rn       = (results_read[6][0].replace("7","/"))[0:3]
            
#             conf_criteria = results_read[0][1]
#             conf_max      = results_read[1][1] ; conf_min = results_read[2][1] ; conf_avg = results_read[3][1]
#             conf_cpk      = results_read[4][1] ; conf_sig = results_read[5][1] ; conf_rn  = results_read[6][1]
            
            
#             ## ---------------------------------------------------------------------------------------------------------
            
#             table_col_name = (name_file, file_page, 
#                               text_date, text_product, text_lot, text_topic, text_criteria, text_max, text_min, text_avg , text_cpk, text_sig, text_rn, text_jude, 
#                               conf_date, conf_product, conf_lot, conf_topic, conf_criteria, conf_max, conf_min, conf_avg, conf_cpk, conf_sig, conf_rn, conf_jude,
#                               Inuse, server_time, pdf_path)
    
#     return table_col_name, opening