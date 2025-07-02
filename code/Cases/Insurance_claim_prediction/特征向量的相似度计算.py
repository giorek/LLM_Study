import numpy as np

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

def euclidean_distance(vec1, vec2):
    """
    计算两个向量的欧氏距离。
    :param vec1: 一维numpy数组或列表
    :param vec2: 一维numpy数组或列表
    :return: 欧氏距离（>=0）
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.linalg.norm(vec1 - vec2)

def euclidean_similarity(vec1, vec2):
    """
    基于欧氏距离计算两个向量的相似度（归一化，值域0~1，越大越相似）。
    :param vec1: 一维numpy数组或列表
    :param vec2: 一维numpy数组或列表
    :return: 欧氏距离相似度（0~1）
    """
    dist = euclidean_distance(vec1, vec2)
    return 1 / (1 + dist)

# 示例
if __name__ == "__main__":
    v1 = [1, 2, 3]
    v2 = [4, 5, 6]
    sim = cosine_similarity(v1, v2)
    dist = euclidean_distance(v1, v2)
    sim_euc = euclidean_similarity(v1, v2)
    print(f"向量 {v1} 和 {v2} 的余弦相似度为: {sim:.4f}")
    print(f"向量 {v1} 和 {v2} 的欧氏距离为: {dist:.4f}")
    print(f"向量 {v1} 和 {v2} 的欧氏距离相似度为: {sim_euc:.4f}") 