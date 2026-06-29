import json

json_data = '''
[
    {"transaction_id": "T01", "product": "Bàn phím cơ", "price": 80.0, "quantity": 3},
    {"transaction_id": "T02", "product": "Chuột không dây", "price": 45.0, "quantity": 5},
    {"transaction_id": "T03", "product": "Bàn phím cơ", "price": 80.0, "quantity": 1},
    {"transaction_id": "T04", "product": "Tai nghe", "price": 120.0, "quantity": 2}
]
'''

def generate_report(data_str: str):
    transactions = json.loads(data_str)
    total_revenue = 0
    product_sales = {}
    
    for t in transactions:
        revenue = t["price"] * t["quantity"]
        total_revenue += revenue
        
        prod = t["product"]
        product_sales[prod] = product_sales.get(prod, 0) + t["quantity"]
        
    print(f"Tổng doanh thu: ${total_revenue:.2f}")
    print("Số lượng bán ra của từng sản phẩm:")
    for prod, qty in product_sales.items():
        print(f"- {prod}: {qty} chiếc")

if __name__ == "__main__":
    generate_report(json_data)