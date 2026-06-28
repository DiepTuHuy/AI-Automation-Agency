# Volume 13: Portfolio - Xây Dựng Thương Hiệu Kỹ Sư Thực Chiến

Khách hàng doanh nghiệp B2B và nhà tuyển dụng không mua lý thuyết hay những lời hứa hẹn. Họ mua những sản phẩm chạy được thực tế và bằng chứng về năng lực giải quyết bài toán nghiệp vụ của bạn. **Portfolio (Hồ sơ năng lực)** chính là vũ khí bán hàng mạnh nhất của một AI Automation Engineer. Volume này hướng dẫn bạn cách thiết kế một trang cá nhân GitHub Profile thu hút, viết các file `README.md` dự án chuẩn B2B thuyết phục, vẽ sơ đồ kiến trúc hệ thống chuyên nghiệp và quay video demo sản phẩm trực quan dài 2 phút để "wow" khách hàng ngay từ cái nhìn đầu tiên.

---

## 1. Learning Objectives (Mục tiêu học tập)
Sau khi hoàn thành Volume này, bạn sẽ:
- **Thiết lập GitHub chuẩn CV**: Thiết kế trang hồ sơ cá nhân GitHub Profile giới thiệu bản thân ấn tượng.
- **Viết README thuyết phục**: Soạn thảo các file README dự án chi tiết, làm nổi bật giá trị ROI mang lại cho doanh nghiệp hơn là chỉ nói về công nghệ.
- **Vẽ sơ đồ kiến trúc chuyên nghiệp**: Sử dụng Mermaid.js và Excalidraw vẽ các sơ đồ hệ thống chuẩn hóa.
- **Sản xuất Video Demo triệu view**: Quay và cắt dựng video demo sản phẩm dài 2 phút tập trung vào giải quyết bài toán thực tế của khách hàng.
- **Chuẩn bị Portfolio B2B**: Hoàn thiện 4 dự án mẫu (Projects 01-04) trong Portfolio ở trạng thái sẵn sàng trình diễn cho khách hàng.

---

## 2. Prerequisites (Điều kiện tiên quyết)
- Hoàn thành các Volume từ 01 đến 12.
- Có tài khoản GitHub và công cụ quay màn hình (như Loom hoặc OBS Studio).

---

## 3. Big Picture (Bức tranh tổng thể)
Hành trình chuyển đổi từ Khách hàng tiềm năng sang Hợp đồng thực tế bằng Portfolio:
Khách xem Video Demo ngắn -> Bị ấn tượng bởi giá trị B2B -> Click vào GitHub xem Sơ đồ kiến trúc -> Xem tài liệu hướng dẫn nhanh -> Đặt lịch họp kí kết hợp đồng.

```
[Video Demo 2 phút (Loom / YouTube)] ──(Tò mò giá trị)──> [GitHub Project README]
                                                                │
                                            (Xem cấu trúc & Sơ đồ kiến trúc) │
                                                                ▼
                                                    [Ký Hợp Đồng Dự Án]
```

---

## 4. First Principles (Nguyên lý gốc)
- **Doanh thu trước, Công nghệ sau (Value Over Code)**: Khách hàng B2B không quan tâm bạn dùng FastAPI hay LangGraph. Họ quan tâm hệ thống của bạn giúp họ tiết kiệm bao nhiêu giờ làm việc và tăng bao nhiêu phần trăm doanh thu. Hãy viết Portfolio bằng ngôn ngữ của doanh nghiệp.
- **Visuals Speak Louder Than Code (Trực quan hóa)**: Một sơ đồ khối đẹp đẽ và một video chạy thực tế luôn thuyết phục hơn 10,000 dòng code Python phức tạp mà khách hàng không hiểu.
- **Mở và Chạy ngay (Reproducibility)**: Một dự án tốt trên GitHub phải chạy được ngay lập tức trên máy của người khác nếu họ làm theo hướng dẫn cài đặt trong README.

---

## 5. Mental Models (Mô hình tư duy)
- **Cửa kính trưng bày sản phẩm (The Storefront Window)**: Hãy coi trang GitHub của bạn giống như tủ kính trưng bày của một cửa hàng thời trang cao cấp trên phố lớn.
  - *Cửa hàng tồi*: Bày bừa các đoạn code nháp, file rác, không có biển hiệu, không có hướng dẫn sử dụng (không có README). Người qua đường sẽ lập tức bỏ đi.
  - *Cửa hàng tốt*: Bày biện 3-4 bộ trang phục đẹp nhất (3-4 dự án chất lượng được ghim), có đèn chiếu sáng rực rỡ (hình ảnh screenshot, sơ đồ kiến trúc), và bảng mô tả chất liệu rõ ràng (README hướng dẫn đầy đủ). Khách hàng sẽ tin tưởng và bước vào mua sắm.

