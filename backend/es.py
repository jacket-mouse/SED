
from elasticsearch import Elasticsearch, helpers
import csv
import traceback
import os
import preprocess
from colorama import Fore, Back, Style
from elasticsearch.helpers import BulkIndexError
from tqdm import tqdm

es = Elasticsearch(["http://localhost:9200"])

# 删除对应名称的索引
def delete_index(index_name):
    response = es.indices.delete(index=index_name)
    # 检查删除是否成功
    if response.get('acknowledged'):
        print(Fore.GREEN + f"Index '{index_name}' deleted successfully")
    else:
        print(Fore.GREEN + f"Failed to delete index '{index_name}'")

# 给文件添加索引
def add_index(file_path):
    file_extension = os.path.splitext(file_path)[1]
    print(Fore.GREEN + f"file_extension = {file_extension}")
    if file_extension == ".xls" or file_extension == ".xlsx":
        excel_import(file_path)
    elif file_extension == ".csv":
        csv_import(file_path)
    elif file_extension == ".txt":
        txt_import(file_path)

# 格式化输出查询结果
def format_output(response):
    if 'hits' in response and 'hits' in response['hits']:
        for hit in response['hits']['hits']:
            doc_id = hit['_id']
            score = hit['_score']
            source = hit['_source']
            
            print(Fore.GREEN + f"Document ID: {doc_id}")
            print(Fore.GREEN + f"Score: {score}")
            print(Fore.GREEN + "Source Data:")
            for key, value in source.items():
                print(Fore.GREEN + f"  {key}: {value}")
    else:
        print(Fore.GREEN + "No results found.") 

# 拼接输出结果为字符串列表
def format_output_toString(response):
    if 'hits' in response and 'hits' in response['hits']:
        results = []
        for hit in response['hits']['hits']:
            doc_id = hit['_id']
            score = hit['_score']
            source = hit['_source']
            result = ""
            print(Fore.GREEN + f"Document ID: {doc_id}")
            print(Fore.GREEN + f"Score: {score}")
            print(Fore.GREEN + "Source Data:")
            for key, value in source.items():
                result = result + (f"  {key}: {value}")
            results.append(result)
        return results
    else:
        return("No results found.") 
    
# 根据索引名获取该索引全部字段        
def get_fields(index_name):
    mapping = es.indices.get_mapping(index=index_name)
    fields = []
    for field, properties in mapping[index_name]['mappings']['properties'].items():
        print(Fore.GREEN + f"字段名称: {field}")
        fields.append(field)
    return fields
        
# 获取全部索引名
def get_index_names():
    indices = es.indices.get_alias(index="*")
    return list(indices.keys())

def search(info):
    index_names = get_index_names()
    for name in index_names:  
        query = {
            "query": {
                "query_string": {
                    "query": "*"+info+"*"
                }
            }
        }
        response = format_output_toString(es.search(index=name, body=query))
        format_output(response)
        return response
     
def excel_import(file_path):
    sheet_names = preprocess.excel_csv(file_path)
    for sheet_name in sheet_names:
       sheet_name = "./csv/"+sheet_name+".csv"
       csv_import(sheet_name)
    
def csv_import(file_path):
    try:
        file_basename = os.path.basename(file_path).split(".")[0]
        file_basename = file_basename.lower()
        print(Fore.GREEN + f"file_basename = {file_basename}")
        actions = []
        i = 1
        with open(file_path, encoding='utf-8') as reader:
            csv_reader = csv.reader(reader)
            headers = next(csv_reader)
            header_list = list(headers)
            print(header_list)
            for line in csv_reader:
                try:
                    # Create a document action for each row
                    action = {
                        "_index": file_basename,
                        "_id": i,
                        "_source": {
                            header_list[j]: line[j] for j in range(len(header_list))
                        }
                    }
                    actions.append(action)
                    i += 1

                    # Bulk insert every 500 rows
                    if len(actions) == 100:
                        try:
                            helpers.bulk(es, actions, raise_on_error=True)
                            actions.clear()
                        except BulkIndexError as bulk_error:
                            print(f"批量导入过程中出错：{bulk_error}")
                            for error in bulk_error.errors:
                                print("错误详情:", error)
                except IndexError:
                    print(f"Skipping row {i} due to missing fields.")
                    continue

            # 导入剩余的文档
            if actions:
                try:
                    helpers.bulk(es, actions, raise_on_error=True)
                except BulkIndexError as bulk_error:
                    print(f"批量导入过程中出错：{bulk_error}")
                    for error in bulk_error.errors:
                        print("错误详情:", error)

        print(f"{file_path} Data import completed.")

    except Exception as e:
        traceback.print_exc()

def txt_import(file_path):
    try:
        file_basename = os.path.basename(file_path).split(".")[0]
        file_basename = file_basename.lower()
        print(Fore.GREEN + f"file_basename = {file_basename}")
        actions = []
        # 读取文件内容
        file_content = extract_text_from_file(file_path)
        if file_content:
            action = {
                "_index": file_basename,
                "_source": {
                    "file_name": file_basename,
                    "file_path": file_path,
                    "content": file_content
                }
            }
            actions.append(action)
            # 每 100 个文档批量插入到 Elasticsearch
            if len(actions) == 100:
                helpers.bulk(es, actions)
                actions.clear()
        # 插入剩余的文档
        if actions:
            helpers.bulk(es, actions)
    except Exception as e:
            traceback.print_exc()
# 读取 .txt 文件中的文本内容
def extract_text_from_file(file_path):
    lines = ""
    # 按字节读取文件并逐行建立索引
    with open(file_path, 'rb')as file:
        total_lines = sum(1 for _ in file) 
        file.seek(0)  # 将文件指针重置到开头
        # 使用 tqdm 创建进度条
        with tqdm(total=total_lines, desc="Processing lines") as pbar:
            for line_number, line in enumerate(file, start=1):
                line = preprocess.check_code(line)
                lines = lines + line
                pbar.update(1)
    return lines



if __name__ == '__main__':
    # get_index_names()
    raise NotImplementedError