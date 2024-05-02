########################################################################
    # Import library
########################################################################
# @st.cache_data

from datetime import datetime
import time
import streamlit as st

import fitz  # PyMuPDF
import numpy as np
import pandas as pd
import cv2
# import os

import pandas as pd
from functools import reduce
from paddleocr import PaddleOCR, draw_ocr


###  --------------------------------------------------------------------------------
@st.cache_data
def draw_lines(img, lines, angle_criteria=None):
    filtered_lines = []
    for line in lines:
        rho, theta = line[0]
        angle = theta * 180 / np.pi
        if angle_criteria is None or (angle_criteria[0] <= angle <= angle_criteria[1]):  # Only consider lines within the specified angle range
            filtered_lines.append((rho, theta))  # Store the lines that meet the condition
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return filtered_lines


###  --------------------------------------------------------------------------------
@st.cache_data
def calculate_rotation_angle(img_array, edge_distance=1):

    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    dilated_edges = cv2.dilate(edges, None)

    # Find contours of dilated edges
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_img = np.zeros_like(img_array)
    cv2.drawContours(contour_img, contours, -1, (255, 255, 255), thickness=edge_distance)

    # Convert the contour image to grayscale
    contour_gray = cv2.cvtColor(contour_img, cv2.COLOR_RGB2GRAY)
    lines = cv2.HoughLines(contour_gray, 1, np.pi / 180, threshold=120)
    
    # Draw lines on the image and get lines that meet the condition
    line_img = np.zeros_like(img_array)
    filtered_lines = draw_lines(line_img, lines, angle_criteria=(70, 110))

    # Calculate average angle of detected lines
    angles = [angle for _, angle in filtered_lines]
    avg_angle = np.mean(angles) if angles else 0.0
    

    return avg_angle / np.pi * 180.0


###  ------------------------------------------------------------------
@st.cache_data
def remove_table_lines(images_input, horizontal, vertical):
    
    image_input_h, image_input_w = images_input.shape[:-1]
    gray = cv2.cvtColor(images_input.copy(), cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(horizontal), 1))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts_horizontal, _ = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result_horizontal = images_input.copy()
    image_hori = cv2.drawContours(result_horizontal, cnts_horizontal, -1, (255, 255, 255), 4)

    # Detect vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(vertical)))
    detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts_vertical, _ = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result_vertical = images_input.copy()
    image_veri = cv2.drawContours(result_vertical, cnts_vertical, -1, (255, 255, 255), 4)
    image = cv2.bitwise_or(image_hori, image_veri)
    _,image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

    return image


###  ------------------------------------------------------------------
@st.cache_data
def target_separate(input_image, axis):
    
    input_image_h, input_image_w = input_image.shape[:-1] 
    image_input = input_image #[10:input_image_h-10 , 10:input_image_w-10].copy()  
    gray_image = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY)
    _, black_image  = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

    
    if axis == 0: sum_value = (np.sum(black_image, axis=0)*100)/(255.*input_image_h)
    else:         sum_value = (np.sum(black_image, axis=1)*100)/(255.*input_image_w)
    
    criteria_pre = []
    for ii in range (0, int(len(sum_value))):
        if sum_value[ii] < int(40):
            sum_value[ii] = 0
        else: 
            sum_value[ii] = 10
        criteria_pre.append(sum_value[ii])

                           
    posi_values = np.where(sum_value< int(10))     
    target_crop = [input_image_h] 
    for value in range (0, len(posi_values[0])-1):
        if value == 0:
            if (posi_values[0][0] != 0):
                target_crop.append(0)
                target_crop.append(posi_values[0][0])
        elif (value != 0) & (value < len(posi_values[0])-1):
            if (posi_values[0][value+1] - posi_values[0][value] == 1) & ((posi_values[0][value] - posi_values[0][value-1] == 1)):
                pass
            else: 
                if (posi_values[0][value] < 2500):
                    target_crop.append(posi_values[0][value]) 
                         
    target_crop = np.sort(target_crop)

    return target_crop


###  ------------------------------------------------------------------
@st.cache_data
def PaddleOCR_image(image_row, custom_bin_edges):
    
    # image_h, image_w = image_row.shape[:-1]
    image_input = cv2.erode(image_row, np.ones((3, 3), np.uint8) , iterations = 2) 

    ocr = PaddleOCR(lang='en')
    result = ocr.ocr(image_input, cls=False) 
    if (result[0]) is not None: 
        # Extract detected text and bounding box coordinates and store them in the DataFrame
        data = []
        for idx, res in enumerate(result):
            for line in res:
                text = line[1][0]
                box = line[0]
                conf = line[1][1]
                data.append({'Text': text, 'X1': box[0][0], 'Y1': box[0][1], 'Conf': conf})  #'X2': box[2][0], 'Y2': box[2][1]
            
        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by = ['X1']).reset_index(drop=True)


        # Loop to check and adjust rows of data along break lines
        for i, threshold in enumerate(custom_bin_edges):
            # Check the data in column 'Y1' and ensure that the rows are lined up correctly.
            df_sorted.loc[df_sorted['X1'] > threshold, 'Row'] = int(i + 1)
  
        df_row = df_sorted.groupby('Row').apply(lambda x: x.sort_values(by='Y1')).reset_index(drop=True)
        df_select = df_row[['Text', 'Conf']]       
    else:
        pass
    return df_select

###  ------------------------------------------------------------------