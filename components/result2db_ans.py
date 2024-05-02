# ----- Save to MySQL DB -----
import mysql.connector
from mysql.connector import errorcode
import os

import streamlit as st
import fitz  # PyMuPDF
# import components.ocr2result_adhesive as ocr2result




@st.cache_data
def result2db(data_to_insert, table_col_name, update_db):   #(results[num], table_col_name, update_db)
    
    # ----- Config -----
    # Table Result
    table = 'an_adhesive_report' # 'an_sw_datasw_result' #'an_lnc_datasw_result'
    # print(f"main foder :  {main_folder_path} \nsub floder : {sub_folders}")


    # MySQL server details
    host = '192.168.2.99'
    user = 'usrrw'
    password = 'activerw'  #rd
    database = 'adhesive_db'

    # --------------------
                
    # Create a connection to the MySQL server
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        try:
            # print(f'Computing... : {file_path_to_chk}')
            
            # st.text(f"--> {status_file} {status_db}")
            if update_db == True:
                data  = data_to_insert
                data_to_insert = tuple(str(val) for val in data) # value to string
                
                # INSERT statement
                insert_query = f"INSERT INTO {table} ({', '.join(table_col_name)}) VALUES ({', '.join(['%s'] * len(table_col_name))})"
                # cursor.execute(insert_query, data_to_insert)
                status_db = '...... inserted successfully'
            elif update_db == False:
                status_db = '...... and not inserted yet' 
            else:
                status_db = "Try again"
                
            # st.text(f"{status_file} {status_db}")



            # Commit the transaction
            connection.commit()
            # print("Data inserted successfully!")
            return (status_db)

            
        except Exception as ex:
            print(f'Error: \nMessage: {ex}')
            # print(f'Error: {file_path_to_chk} \nMessage: {ex}')
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: The specified database does not exist.")
        else:
            print("Error:", err)

    finally:
        print("Finally: ")
        # Close the cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
            print("Closed")
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Closed")
