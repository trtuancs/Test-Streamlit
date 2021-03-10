import streamlit as st
import pandas as pd
import base64
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx"> {}</a>'.format('test') # decode b'abc' => abc



st.title('Wellcome to CHECK TOOL')
option = st.selectbox("Please select your option: ", 
                    ['Check Transaction', 'Check VMG'])
if option == 'Check Transaction':
    st.text("You are using Check Transaction Function")
    month_key = st.text_input("Enter month_key") 
    # st.button('Add file transaction to check')
    file_input = st.file_uploader("Upload File Transaction",type=['xlsx'])
    if file_input is not None:
        st.text("We are checking month_key: {}".format(month_key))
        df2 = pd.read_excel(file_input,'MOMO',usecols="A,B,F",dtype=str).astype(str)
        st.markdown(get_table_download_link(df2), unsafe_allow_html=True)