import pandas as pd
import chardet
import re
import os

def excel_csv(excel_file):
    xls = pd.ExcelFile(excel_file)
    sheet_names = xls.sheet_names
    for sheet_name in sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        output_csv_path = f"./csv/{sheet_name}.csv"
        df.to_csv(output_csv_path, index=False, encoding='utf-8')
        print(f"Excel 文件 '{excel_file}' 已成功转换为 CSV 文件 '{output_csv_path}'")
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

def mk_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)