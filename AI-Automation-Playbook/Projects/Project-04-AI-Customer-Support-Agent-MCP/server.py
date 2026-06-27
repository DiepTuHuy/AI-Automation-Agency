import sqlite3
from mcp.server.fastmcp import FastMCP

# Khởi tạo MCP Server
mcp = FastMCP("CRM Order Database Service")

def get_db_connection():
    return sqlite3.connect("orders.db")

@mcp.tool()
def get_order_status(order_id: str) -> str:
    """Kiểm tra trạng thái của một đơn hàng cụ thể dựa trên Mã đơn hàng (Ví dụ: 'OR-111')."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT customer_name, product, status, price FROM orders WHERE order_id = ?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return f"Đơn hàng {order_id} của {row[0]}: Sản phẩm {row[1]} | Trạng thái: {row[2]} | Giá trị: {row[3]:,} VND."
        return f"Không tìm thấy thông tin cho mã đơn hàng {order_id}."
    except Exception as e:
        return f"Lỗi truy vấn database: {str(e)}"

if __name__ == "__main__":
    # Chạy MCP server qua STDIO
    mcp.run()
