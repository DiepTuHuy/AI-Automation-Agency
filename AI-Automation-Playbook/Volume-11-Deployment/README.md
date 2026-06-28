# Volume 11: Deployment - Đưa Dịch Vụ AI Lên Môi Trường Internet (Production)

Một hệ thống AI Automation chạy trên máy tính cục bộ của bạn (`localhost`) sẽ ngừng hoạt động ngay khi bạn tắt máy tính hoặc mất kết nối mạng. Để phục vụ khách hàng doanh nghiệp B2B 24/7, bạn bắt buộc phải biết cách đóng gói và triển khai ứng dụng lên hệ thống máy chủ đám mây (Cloud/VPS). Volume này hướng dẫn bạn các kỹ năng DevOps cốt lõi từ việc đóng gói bằng Docker, cấu hình tường lửa bảo mật Linux VPS, thiết lập Nginx làm Reverse Proxy, cài đặt chứng chỉ bảo mật SSL (HTTPS) miễn phí, và thiết lập đường ống tự động hóa triển khai CI/CD qua GitHub Actions.

---

## 1. Learning Objectives (Mục tiêu học tập)
Sau khi hoàn thành Volume này, bạn sẽ:
- **Đóng gói container thành thạo**: Viết Dockerfile và Docker Compose để đóng gói ứng dụng FastAPI và Database chạy đồng bộ.
- **Quản trị Linux Server**: Thuộc lòng các lệnh Linux cơ bản, cấu hình tường lửa UFW và kết nối an toàn qua SSH Key.
- **Làm chủ Nginx & SSL**: Cấu hình Nginx làm Reverse Proxy và kích hoạt HTTPS bằng Let's Encrypt (Certbot).
- **Tự động hóa CI/CD**: Xây dựng luồng tự động kiểm thử và deploy code lên VPS ngay khi thực hiện `git push` qua GitHub Actions.

---

## 2. Prerequisites (Điều kiện tiên quyết)
- Hoàn thành Volume 04 (FastAPI) và Volume 06 (Database).
- Có tài khoản GitHub và hiểu cách đẩy mã nguồn lên GitHub.

---

## 3. Big Picture (Bức tranh tổng thể)
Môi trường Deployment Production tiêu chuẩn:
Khách hàng truy cập tên miền HTTPS -> Nginx Reverse Proxy tiếp nhận và giải mã SSL -> Điều hướng request vào Docker Container chạy FastAPI cục bộ trên server -> FastAPI kết nối database nội bộ và trả kết quả.

```
[Người dùng: https://api.mycrm.com]
                  │
                  ▼ (Internet)
         [Linux VPS: Cổng 443]
                  │
                  ├─(Nginx: Giải mã SSL) ──> [Điều hướng nội bộ cổng 8000]
                  │
                  ▼
         [Docker Container: FastAPI App]
```

---

## 4. First Principles (Nguyên lý gốc)
- **Môi trường bất biến (Immutable Infrastructure)**: Lỗi *"Chạy được trên máy tôi nhưng lỗi trên server"* là do sự sai lệch môi trường (phiên bản Python, thư viện hệ điều hành). Docker giải quyết triệt để bằng cách đóng gói mọi thứ cần thiết vào một Container chạy độc lập đồng nhất ở mọi nơi.
- **Phòng vệ chiều sâu (Defense in Depth)**: Không bao giờ mở trực tiếp cổng ứng dụng (như 8000 của FastAPI hay 5432 của PostgreSQL) ra Internet. Hãy khóa tất cả các cổng bằng tường lửa UFW, chỉ mở cổng 80/443 (HTTP/HTTPS) cho Nginx và cổng 22 (SSH) để quản trị.
- **Tự động hóa triển khai (Automation Over Manual)**: Tuyệt đối không deploy bằng cách SSH vào server rồi gõ lệnh pull code thủ công. Con người rất dễ gõ sai câu lệnh. Hãy để đường ống CI/CD thực hiện tự động nhằm đảm bảo tính nhất quán tuyệt đối.

---

## 5. Mental Models (Mô hình tư duy)
- **Tàu container vận chuyển hàng hóa (Dockerized Shipping)**: Trong ngành vận tải biển cũ, hàng hóa chất đống hỗn loạn trên tàu, dễ bị rơi vỡ hoặc thất thoát. Khi chuẩn "Container" ra đời, mọi hàng hóa (dầu ăn, quần áo, thiết bị) đều được xếp vào các thùng container tiêu chuẩn có kích thước giống hệt nhau. Tàu chở hàng chỉ việc xếp các thùng container này lên boong. Docker hoạt động y hệt. FastAPI của bạn, Postgres DB, n8n... đều được đóng vào các "Container" Docker tiêu chuẩn. Máy chủ VPS chỉ việc chạy các container này mà không cần quan tâm bên trong chứa hệ điều hành hay mã nguồn gì.

---

