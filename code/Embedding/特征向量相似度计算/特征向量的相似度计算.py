import numpy as np

"""
对向量进行余弦相似度计算
"""

def cosine_similarity(vec1, vec2):
    """
    计算两个向量的余弦相似度。
    :param vec1: 一维numpy数组或列表
    :param vec2: 一维numpy数组或列表
    :return: 余弦相似度（-1到1之间）
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)

# 示例
if __name__ == "__main__":
    v1 = [1, 2, 3, 7, 8, 23, 54]
    v2 = [4, 5, 6, 18, 96, 33, 55]
    sim = cosine_similarity(v1, v2)
    print(f"向量 {v1} 和 {v2} 的余弦相似度为: {sim:.4f}") 