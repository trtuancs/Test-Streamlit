import streamlit as st
import csv
import psycopg2
import pandas as pd
from config import *
import os


class ConnDB:
    def __init__(self, Config):
        self.Config = Config

    def create_conn(self):
        try:
            conn = psycopg2.connect(user=self.Config.USER,
                                    password=self.Config.PW,
                                    host=self.Config.HOST,
                                    port=self.Config.PORT,
                                    database=self.Config.DB)
        except:
            st.error("Could not create connect to DB")
        return conn


class FileInputProcessor:

    def __init__(self, file, month_key, pay_lst):
        self.file = file
        self.pay_lst = pay_lst
        self.month_key = month_key

    def process(self):
        result = pd.DataFrame()
        for pay in self.pay_lst:
            if pay == 'MOMO':
                df = self.__momo(pay)
            elif pay == 'GOOGLE':
                df = self.__google(pay)
            elif pay == 'VNPAY':
                df = self.__vnpay(pay)
            elif pay == 'ASIAPAY':
                df = self.__asiapay(pay)
            result = result.append(df)
        return result[cols_lst]

    def __momo(self, name):
        df = self.__read_item(name, momo)
        df['month_key'] = self.month_key
        df['payment_type'] = name
        df['merchant_ref'] = None
        df = df.rename(columns={'Trạng thái': 'status'})
        return df

    def __google(self, name):
        df = self.__read_item(name, google)
        df['month_key'] = self.month_key
        df['payment_type'] = name
        df['merchant_ref'] = None
        df = df.rename(columns={'Financial Status': 'status'})
        return df

    def __vnpay(self, name):
        df = self.__read_item(name, vnpay)
        df['month_key'] = self.month_key
        df['payment_type'] = name
        df['merchant_ref'] = None
        df = df.rename(columns={'Trạng thái': 'status'})
        return df

    def __asiapay(self, name):
        df = self.__read_item(name, asiapay)
        df['month_key'] = self.month_key
        df['payment_type'] = name
        df = df.rename(columns={'Merchant Ref.': 'merchant_ref', 'Status': 'status'})
        return df

    def __read_item(self, name, cols: str):
        df = pd.read_excel(self.file, name, usecols=cols, dtype=str).astype(str)
        return df

    def save_csv_local(self, dataframe: pd.DataFrame):
        path = os.getcwd()
        dataframe.to_csv(f"{path}/{self.month_key}.csv", index=False, header=True)

    def clean_local(self):
        path = os.getcwd()
        os.remove(f"{path}/{self.month_key}.csv")


class DBProcessor:
    def __init__(self, month_key):
        self.month_key = month_key

    def process(self, conn):
        self.__delete_old_data(conn)
        self.__insert_data(conn)

    def __delete_old_data(self, conn):
        cur = conn.cursor()
        cur.execute(f"DELETE FROM hd1report_db.data_congthanhtoan WHERE month_key={self.month_key}")
        conn.commit()

    def __insert_data(self, conn):
        path = os.getcwd()
        cur = conn.cursor()
        with open(f"{path}/{self.month_key}.csv", 'r') as f:
            reader = csv.reader(f)
            next(reader)
            cur.copy_from(f, "hd1report_db.data_congthanhtoan",
                          columns=(
                              'month_key', 'payment_type', 'ma_giao_dich', 'ngay_giao_dich', 'merchant_ref', 'status'),
                          sep=",")
        conn.commit()


class CheckTransactionProcessor:
    def __init__(self, conn, month_key):
        self.conn = conn
        self.month_key = month_key

    def check_not_pay_gate(self):
        conn = self.conn
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM public.doi_soat_transaction_not_exist_in_payment_data_monthly({self.month_key})")
        result = cur.fetchall()
        df = pd.DataFrame(result, columns=trans_not_pay_gate_cols)
        self.conn.commit()
        return df

    def check_not_glx(self):
        conn = self.conn
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM public.doi_soat_glx_transaction_monthly({self.month_key})")
        result = cur.fetchall()
        df = pd.DataFrame(result, columns=trans_not_glx_cols)
        self.conn.commit()
        return df
