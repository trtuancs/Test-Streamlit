from create_download import *
from check_transaction import *
from config import *

st.title('Wellcome to CHECK TOOL')
option = st.selectbox("Please select your option: ",
                      ['Check Transaction', 'Check VMG'])
if option == 'Check Transaction':
    st.text("You are using Check Transaction Function")
    month_key = st.text_input("Enter month_key")
    file_input = st.file_uploader("Upload File Transaction", type=['xlsx'])
    if file_input is not None:
        if st.button('Begin checking'):
            st.text("We are checking month_key: {}".format(month_key))
            config = Config('Staging').get_config()
            conn = ConnDB(config).create_conn()
            PreProcess = FileInputProcessor(file_input, month_key, payment_type)
            df = PreProcess.process()
            PreProcess.save_csv_local(df)
            DBProcessor(month_key).process(conn)
            Check = CheckTransactionProcessor(conn, month_key)
            not_pay_gate = Check.check_not_pay_gate()
            not_glx = Check.check_not_glx()
            st.write("Click below link to download: ")
            not_pay_gate_link = CreateDownload(not_pay_gate, "not_in_pay_gate", "Transaction not in payment gate").process()
            not_glx_link = CreateDownload(not_glx, "not_in_glx", "Transaction not in Galaxy").process()
