import dashscope
import os
from http import HTTPStatus

"""
Hello_Embedding.py
------------------

本脚本演示了如何使用阿里云 DashScope 的 text-embedding-v4 模型对中文文本进行向量化（Embedding），支持单条文本和批量文本的嵌入。

主要功能：
1. embedding_text()：对单条中文文本生成稠密/稀疏向量。
2. embedding_batch_text()：对多条文本批量生成稀疏向量，并合并结果。

依赖环境：
- dashscope
- http (Python 标准库)

output_type 参数说明：
- 用于指定返回的向量类型。
- 可选值：
    - "dense"：仅返回稠密向量（默认）。
    - "sparse"：仅返回稀疏向量。
    - "dense&sparse"：同时返回稠密和稀疏向量。
- 使用场景：
    - 若只需常规 embedding，建议用 "dense"。
    - 若需高效存储或稀疏特征分析，可用 "sparse"。
    - 若需两者兼得，可用 "dense&sparse"。

用法示例：
1. 单条文本嵌入：
    在 main 函数中调用 embedding_text()
2. 批量文本嵌入：
    在 main 函数中调用 embedding_batch_text()

运行方式：
    python Hello_Embedding.py

注意事项：
- 需提前安装 dashscope SDK 并配置好 API Key。
- 返回结果为 dict 类型，访问字段需使用中括号。
- 支持 text-embedding-v3 及 v4 的维度参数。

"""

"""
使用text-embedding-v4 embedding文本
"""
def embedding_text():
    resp = dashscope.TextEmbedding.call(
        model="text-embedding-v4",
        input='衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买',
        dimension=1024,  # 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
        output_type="dense&sparse" #返回结果中是否包含稀疏向量、稠度向量
    )

    #print(resp) 
    if resp["status_code"] == HTTPStatus.OK:
        print(f"\n embedding:{resp['output']['embeddings'][0]['sparse_embedding']}")
    else:
        print(resp)



def embedding_batch_text():
    DASHSCOPE_MAX_BATCH_SIZE = 25

    inputs = ['风急天高猿啸哀', '渚清沙白鸟飞回', '无边落木萧萧下', '不尽长江滚滚来']

    result = None
    batch_counter = 0
    for i in range(0, len(inputs), DASHSCOPE_MAX_BATCH_SIZE):
        batch = inputs[i:i + DASHSCOPE_MAX_BATCH_SIZE]
        resp = dashscope.TextEmbedding.call(
            model="text-embedding-v4",
            input=batch,
            dimension=1024 , # 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
            output_type="sparse" #仅仅返回稀疏向量
        )
        print(f"status:{resp.status_code}")
        if resp.status_code == HTTPStatus.OK:
            if result is None:
                result = resp
            else:
                for emb in resp.output['embeddings']:
                    emb['text_index'] += batch_counter
                    result.output['embeddings'].append(emb)
                result.usage['total_tokens'] += resp.usage['total_tokens']
        else:
            print(resp)
        batch_counter += len(batch)

    print('---------')
    print(result)



if __name__ == "__main__":
    #embedding_text()
    embedding_batch_text()
    print(os.getcwd())
    print(os.getenv("DASHSCOPE_API_KEY"))