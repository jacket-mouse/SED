import pandas as pd
import chardet
import re

def excel_csv(excel_file):
    xls = pd.ExcelFile(excel_file)
    sheet_names = xls.sheet_names
    for sheet_name in sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        df.to_csv(sheet_name, index=False, encoding='utf-8')
        print(f"Excel 文件 '{excel_file}' 已成功转换为 CSV 文件 '{sheet_name}'")
    return sheet_names

def check_code(text):
    adchar = chardet.detect(text)
    if adchar['encoding'] == 'gbk' or adchar['encoding'] == 'GBK' or adchar['encoding'] == 'GB2312':
        true_text = text.decode('GB2312', "ignore")
    else:
        true_text = text.decode('utf-8', "ignore")
    return true_text

# 去除空白符
def remove_whitespace(s):
    parts = s.split('\t')
    new_parts = []
    for part in parts:
         # 移除常见的空白符，包括全角空格
        part = part.replace('\u3000', '')  # 全角空格
        part = re.sub(r'\s+', '', part, flags=re.UNICODE)
        new_parts.append(part)
    return new_parts