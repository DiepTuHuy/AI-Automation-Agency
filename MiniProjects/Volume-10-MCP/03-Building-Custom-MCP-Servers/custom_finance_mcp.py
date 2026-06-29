from mcp.server.fastmcp import FastMCP

# Khởi tạo FastMCP Server
mcp = FastMCP("FinanceAssistant")

# Định nghĩa Tool tính thuế
@mcp.tool()
def calculate_income_tax(income_usd: float) -> str:
    """Tính toán thuế thu nhập cá nhân ước tính (10% cho thu nhập dưới 50k, 20% cho trên 50k)."""
    if income_usd < 50000:
        tax = income_usd * 0.1
    else:
        tax = (50000 * 0.1) + ((income_usd - 50000) * 0.2)
    return f"Thuế thu nhập cá nhân ước tính cho mức ${income_usd:,.2f} là: ${tax:,.2f}"

if __name__ == "__main__":
    mcp.run()