## 6. Core Concepts (Khái niệm cốt lõi)
1. **Dockerfile**: Tệp tin cấu hình chứa danh sách các bước chỉ dẫn để Docker build ra một Image (ảnh tĩnh của ứng dụng).
2. **Docker Compose**: Công cụ dùng để định nghĩa và chạy hệ thống nhiều container đồng thời thông qua một file cấu hình YAML duy nhất.
3. **Nginx Reverse Proxy**: Máy chủ web trung gian tiếp nhận yêu cầu từ client, xử lý giải mã HTTPS và chuyển tiếp yêu cầu đến các ứng dụng backend nội bộ.

---

## 8. Best Practices (Quy chuẩn thực chiến)
- **Sử dụng Multi-stage Build trong Dockerfile**: Tách biệt giai đoạn cài đặt thư viện phụ thuộc (build stage) và giai đoạn chạy ứng dụng thực tế (run stage) để giảm dung lượng file Docker Image từ 1GB xuống còn dưới 150MB, giúp tăng tốc độ tải và giảm nguy cơ bảo mật.
- **Tuyệt đối không lưu mật khẩu trong Dockerfile**: Luôn sử dụng biến môi trường (Environment Variables) truyền vào container lúc khởi chạy qua file `.env`.
- **Sử dụng SSH Key thay thế Mật khẩu**: Tắt tính năng đăng nhập VPS bằng mật khẩu trong file cấu hình SSH Daemon (`PasswordAuthentication no`) để ngăn chặn 100% các cuộc tấn công Brute-force dò quét mật khẩu từ hacker.

---

## 9. Common Mistakes (Sai lầm thường gặp)
- **Quên ghi file Docker Volume cho Database**: Khởi chạy DB Postgres trong Docker nhưng quên cấu hình volume đĩa cứng. Khi container bị sập hoặc cập nhật phiên bản mới, toàn bộ dữ liệu của database sẽ bị xóa sạch. *Cách sửa*: Luôn khai báo `volumes` liên kết thư mục dữ liệu của DB ra ổ đĩa của VPS máy chủ.
- **Mở cổng 80 mà quên cấu hình HTTPS**: Gửi các API Key bảo mật hoặc thông tin tài khoản qua HTTP dưới dạng text thô không mã hóa, khiến hacker dễ dàng nghe trộm (Sniffing) dữ liệu trên đường truyền. *Cách sửa*: Luôn sử dụng Let's Encrypt để lấy chứng chỉ SSL và tự động redirect mọi traffic HTTP sang HTTPS.

---

## 10. Engineering Mindset (Tư duy kỹ sư)
Một kỹ sư DevOps thực chiến thiết kế hệ thống với tư duy *"Mọi thứ đều có thể sụp đổ đột ngột"*. Họ xây dựng các đoạn script sao lưu database tự động hàng ngày, cấu hình cho các container Docker tự khởi động lại khi crash (`restart: always`), và thiết lập hệ thống giám sát sức khỏe server (Uptime monitoring) để nhận thông báo tức thì qua Telegram khi máy chủ bị nghẽn mạng.

---

## 13. Capstone Project (Dự án kết khóa Volume)
Triển khai toàn diện Hệ thống CRM AI lên Cloud VPS: Mua một VPS Ubuntu rẻ (như Hetzner, DigitalOcean), cài đặt Docker, cấu hình tường lửa UFW bảo mật. Viết file `docker-compose.yml` khởi chạy ứng dụng FastAPI Lead Qualification (ở Vol 06) cùng cơ sở dữ liệu PostgreSQL. Thiết lập tên miền riêng trỏ về IP của VPS, cấu hình Nginx Reverse Proxy và lấy chứng chỉ SSL HTTPS miễn phí bằng Certbot. Thiết lập GitHub Actions tự động build và deploy code mới lên VPS khi commit.

---

## 14. Review Questions (Bloom Taxonomy - 30 câu hỏi)
### Level 1 — Remember (Nhớ)
1. Docker Container khác Virtual Machine (Máy ảo) ở điểm cốt lõi nào?
2. SSH là gì và cổng mặc định của nó là cổng mấy?
3. Nginx đóng vai trò gì trong hệ thống mạng?
4. Chứng chỉ SSL là viết tắt của từ gì và tác dụng của nó là gì?
5. CI/CD là viết tắt của các từ gì?

### Level 2 — Understand (Hiểu)
6. Giải thích sự khác biệt giữa Docker Image và Docker Container.
7. Tại sao chúng ta cần sử dụng Docker Compose thay vì tự chạy từng lệnh `docker run` thủ công?
8. Tại sao việc tắt đăng nhập VPS bằng mật khẩu và chuyển sang SSH Key lại nâng cao bảo mật hệ thống lên hàng chục lần?
9. Cơ chế Let's Encrypt và Certbot tự động xác thực tên miền để cấp chứng chỉ SSL hoạt động như thế nào?
10. Giải thích luồng chạy tự động của một GitHub Actions workflow từ khi lập trình viên đẩy code lên đến khi deploy thành công trên server.

