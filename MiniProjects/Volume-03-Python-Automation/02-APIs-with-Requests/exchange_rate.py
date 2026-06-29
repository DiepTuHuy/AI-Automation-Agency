import requests

def get_usd_to_vnd():
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(url)
        response.raise_for_status() # Báo lỗi nếu HTTP status không phải 200
        
        data = response.json()
        rates = data.get("rates", {})
        vnd_rate = rates.get("VND")
        
        if vnd_rate:
            print(f"1 USD = {vnd_rate:,.2f} VND")
            print(f"Cập nhật lúc: {data.get('time_last_update_utc')}")
        else:
            print("Không tìm thấy thông tin tỷ giá VND.")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi kết nối API: {e}")

if __name__ == "__main__":
    get_usd_to_vnd()