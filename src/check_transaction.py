from sqlalchemy import create_engine
import streamlit as st
import csv
import psycopg2
import pandas as pd
import os
from config import *

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
        except:
            st.error("Could not create connect to DB")
        return conn

class Processor:
    def __init__(self,file,month_key,pay_lst):
        self.file = file
        self.pay_lst = pay_lst
        self.month_key = month_key
    
    def process(self):
        result = pd.DataFrame()
        for pay in pay_lst:
            if pay == 'MOMO':
                df = self.momo(pay)
            elif pay == 'GOOGLE':
                df = self.google(pay)
            elif pay =='VNPAY':
                df = self.vnpay(pay)
            elif pay == 'ASIAPAY':
                df = self.asiapay(pay)
            result = result.append(df)
        return result[cols_lst]

    def momo(self,name):
        df = pd.read_excel(self.file,name,usecols=momo,dtype=str).astype(str)
        df['month_key'] = self.month_key
        df['payment_type'] = name
        df['merchant_ref'] = None
        df = df.rename(columns = {'Trạng thái':'status'})
        return df
    
    def google(self,name):
        df = pd.read_excel(self.file,name,usecols=google,dtype=str).astype(str)
        df['month_key'] = self.month_key
        df['payment_type'] = name
        df['merchant_ref'] = None
        df = df.rename(columns = {'Financial Status':'status'})
        return df
    
    def vnpay(self,name):
        df = pd.read_excel(self.file,name, usecols=vnpay,dtype=str).astype(str)
        df['month_key'] = self.month_key
        df['payment_type'] = name
        df['merchant_ref'] = None
        df = df.rename(columns = {'Trạng thái':'status'})
        return df

    def asiapay(self,name):
        df = pd.read_excel(self.file,name, usecols=asiapay,dtype=str).astype(str)
        df['month_key'] = self.month_key
        df['payment_type'] = name
        df = df.rename(columns={'Merchant Ref.':'merchant_ref','Status':'status'})
        return df

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