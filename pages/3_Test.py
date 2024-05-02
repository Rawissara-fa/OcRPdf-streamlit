import streamlit as st
from streamlit import session_state as ss
import pandas as pd


# data = {
#     'Name': ['AAA', 'BBB', 'CCC'],
#     'Pay Due': [200, 200, 200],
#     'Pay Amount': [50, 50, 50],
#     'Pay Balance': [0, 0, 0]
# }


# if 'df' not in ss:
#     ss.df = pd.DataFrame(columns=list(data.keys()))


# def change():
#     # Get the edited row index, column name and value.
#     er = ss.pay['edited_rows']
#     affected_index = list(er.keys())[0]
#     affected_pay_amount = er[affected_index]['Pay Amount']

#     # Update the pay amount at the affected index.
#     ss.df.at[affected_index, 'Pay Amount'] = affected_pay_amount    

#     # Calculate the new value for pay balance at the affected index.
#     pay_bal = ss.df.at[affected_index, 'Pay Amount'] - ss.df.at[affected_index, 'Pay Due']

#     # Update the value of pay_bal at the affected index.
#     ss.df.at[affected_index, 'Pay Balance'] = pay_bal


# def main():
#     if not len(ss.df):
#         ss.df = pd.DataFrame(data)

#     st.data_editor(ss.df, hide_index=True, on_change=change, key='pay')
    
#     print(ss.df)
#     savedata = ss.df.to_dict()
#     # if st.button(label="Save Data"):
#     #     st.success("Data saved")
#     #     with open("Save_dataframe.json", "w") as data:
#     #         json.dump(savedata, data)
#     st.json(savedata)

# if __name__ == '__main__':
#     main()
    
    #st.session_state.df.reset_index(drop=True, inplace=True)
    
###------------------------------------------------------------------------------------------------


# if st.button("Notes"):
#     notes = "Notes:- "
#     with st.sidebar:
#         st.title("Notes")
#         st.text_area("Text", notes, height=300)
#         st.download_button(
#             label="Download Notes",
#             data=notes,
#             file_name="my_notes.txt")

# st.title("Notes")
# notes = st.text_area("Text", "Notes:- ", height=300)
# st.download_button(label="Download Notes", data=notes, file_name="my_notes.txt")


# {'Column 1': [None, None], 'Column 2': [None, None], 'Column 3': [None, None], 'Column 4': [None, None]}
columns = 3
rows = 5
data = {'Column {}'.format(i+1): [None] * rows for i in range(columns)}

info = []
for key in data:
    info.append({
        'header': key,
        'detail': data[key],
    })
# for key in data:
#     content_dict = {}
#     for i in range(rows):
#         content_dict['content {}'.format(i+1)] = data[key][i]
#     info.append({
#         'header': key,
#         **content_dict
#     })
# st.text(info)

# # Writing to a text file
# with open('output.txt', 'w') as file:
#     for item in info:
#         file.write(str(item) + '\n')


# import ast
# loaded_info = []
# with open('output.txt', 'r') as file:
#     for line in file:
#         # Convert each line (which contains a string representation of a dictionary) back to a dictionary
#         loaded_info.append(ast.literal_eval(line.strip()))
# st.text(loaded_info)
        
        
        
        
        
        
        
        
        
# st.title("Notes")
notes = ["Header name : " + item['header'] + "\n        ,detail : " + ', '.join(str(header) for header in item['detail']) for item in info]
# edit_note = st.text_area("Text", "\n".join(notes), height=300)

# edit_note = "".join(edit_note.replace("\n", " "))

# key1 = "Header name :"
# key2 = ",detail :"
# parts = edit_note.split(key1)

# split_data = []
# for part in parts:
#     split_data.extend(part.split(key2))

# # Remove empty strings from the list
# my_list = [item.strip() for item in split_data if item.strip()]

# # st.text(data)
# # st.text(my_list)

# # my_dict = {my_list[i]: [my_list[i + 1]] for i in range(0, len(my_list), 2)}
# my_dict = {}
# i = 0
# while i < len(my_list):
#     column = my_list[i]
#     rows = my_list[i + 1]
#     rows_list = [row.strip(" []") for row in rows.strip(" []").split(",")]
#     my_dict[column] = rows_list
#     i += 2

# st.data_editor(pd.DataFrame(my_dict), num_rows="fixed",hide_index=False, key='demo_df')
# st.text(my_dict)
# # for seq in 




notes = "Header name"

if "text" not in st.session_state:
    st.session_state["text"] = ""
text1 = st.text_area('Text : ', st.session_state["text"])
before = st.text_input('Before', value = notes)
after = st.text_input('After')
button = st.button('Button')

if button:
    st.session_state["text"] = text1.replace(before, after)
    st.rerun()