---

## 6. Core Concepts (Khái niệm cốt lõi)
1. **GitHub Profile README**: File markdown đặc biệt hiển thị ngay đầu trang cá nhân GitHub để giới thiệu bản thân và định hướng công việc.
2. **Mermaid.js**: Công cụ viết code để sinh ra sơ đồ khối, sequence diagram trực tiếp trong file markdown của GitHub mà không cần chèn file ảnh nặng.
3. **The 2-Minute Demo Rule**: Quy tắc quay video demo sản phẩm: 30 giây đầu tiên hiển thị kết quả cuối cùng (WOW factor), 60 giây tiếp theo giải thích cách hoạt động nghiệp vụ, 30 giây cuối cùng lướt qua kiến trúc kỹ thuật.

---

## 8. Best Practices (Quy chuẩn thực chiến)
- **Sử dụng Badges**: Thêm các nhãn thông tin (badges) như phiên bản Python, trạng thái deploy, công cụ sử dụng ở đầu file README để tăng tính chuyên nghiệp.
- **Cung cấp File `.env.example`**: Luôn giấu các key API thực tế nhưng phải cung cấp file ví dụ `.env.example` để người dùng biết cần điền các tham số cấu hình nào.
- **Viết Commit Message chuẩn**: Sử dụng Conventional Commits (ví dụ: `feat: add fallback model`, `fix: repair token counter`) để thể hiện tác phong lập trình chuyên nghiệp.

---

## 9. Common Mistakes (Sai lầm thường gặp)
- **Đẩy các file rác lên GitHub**: Commit cả thư mục ảo `.venv/`, các file lưu cấu hình nhạy cảm `.env`, hoặc file lưu cache của hệ điều hành `.DS_Store`. *Cách sửa*: Luôn khai báo đầy đủ file `.gitignore` để lọc bỏ file rác trước khi commit.
- **README dài dòng học thuật**: Giải thích lịch sử ra đời của Transformer thay vì tập trung vào hướng dẫn sử dụng sản phẩm. *Cách sửa*: Viết README tập trung vào: Tính năng, Kiến trúc, Cài đặt và Hướng dẫn chạy nhanh.

---

## 10. Engineering Mindset (Tư duy kỹ sư)
Một kỹ sư phần mềm chuyên nghiệp coi "Tài liệu kỹ thuật" (Documentation) là một phần cốt lõi của mã nguồn sản phẩm. Họ không bao giờ coi dự án là hoàn thành nếu chưa viết xong file README rõ ràng và vẽ xong sơ đồ kiến trúc.

---

## 13. Capstone Project (Dự án kết khóa Volume)
Hoàn thiện hồ sơ năng lực cá nhân: Thiết lập trang cá nhân GitHub Profile. Cập nhật và xuất bản 4 dự án Capstone (từ Vol 01 đến Vol 12) lên 4 repositories độc lập. Viết file README hoàn chỉnh cho từng dự án, vẽ sơ đồ kiến trúc bằng Mermaid, chụp ảnh màn hình giao diện thực tế và quay 1 video demo dài 2 phút bằng Loom đính kèm vào mỗi README.

---

## 14. Review Questions (Bloom Taxonomy - 30 câu hỏi)
### Level 1 — Remember (Nhớ)
1. File `.gitignore` dùng để làm gì?
2. Markdown hỗ trợ chèn hình ảnh theo cú pháp nào?
3. Mermaid.js là gì?
4. Loom là công cụ gì?
5. Nêu 5 phần bắt buộc phải có trong một file README tiêu chuẩn.

### Level 2 — Understand (Hiểu)
6. Tại sao việc Maintain một đồ thị đóng góp màu xanh (Contribution Graph) trên GitHub lại có lợi thế lớn khi tìm kiếm cơ hội dự án?
7. Giải thích sự khác biệt về đối tượng độc giả khi viết README dự án B2B (Dành cho khách hàng doanh nghiệp) và B2C (Dành cho người dùng cuối).
8. Tại sao việc đưa mã nguồn chứa thông tin API Key lên GitHub Public Repository lại là một lỗi nghiêm trọng và cách phòng ngừa?
9. Quy tắc "The 2-Minute Demo Rule" giúp giữ chân người xem video như thế nào?
10. Tại sao việc vẽ sơ đồ kiến trúc hệ thống lại giúp khách hàng B2B dễ dàng phê duyệt ngân sách hơn?

