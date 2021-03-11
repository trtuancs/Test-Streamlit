from sqlalchemy import create_engine
import csv
import psycopg2
import pandas as pd
import os

cols_lst = ['month_key','payment_type','ma_giao_dich','ngay_giao_dich','merchant_ref','status']
class ConnDB:
    def __init__(self,Config):
        self.Config = Config
    def create_conn(self):
        try:
            conn = psycopg2.connect(user = self.Config.USER,
                               password = self.Config.PW,
                               host = self.Config.HOST,
                               port = self.Config.PORT,
                               database = self.Config.DB)
            print("Create Connect is success")
        except:
            raise Exception('Could not create connect to DB')
        return conn

def preprocessing(file: pd.io.excel._base.ExcelFile)-> pd.DataFrame:
    try:
        payment_type = 'CCSTRIPE'
        df1 = pd.read_excel(file, 'CCSTRIPE',usecols="A,B",dtype=str).astype(str)
        df1['month_key'] = month_key
        df1['payment_type'] = payment_type
        df1['merchant_ref'] = None
        df1['status'] = None
    except:
        df1 = []
        print(payment_type,' missed.')
    
    try:
        payment_type = 'MOMO'
        df2 = pd.read_excel(file,'MOMO',usecols="A,B,F",dtype=str).astype(str)
        df2['month_key'] = month_key
        df2['payment_type'] = payment_type
        df2['merchant_ref'] = None
        df2 = df2.rename(columns = {'Trạng thái':'status'})
        df2 = df2.append(df1)
    except:
        df2 = df1
        print(payment_type,' missed.')

    try:
        payment_type = 'GOOGLE'
        df3 = pd.read_excel(file,'GOOGLE',usecols="A,B,D",dtype=str).astype(str)
        df3['month_key'] = month_key
        df3['payment_type'] = payment_type
        df3['merchant_ref'] = None
        df3 = df3.rename(columns = {'Financial Status':'status'})
        df3 = df3.append(df2)
    except:
        df3 = df2
        print(payment_type,' missed.')

    try:
        payment_type = 'VNPAY'
        df4 = pd.read_excel(file,'VNPAY', usecols="A,B,K",dtype=str).astype(str)
        df4['month_key'] = month_key
        df4['payment_type'] = payment_type
        df4['merchant_ref'] = None
        df4 = df4.rename(columns = {'Trạng thái':'status'})
        df4 = df4.append(df3)
    except:
        df4 = df3
        print(payment_type,' missed.')

    try:
        payment_type = 'ASIAPAY'
        df5 = pd.read_excel(file,'ASIAPAY', usecols="A,B,G,Q",dtype=str).astype(str)
        df5['month_key'] = month_key
        df5['payment_type'] = payment_type
        df5 = df5.rename(columns={'Merchant Ref.':'merchant_ref','Status':'status'})
        df5 = df5.append(df4)
    except:
        df5 = df4
        print(payment_type,' missed.')
    
    # df5 = df5.loc[:,cols_lst]
    return df5

def save_csv_local(dataframe: pd.DataFrame,month_key):
    dataframe.to_csv(f"file/data_check_transaction_{month_key}.csv",index = False, header=True)

def delete_old_data(conn):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM hd1report_db.data_congthanhtoan WHERE month_key={month_key}")
    conn.commit()

def insert_data(conn,month_key):
    # insert data den doi soat
    cur = conn.cursor()
    with open(f"file/data_check_transaction_{month_key}.csv", 'r') as f:
        reader = csv.reader(f)
        next(reader) # Skip the header row.
        cur.copy_from(f,"hd1report_db.data_congthanhtoan", columns = ('month_key','payment_type','ma_giao_dich','ngay_giao_dich','merchant_ref','status'), sep=",")
        print('Data inserted.')
    conn.commit()

def convert_to_csv_congthanhtoan_glxp(data):
    df = pd.DataFrame(data, columns = ['month_key','ma_giao_dich', 'payment_type', 'ket_qua_doi_soat', 'chi_tiet','merchant_ref', 'transaction_id_glx', 'created_at_glxp','created_at_ctt'])
    return df
def doi_soat_congthanhtoan_glxp(conn,month_key):
    # run ham chay doi soat
    print('Bat dau doi soat...')
    cur1 = conn.cursor()
    cur1.execute(f"SELECT * FROM public.doi_soat_glx_transaction_monthly({month_key})")
    columns = [i[0] for i in cur1.description]
    result_doisoat = cur1.fetchall()
    df = convert_to_csv_congthanhtoan_glxp(result_doisoat)
    print("1. Doi soat xong phan data co o cong thanh toan nhung ko co o GLXP")
    print("Doi soat xong 1 chieu.")
    conn.commit()
    return df

def convert_to_csv_glxp_congthanhtoan(data):
    df = pd.DataFrame(data, columns = ['month_key', 'transaction_id', 'origin_subscription_id', 'payment_type', 'plan_id', 'title_name', 'paid_price', 'payment_charge_id', 'partner_trans_id', 'create_at','recheck','merchant_ref'])
    return df
# giao dich co o GLXP nhung ko co o cong thanh toan.
def doi_soat_glxp_congthanhtoan(conn,month_key):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM public.doi_soat_transaction_not_exist_in_payment_data_monthly({month_key})")
    columns = [i[0] for i in cur.description]
    result_doisoat = cur.fetchall()
    df = convert_to_csv_glxp_congthanhtoan(result_doisoat)
    print("2. Doi soat xong phan data co trong GLXP nhung ko co trong data cong thanh toan.")
    print("Doi soat xong chieu nguoc lai.")
    print("Hoan thanh Doi soat !")
    conn.commit()
    return df