cols_lst = ['month_key', 'payment_type', 'ma_giao_dich', 'ngay_giao_dich', 'merchant_ref', 'status']
payment_type = ['MOMO', 'GOOGLE', 'VNPAY', 'ASIAPAY']
momo = "A,B,F"
google = "A,B,D"
vnpay = "A,B,K"
asiapay = "A,B,G,Q"
trans_not_pay_gate_cols = ['month_key', 'transaction_id', 'origin_subscription_id', 'payment_type', 'plan_id',
                           'title_name', 'paid_price', 'payment_charge_id', 'partner_trans_id', 'create_at',
                           'ket_qua_doi_soat', 'merchant_ref', 'active_type']
trans_not_glx_cols = ['month_key', 'ma_giao_dich', 'payment_type', 'ket_qua_doi_soat', 'chi_tiet',
                      'merchant_ref', 'transaction_id_glx', 'created_at_glxp', 'created_at_ctt']
trans_path = "data_check_transaction"


class StagingDB:
    USER = 'report'
    PW = 'mCVMtqJ6tfn5cHfQYz'
    HOST = '10.10.25.84'
    PORT = '5432'
    DB = 'report'


class Config:
    def __init__(self, DB_id):
        self.db_id = DB_id

    def get_config(self):
        if self.db_id == 'Staging':
            return StagingDB