### Level 3 — Apply (Áp dụng)
11. Viết một file `.gitignore` tiêu chuẩn lọc bỏ `.venv/`, `.env`, `__pycache__/` và các tệp tin cơ sở dữ liệu SQLite `.db`.
12. Viết đoạn code Mermaid.js biểu diễn một sequence diagram gồm 3 bên: Người dùng -> FastAPI -> Database.
13. Thiết kế cấu trúc bảng giới thiệu các tính năng của dự án trong file Markdown README.
14. Áp dụng phong cách Conventional Commits viết 3 thông điệp commit cho các tác vụ: sửa lỗi chính tả, thêm tính năng mới, và viết tài liệu.
15. Thiết lập liên kết ảnh chụp màn hình cục bộ hiển thị trực tiếp trong file README.

### Level 4 — Analyze (Phân tích)
16. Phân tích sự ảnh hưởng của một file README trình bày cẩu thả, không có tiêu đề phân cấp đối với quyết định tuyển dụng của nhà tuyển dụng.
17. So sánh hiệu năng truyền tải thông tin của một video demo quay màn hình không có giọng nói thuyết minh và một video có thuyết minh rõ ràng.
18. Đánh giá mức độ an toàn bảo mật khi public mã nguồn chứa thông tin cấu hình cổng mặc định của database VPS.
   - *Cách sửa*: Luôn ẩn thông tin IP và Cổng trong file `.env`.
19. Phân tích nguyên nhân tại sao một dự án mã nguồn mở có 1000 sao (stars) trên GitHub thường có tài liệu hướng dẫn cài đặt cực kỳ chi tiết.
20. Tại sao việc chèn các badges chỉ số (như Test Coverage, Build Status) lại tăng mức độ tin cậy của dự án phần mềm?

### Level 5 — Design (Thiết kế)
21. Thiết kế trang hồ sơ GitHub Profile cá nhân giới thiệu đầy đủ kỹ năng: Python, FastAPI, Docker, n8n, LangGraph và các dự án tiêu biểu.
22. Đề xuất kịch bản (Script) chi tiết từng giây cho video demo dài 2 phút giới thiệu dự án AI Chat PDF.
23. Thiết kế sơ đồ kiến trúc toàn thể hệ thống AI CRM Automation bao gồm cả luồng thông báo lỗi trung tâm sử dụng Mermaid.js.
24. Đề xuất quy trình quản lý phiên bản phát hành (Releases) chuyên nghiệp trên GitHub cho một dự án AAA bàn giao cho khách hàng.
25. Thiết kế cấu trúc file README cho một dự án ngách AI phục vụ riêng cho ngành y tế đòi hỏi các tiêu chuẩn bảo mật dữ liệu HIPAA nghiêm ngặt.

### Level 6 — Evaluate (Đánh giá)
26. Đánh giá tính hiệu quả thương mại của việc xây dựng một trang web Portfolio cá nhân độc lập so với việc sử dụng trực tiếp GitHub Profile.
27. Đánh giá sự đánh đổi giữa việc mở mã nguồn dự án (Open-source) trên GitHub để làm portfolio và việc giữ kín mã nguồn để bảo vệ bản quyền ý tưởng.
28. Kiểm chứng độ chính xác của tài liệu hướng dẫn cài đặt trong README bằng cách chạy thử trên một máy tính hoàn toàn mới (Clean machine).
29. Đánh giá mức độ ảnh hưởng của việc duy trì lịch sử Git commit sạch sẽ đối với khả năng làm việc nhóm (Teamwork) trong các dự án lớn.
30. Lập luận bác bỏ hoặc đồng ý với nhận định: *"Kỹ sư AI giỏi chỉ cần code chạy tốt, không cần tốn thời gian học cách vẽ sơ đồ hay quay video giới thiệu làm màu"*.

---

## 15. Checklist hoàn thành
- [ ] Thiết lập file .gitignore chuẩn cho mọi dự án Python.
- [ ] Thiết kế trang cá nhân GitHub Profile README chuyên nghiệp.
- [ ] Viết được file README dự án chi tiết có chèn sơ đồ kiến trúc Mermaid.js.
- [ ] Quay thành công ít nhất 1 video demo sản phẩm bằng Loom dài 2 phút có thuyết minh giọng nói.
- [ ] Trả lời đúng tối thiểu 80% câu hỏi ôn tập.

---

## 16. Resources (Tài liệu tham khảo)
- **Tài liệu**: [GitHub Profile Readme Guide](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme)
- **Sơ đồ**: [Mermaid.js Official Live Editor](https://mermaid.live/)
- **Đọc thêm**: *Pro Git Book by Scott Chacon.*