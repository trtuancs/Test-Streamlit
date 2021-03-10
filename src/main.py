import streamlit as st
import os
import pandas as pd

st.title('Wellcome to CHECK TOOL')
option = st.selectbox("Please select your option: ", 
                    ['Check Transaction', 'Check VMG'])
if option == 'Check Transaction':
    st.subheader("You are using Check Transaction Function")
    if st.button('Add file from account'):
        file_input = st.file_uploader("Upload File",type=['xlsx'])
        if file_input:
            # st.write(str(type(file_input)))
            df2 = pd.read_excel(file_input,'MOMO',usecols="A,B,F",dtype=str).astype(str)
            st.table(df2)