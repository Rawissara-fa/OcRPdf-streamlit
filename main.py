# import yaml
import streamlit as st
import requests




st.set_page_config(page_title="Home", page_icon="👋",layout="wide")
st.write("# H e LL O! 👋")


st.markdown("_________________________________________________")

if st.session_state is None:
    st.session_state = {}

        
cols1, cols2 = st.columns([1 ,1])
with cols1:

     
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Sign in")
    
    
    if login_btn:
        # send api to fft security system
        SECURITY_API = "http://192.168.1.235:7010/api/security-center/SignIn"
        
        login_data_json = {
            "USER_NAME": username,
            "USER_PASSWORD": password
            }

        login_response = requests.post(url = SECURITY_API, 
                                       json = login_data_json).json()
        # print(login_response)
        print("-------------------------------------------------------------------------")
            
        
        if login_response["Status"] is True:
            login_user = login_response["ResultOnDb"][0]
            st.session_state["login_user"] = {"Status": login_response["Status"],
                                              "TITLE_OF_COURTESY_NAME": login_user["TITLE_OF_COURTESY_NAME"],
                                              "EMPLOYEE_CODE"         : login_user["EMPLOYEE_CODE"],
                                              "FIRST_NAME"            : login_user["FIRST_NAME"],
                                              "SECTION_NAME"          : login_user["SECTION_NAME"],
                                            }
            
            st.sidebar.write("Welcome: "+st.session_state["login_user"]["TITLE_OF_COURTESY_NAME"] +st.session_state["login_user"]["FIRST_NAME"]+ \
                    "\n"+ "Department: " + st.session_state["login_user"]["SECTION_NAME"])
            print("User login: " +st.session_state["login_user"]["EMPLOYEE_CODE"])
        
            logout_btn = st.sidebar.button("Logout")
            if logout_btn:
                print("User logout")
                st.session_state["login_user"]["Status"] = False
                st.rerun()
            st.success('User Login successfully')
        elif login_response["Status"] is False:
            st.error('Username/password is incorrect')
        else:
            st.error(login_response["Message"])
        
        
        





# https://stackoverflow.com/questions/57361723/error-when-pull-or-push-to-git-enoent-no-such-file-or-directory

# -----------------------------------------
  ## OPen streamlit app
#------------------------------------------

# C:/Users/rawissara.bua/AppData/Local/anaconda3/Scripts/activate
# conda activate pyocr_ver3
# streamlit run main.py
# PS(XXX) python -m streamlit run main.py