from flask import Flask, request, jsonify
from flask_cors import CORS
import parser
import os
import es
import preprocess
import mysql

app = Flask(__name__)
CORS(app)



@app.route('/search', methods=['GET'])
def search():
    searchStr = request.args.get('searchStr', '')
    app.logger.info(f"Received search query: {searchStr}")
    results = parser.search(searchStr)
    # print(results)
    return jsonify(results)

@app.route('/upload', methods=['POST'])
def add_data_source():
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        return "No file part in the request", 400
    file = request.files['file']
    # 检查文件名是否为空
    if file.filename == '':
        return "文件名不能为空", 400
    print(f"File: {file.filename}")
    file_extension = os.path.splitext(file.filename)[1]
    print(f"File extension: {file_extension}")
    file_extension = file_extension.replace('.', '')
    
    if file:
        file_path = (f"./{file_extension}/{file.filename}") 
        file.save(file_path)
        index_dir = "./index/" + file.filename
        if file_extension == 'txt':
            parser.create_index(index_dir, file_path)
        elif file_extension == 'csv' or file_extension == 'xls' or file_extension == 'xlsx':
            es.add_index(file_path)
            mysql.db_import(file_path)
        return "File uploaded successfully", 200

if __name__ == '__main__':
    xlsx_dir = "./xlsx"
    xls_dir = "./xls"
    txt_dir = "./txt"
    csv_dir = "./csv"
    preprocess.mk_dir(xls_dir)
    preprocess.mk_dir(xlsx_dir)
    preprocess.mk_dir(txt_dir)
    preprocess.mk_dir(csv_dir)
    # base_file_path = "./index_data"
    # base_index_path = "./index"
    # txt_files = [ f for f in os.listdir(base_file_path) if f.endswith(".txt")]
    # # 为不同文件添加索引
    # for file in txt_files:
    #     file_path = base_file_path + "/" + file
    #     index_dir = base_index_path + "/" + file
    #     create_index(index_dir, file_path)
    app.run(host='localhost', port=3010)
