import asyncio
import httpx

urls = [
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500"
]

async def check_url(client: httpx.AsyncClient, url: str):
    try:
        response = await client.get(url)
        print(f"URL: {url} -> Status: {response.status_code}")
    except Exception as e:
        print(f"URL: {url} -> Lỗi kết nối: {e}")

async def main():
    async with httpx.AsyncClient() as client:
        # Tạo danh sách các task chạy song song
        tasks = [check_url(client, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())