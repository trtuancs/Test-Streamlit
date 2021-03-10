import streamlit as st
import os
import pandas as pd

st.title('Wellcome to CHECK TOOL')
option = st.selectbox("Please select your option: ", 
                    ['Check Transaction', 'Check VMG'])
if option == 'Check Transaction':
    st.subheader("You are using Check Transaction Function")
    month_key = st.text_input("Enter month_key") 
    # st.button('Add file transaction to check')
    file_input = st.file_uploader("Upload File Transaction",type=['xlsx'])
    if file_input is not None:
        st.write("OK--------------------------- {}".format(month_key))
        df2 = pd.read_excel(file_input,'MOMO',usecols="A,B,F",dtype=str).astype(str)
        st.table(df2)