### Level 3 — Apply (Áp dụng)
11. Viết một file Dockerfile tiêu chuẩn cho ứng dụng FastAPI sử dụng python 3.10-slim image.
12. Viết câu lệnh Docker Compose chạy đồng thời hai dịch vụ: web app FastAPI và database PostgreSQL.
13. Thực hiện kết nối tới một Linux VPS từ máy tính cá nhân sử dụng tệp SSH Key bí mật qua Terminal.
14. Sử dụng tường lửa UFW trên Ubuntu để chỉ mở các cổng 22, 80, 443 và chặn tất cả các cổng còn lại.
15. Viết file cấu hình Nginx cơ bản điều hướng tên miền `api.example.com` về cổng local 8000 của server.

### Level 4 — Analyze (Phân tích)
16. Phân tích nguyên nhân tại sao kích thước Docker Image quá lớn lại ảnh hưởng tiêu cực tới quá trình triển khai CI/CD.
17. So sánh ưu thế và nhược điểm của việc triển khai database PostgreSQL nằm trong container Docker so với việc thuê dịch vụ Database Managed của nhà cung cấp (như AWS RDS).
18. Đánh giá tính an toàn của việc lưu trữ SSH Private Key trong phần Secrets của GitHub để phục vụ CI/CD deploy tự động.
19. Phân tích sự ảnh hưởng của tham số `restart: unless-stopped` trong cấu hình Docker Compose đối với độ ổn định của hệ thống sau khi VPS bị reboot.
20. Tại sao Nginx Reverse Proxy lại giúp che giấu cấu trúc mạng nội bộ và thông tin của máy chủ ứng dụng thực tế phía sau?

### Level 5 — Design (Thiết kế)
21. Thiết kế file Dockerfile tối ưu áp dụng kỹ thuật Multi-stage Build cho một ứng dụng Python cài đặt các thư viện nặng (như numpy, pandas).
22. Đề xuất sơ đồ phân luồng mạng và quy trình bảo mật cho một hệ thống gồm: Frontend React, API FastAPI, cơ sở dữ liệu PostgreSQL và n8n cùng chạy trên 1 VPS.
23. Thiết kế script tự động backup định kỳ cơ sở dữ liệu PostgreSQL ra file `.sql` nén và đẩy lên dịch vụ lưu trữ S3 an toàn.
24. Đề xuất quy trình chuyển dịch hệ thống không downtime (Zero-downtime Deployment) sử dụng kỹ thuật Blue-Green hoặc Rolling Update trong Docker.
25. Thiết kế workflow GitHub Actions hoàn chỉnh tự động chạy testcases, nếu test pass thì tiến hành build Docker Image, đẩy lên Docker Hub và thông báo lên Telegram.

### Level 6 — Evaluate (Đánh giá)
26. Đánh giá sự đánh đổi giữa việc tự host toàn bộ hệ thống trên một VPS đơn lẻ và sử dụng kiến trúc Serverless (như AWS Lambda, Supabase) cho dự án AI Automation khởi nghiệp.
27. Đánh giá độ an toàn bảo mật của cổng HTTPS Let's Encrypt trước các cuộc tấn công Man-in-the-middle (Nghe trộm đường truyền).
28. Kiểm chứng độ ổn định của đường ống CI/CD khi đồng thời có nhiều lập trình viên cùng đẩy code lên nhánh main trong một dự án.
29. Đánh giá hiệu năng xử lý của Nginx Reverse Proxy khi đối mặt với các cuộc tấn công từ chối dịch vụ quy mô nhỏ (DDoS).
30. Lập luận bác bỏ hoặc đồng ý với quan điểm: *"Trong kỷ nguyên đám mây hiện nay, kỹ sư AI không cần biết về Linux hay Docker, các dịch vụ Cloud PaaS (như Render, Vercel) sẽ tự động làm hết mọi việc"*.

---

## 15. Checklist hoàn thành
- [ ] Viết được Dockerfile đóng gói thành công ứng dụng python chạy local.
- [ ] Sử dụng được Docker Compose quản lý FastAPI và Postgres DB.
- [ ] Cấu hình thành công tường lửa UFW và truy cập VPS qua SSH Key.
- [ ] Cấu hình Nginx Reverse Proxy điều hướng tên miền trỏ về đúng cổng ứng dụng.
- [ ] Kích hoạt HTTPS SSL Let's Encrypt thành công trên tên miền thực tế.
- [ ] Trả lời đúng tối thiểu 80% câu hỏi ôn tập.

---

## 16. Resources (Tài liệu tham khảo)
- **Docker**: [Docker Get Started Guide](https://docs.docker.com/get-started/)
- **Linux**: [Ubuntu Server Guide](https://ubuntu.com/server/docs)
- **Nginx**: [Nginx Beginner's Guide](https://nginx.org/en/docs/beginners_guide.html)