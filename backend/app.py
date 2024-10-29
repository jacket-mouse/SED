from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from elasticsearch import Elasticsearch
import parser
import os
import es

app = Flask(__name__)
CORS(app)

# MySQL配置
db = pymysql.connect(host='localhost', user='root', password='admin123', database='bike')

@app.route('/search', methods=['GET'])
def search():
    searchStr = request.args.get('searchStr', '')
    app.logger.info(f"Received search query: {searchStr}")
    results = parser.search(searchStr)
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
        return "File uploaded successfully", 200

if __name__ == '__main__':
    # base_file_path = "./index_data"
    # base_index_path = "./index"
    # txt_files = [ f for f in os.listdir(base_file_path) if f.endswith(".txt")]
    # # 为不同文件添加索引
    # for file in txt_files:
    #     file_path = base_file_path + "/" + file
    #     index_dir = base_index_path + "/" + file
    #     create_index(index_dir, file_path)
    app.run(host='localhost', port=3010)
