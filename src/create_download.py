import base64
from io import BytesIO
import pandas as pd


class CreateDownload:
    def __init__(self, data, name, desc):
        self.data = data
        self.name = name
        self.desc = desc

    def __to_excel(self):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        self.data.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        processed_data = output.getvalue()
        return processed_data

    def process(self):
        val = self.__to_excel()
        b64 = base64.b64encode(val)  # val looks like b'...'
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{self.name}.xlsx"> {self.desc}</a>'
