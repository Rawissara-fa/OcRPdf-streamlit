# ----- Save to MySQL DB -----
import mysql.connector
from mysql.connector import errorcode
import os

from datetime import datetime
import streamlit as st
import fitz  # PyMuPDF
import components.ocr2result_pe as ocr2result_pe




@st.cache_data
def result2db (main_folder_path, sub_folders, table_col_name, update_db):
    
    # ----- Config -----
    # Table Result
    table = 'an_pkg_report'# 'an_sw_datasw_result' #'an_lnc_datasw_result'


    # MySQL server details
    host = '192.168.2.99'
    user = 'usrrw'
    password = 'activerw'  #rd
    database = 'pe_db'

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
        files = os.listdir(os.path.join(main_folder_path, sub_folders))

        # Loop df from file
        for file in files:

            fol_chk = os.path.join(main_folder_path, sub_folders) 
            file_path_to_chk = os.path.join(fol_chk, file)
            print(file_path_to_chk)
            
            try:
                print(f'Computing... : {file_path_to_chk}')
        
                # Check file existing
                if os.path.isfile(file_path_to_chk):
                    print(f"Found: {file_path_to_chk}")
                    
                    ## ------------------------------------------------------- add code
                    with fitz.open(file_path_to_chk) as pdf_document:
                        page_number = pdf_document.page_count 

                    for i in range(page_number):
                        
                        # cursor.execute("select now()")
                        # tim = cursor.fetchone()
                        # print(tim)
                        current_today = datetime.now()
                        current_folder = str(current_today).split(".")[0]
                        
                        ## read (specific) au line
                        ## st.dataframe(results).T
                        results, status_file = ocr2result_pe.extract_text_from_pdf(file_path_to_chk, i, current_folder)
                        # st.text(opening)
                        # print(status_file)
        
                        # INSERT statement
                        insert_query = f"INSERT INTO {table} ({', '.join(table_col_name)}) VALUES ({', '.join(['%s'] * len(table_col_name))})"                  
                        
                        # All data to insert
                        data = results # list following column name
                        data_to_insert = tuple(str(val) for val in data) # value to string
                        print(data_to_insert)

                        # update data
                        if update_db == True:
                            # cursor.execute(insert_query, data_to_insert)
                            status_db = '...... inserted successfully'
                            st.text((status_file +status_db))
                        elif update_db == False:
                            status_db = '...... and not inserted yet'
                            st.text((status_file +status_db))
                        else:
                            st.warning(("Try again" +status_file))

                    # Commit the transaction
                    connection.commit()
                    # print("Data inserted successfully!")
                
                else:
                    print(f"Error: file not found: {file_path_to_chk}")
                
            except Exception as ex:
                print(f'Error: {file_path_to_chk} \nMessage: {ex}')
        
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