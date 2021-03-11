cols_lst = ['month_key','payment_type','ma_giao_dich','ngay_giao_dich','merchant_ref','status']
payment_type = ['MOMO','GOOGLE','VNPAY','ASIAPAY']
momo = "A,B,F"
google = "A,B,D"
vnpay = "A,B,K"
asiapay = "A,B,G,Q"


class StagingDB:
    USER = 'report'
    PW = 'mCVMtqJ6tfn5cHfQYz'
    HOST = '10.10.25.84'
    PORT = '5432'
    DB = 'report'

class Config:
    def __init__(self,DB_id):
        self.db_id = DB_id
    
    def get_config(self):
        if self.db_id == 'Staging':
            return StagingDB