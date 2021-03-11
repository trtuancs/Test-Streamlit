import streamlit as st
import pandas as pd
from create_download import *
from check_transaction import *
from config import *


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
            config = Config('Staging')
            conn = ConnDB(config)
            # st.text("Xong conn")
            df = pd.read_excel('GOOGLE','GOOGLE',usecols=google,dtype=str).astype(str)
            st.write(df)
            # save_csv_local(df,month_key)
            # delete_old_data(conn)
            # insert_data(conn,month_key)
            # not_glx_df = doi_soat_congthanhtoan_glxp(conn,month_key)
            # not_gateway = doi_soat_glxp_congthanhtoan(conn,month_key)
            # st.markdown(get_table_download_link(not_glx_df,'not_glx','Transaction has at payment gateway - not at glx'), unsafe_allow_html=True)
            # st.markdown(get_table_download_link(not_gateway,'not_gateway','Transaction has at glx - not at gateway'), unsafe_allow_html=True)