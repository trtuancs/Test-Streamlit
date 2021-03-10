import streamlit as st
import pandas as pd
from result import *


st.title('Wellcome to CHECK TOOL')
option = st.selectbox("Please select your option: ", 
                    ['Check Transaction', 'Check VMG'])
if option == 'Check Transaction':
    st.text("You are using Check Transaction Function")
    month_key = st.text_input("Enter month_key") 
    file_input = st.file_uploader("Upload File Transaction",type=['xlsx'])
    if file_input is not None:
        if st.button('Begin checking'):
            st.text("We are checking month_key: {}".format(month_key))
            df2 = pd.read_excel(file_input,'MOMO',usecols="A,B,F",dtype=str).astype(str)
            st.markdown(get_table_download_link(df2,'result','result'), unsafe_allow_html=True)