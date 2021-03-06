from create_download import *
from check_transaction import *
from config import *

CHOICES = {1: "Check Transaction", 2: "Check VMG"}


def format_func(option):
    return CHOICES[option]


st.title('Welcome to CHECK TOOL')
option = st.selectbox("Please select your option: ",
                      options=list(CHOICES.keys()), format_func=format_func)
if option == 1:
    st.info("You are using Check Transaction Function")
    month_key = st.text_input("Enter month_key")
    file_input = st.file_uploader("Upload File Transaction", type=['xlsx'])
    if (file_input is not None) and (month_key != ""):
        if st.button('Begin checking'):
            with st.spinner("We are checking month_key: {} ...".format(month_key)):
                config = Config('Staging').get_config()
                conn = ConnDB(config).create_conn()
                PreProcess = FileInputProcessor(file_input, month_key, payment_type)
                df = PreProcess.process()
                PreProcess.save_csv_local(df)
                DBProcessor(month_key).process(conn)
                Check = CheckTransactionProcessor(conn, month_key)
                not_pay_gate = Check.check_not_pay_gate()
                not_glx = Check.check_not_glx()
                not_pay_gate_link = CreateDownload(not_pay_gate, "not_in_pay_gate",
                                                   "Transactions not in payment gate").process()
                not_glx_link = CreateDownload(not_glx, "not_in_glx", "Transactions not in Galaxy").process()
                PreProcess.clean_local()
                st.success("Processing is success - Click below link to download: ")
                st.markdown(not_pay_gate_link, unsafe_allow_html=True)
                st.markdown(not_glx_link, unsafe_allow_html=True)
elif option == 2:
    st.header("This function are maintenance")
