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