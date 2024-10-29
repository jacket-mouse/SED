from tika import parser
import jieba
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os
from tqdm import tqdm
import preprocess
import es


# 定义索引的 Schema
def create_schema():
    return Schema(line_number=ID(stored=True), content=TEXT(stored=True))

# 创建索引
def create_index(index_dir, file_path):
    print("@" + file_path + " 创建索引中……")
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        schema = create_schema()
        ix = create_in(index_dir, schema)
        writer = ix.writer()
        # 先完成字典加载和其他初始化工作
        jieba.initialize()  # 可以显示加载的步骤，但不会影响后续分词
        print("Jieba initialization completed.")
        # 按字节读取文件并逐行建立索引
        with open(file_path, 'rb')as file:
            total_lines = sum(1 for _ in file) 
            file.seek(0)  # 将文件指针重置到开头
            # 使用 tqdm 创建进度条
            with tqdm(total=total_lines, desc="Processing lines") as pbar:
                for line_number, line in enumerate(file, start=1):
                    line = preprocess.check_code(line)
                    seg_list = jieba.cut(line.strip())
                    segmented_text = " ".join(seg_list)
                    writer.add_document(line_number=str(line_number), content=segmented_text)
                    # 更新进度条
                    pbar.update(1)
        writer.commit()
        print("创建结束" + file_path)

# 搜索功能
def search_index(index_dir, query_str):
    ix = open_dir(index_dir)
    searcher = ix.searcher()
    parser = QueryParser("content", ix.schema)
    query = parser.parse(query_str)
    results = searcher.search(query)
    output = []
    for result in results:
        processed = preprocess.remove_whitespace(result["content"])
         # 将结果转换为一个可 JSON 序列化的列表
        output.append({
            "line_number": result["line_number"],  # 行号
            "content": processed  # 匹配内容
        })
        # 格式化输出结果
        print()
        print(f"匹配结果: {result['line_number']}", end=" ")
        for item in processed:
            print(f"{item}", end=" ")
    return output

def search(searchStr):
    results = es.search(searchStr)
    txt_files = [ f for f in os.listdir("./txt") if f.endswith(".txt")]
    for file in txt_files:
        index_dir = "./index/" + file
        for result in search_index(index_dir, searchStr):
            results.append(result)
    return results

def main():
    # 示例使用
    index_dir = "index"
    file_paths = "2000-1/1-5.txt"  # 你要处理的文件列表

    # 创建索引
    create_index(index_dir, file_paths)

    # 搜索示例
    search_query = "qq"  # 替换为你想要搜索的内容
    search_index(index_dir, search_query)

if __name__ == "__main__":
    main()