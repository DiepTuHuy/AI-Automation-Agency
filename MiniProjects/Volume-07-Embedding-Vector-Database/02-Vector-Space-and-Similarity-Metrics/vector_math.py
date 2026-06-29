import numpy as np

def calculate_metrics(v1, v2):
    a = np.array(v1)
    b = np.array(v2)
    
    # 1. Tính khoảng cách Euclidean
    euclidean_dist = np.linalg.norm(a - b)
    
    # 2. Tính Cosine Similarity
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    cosine_sim = dot_product / (norm_a * norm_b)
    
    print(f"Vector A: {v1}")
    print(f"Vector B: {v2}")
    print(f"Khoảng cách Euclidean: {euclidean_dist:.4f}")
    print(f"Điểm tương đồng Cosine: {cosine_sim:.4f}")

if __name__ == "__main__":
    vector_a = [1.0, 2.0, 3.0]
    vector_b = [1.5, 2.2, 2.8]
    calculate_metrics(vector_a, vector_b)