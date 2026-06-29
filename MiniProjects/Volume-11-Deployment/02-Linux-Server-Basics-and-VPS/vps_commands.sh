# 1. Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# 2. Cài đặt Python và Pip
sudo apt install python3 python3-pip -y

# 3. Kiểm tra dung lượng ổ đĩa
df -h

# 4. Xem các cổng mạng đang mở lắng nghe
sudo ss -tunlp