import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database.db import get_conn

def recommend_products(product_id, top_k=4):
    conn = get_conn()
    try:
        # --- SỬA LỖI SQL Ở ĐÂY ---
        # 1. Đổi 'product_specs' thành 'products'
        # 2. Đổi 'storage' thành 'ssd'
        # 3. Join với bảng brands để lấy tên hãng (brand_name) thay vì brand_id
        sql = """
        SELECT p.product_id, 
               CONCAT(IFNULL(p.cpu,''), ' ', IFNULL(p.ram,''), ' ', IFNULL(p.ssd,''), ' ', IFNULL(p.gpu,''), ' ', IFNULL(b.brand_name,'')) AS spec 
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.brand_id
        """
        # -------------------------
        
        df = pd.read_sql(sql, conn)
        
        if df.empty: return []

        tfidf = TfidfVectorizer()
        vec = tfidf.fit_transform(df['spec'])
        
        sim = cosine_similarity(vec)
        
        # Tìm index của sản phẩm đang chọn
        if product_id not in df['product_id'].values:
            return []
            
        idx = df.index[df['product_id'] == product_id][0]
        
        # Lấy danh sách độ tương đồng
        scores = list(enumerate(sim[idx]))
        # Sắp xếp giảm dần (giống nhất lên đầu)
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # Lấy top_k (bỏ phần tử đầu tiên vì là chính nó)
        top_indices = [i[0] for i in scores[1:top_k+1]]
        
        return df.iloc[top_indices]['product_id'].tolist()

    except Exception as e:
        print(f"Lỗi AI: {e}")
        return []
    finally:
        try: conn.close()
        except: pass