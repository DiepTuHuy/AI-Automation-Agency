# Volume 15: Client Projects - Quy Trình Triển Khai & Bàn Giao Dự Án Thực Tế

Ký được hợp đồng với khách hàng mới chỉ là sự khởi đầu. Sự khác biệt giữa một freelancer nghiệp dư và một Agency chuyên nghiệp nằm ở **Quy trình triển khai dự án (Delivery Process)**. Volume này hướng dẫn bạn cách tổ chức buổi họp khảo sát nghiệp vụ (Discovery & Scoping Session) để vẽ lại bản đồ quy trình thô của khách hàng, cách chia nhỏ dự án thành các mốc bàn giao tuần tự (Milestones) theo mô hình Agile, cách quản lý kỳ vọng của khách hàng để tránh bị phình tính năng, và quy trình bàn giao (Handover) bàn giao hệ thống, viết tài liệu và đào tạo nhân sự khách hàng sử dụng để nghiệm thu dự án thành công nhận nốt phần tiền còn lại.

---

## 1. Learning Objectives (Mục tiêu học tập)
Sau khi hoàn thành Volume này, bạn sẽ:
- **Tổ chức họp khảo sát chuyên nghiệp**: Điều phối buổi họp Scoping để khai thác chính xác nỗi đau nghiệp vụ và vẽ sơ đồ quy trình thô (As-Is).
- **Thiết lập mốc bàn giao**: Lập kế hoạch dự án 4 tuần chuẩn Agile với các mốc Milestone rõ ràng và bàn giao bản chạy thử (MVP) sớm.
- **Quản lý kỳ vọng**: Thiết lập quy trình phản hồi và duyệt thay đổi (Change Request) để bảo vệ dự án khỏi trễ hạn.
- **Viết tài liệu bàn giao**: Soạn thảo tài liệu bàn giao kỹ thuật (Handover Document) và làm video đào tạo nhân sự khách hàng.
- **Nghiệm thu dự án**: Ký biên bản bàn giao bàn giao và nghiệm thu dự án chính thức để giải ngân đợt cuối.

---

## 2. Prerequisites (Điều kiện tiên quyết)
- Hoàn thành các Volume từ 01 đến 14.
- Hiểu rõ quy trình kinh doanh và giao tiếp B2B.

---

## 3. Big Picture (Bức tranh tổng thể)
Quy trình triển khai dự án B2B tiêu chuẩn:
Khảo sát nghiệp vụ -> Vẽ quy trình To-Be -> Triển khai MVP (Tuần 1-2) -> Kiểm thử & Tối ưu (Tuần 3) -> Đào tạo & Bàn giao (Tuần 4) -> Nghiệm thu & Nhận tiền.

```
[Họp Khảo Sát (Scoping)] ──> [Bàn giao MVP Tuần 1-2] ──> [Kiểm thử & Đào tạo Tuần 3-4]
                                                                  │
                                                                  ▼
                                                      [Nghiệm Thu & Giải Ngân]
```

---

## 4. First Principles (Nguyên lý gốc)
- ** MVP sớm thắng tính năng hoàn hảo**: Đừng bao giờ biến mất trong 4 tuần rồi đột ngột quay lại giao một hệ thống khổng lồ. Hãy bàn giao một bản chạy thử tối giản (MVP) hoạt động được ngay trong tuần đầu tiên để lấy feedback sớm và xây dựng lòng tin cho khách hàng.
- **Tài liệu là bằng chứng nghiệm thu**: Khách hàng không thể nghiệm thu nếu không biết cách dùng. Việc cung cấp tài liệu bàn giao rõ ràng giúp giảm thiểu 80% số lượng câu hỏi hỗ trợ kỹ thuật sau khi bàn giao.
- **Giai đoạn Hypercare (Chăm sóc đặc biệt)**: Trong 2 tuần đầu tiên sau khi hệ thống go-live, nhân viên khách hàng sẽ thao tác sai hoặc phát sinh lỗi tiềm ẩn. Việc hỗ trợ online trực tiếp tức thời trong thời gian này là chìa khóa để chốt hợp đồng Retainer sau này.

---

## 5. Mental Models (Mô hình tư duy)
- **Kiến trúc sư xây nhà**: Một kiến trúc sư giỏi không bao giờ đổ móng bê tông ngay sau khi khách hàng nói: *"Tôi muốn xây nhà 3 tầng"*.
  - Họ sẽ ngồi vẽ bản vẽ thiết kế 2D, 3D (Scoping & SOW).
  - Thống nhất màu sơn, vật liệu (Milestones).
  - Cho khách hàng duyệt bản vẽ trước khi xây (MVP Approval).
  - Khi hoàn thành, bàn giao sơ đồ đường điện, đường nước và chìa khóa nhà (Handover Document).
  Làm dự án AI Automation y hệt như xây nhà. Hãy làm theo đúng quy trình kiến trúc sư.

---

## 6. Core Concepts (Khái niệm cốt lõi)
1. **Discovery Session**: Buổi họp phỏng vấn khách hàng để thu thập thông tin về cấu trúc phòng ban, quy trình làm việc thủ công hiện tại và các hệ thống phần mềm đang sử dụng.
2. **MVP (Minimum Viable Product)**: Phiên bản sản phẩm tối thiểu chạy được, chỉ chứa tính năng cốt lõi nhất để giải quyết nỗi đau lớn nhất của khách hàng.
3. **Hypercare Period**: Khoảng thời gian hỗ trợ kỹ thuật tăng cường (thường từ 2 tuần đến 1 tháng) ngay sau khi dự án go-live để đảm bảo hệ thống vận hành ổn định trên môi trường thực tế.

---

## 8. Best Practices (Quy chuẩn thực chiến)
- **Tạo kênh Slack/Zalo chung**: Thiết lập kênh chat chung giữa đội ngũ của bạn và khách hàng để trao đổi thông tin nhanh chóng hàng ngày.
- **Họp Demo hàng tuần (Weekly Demo)**: Tổ chức buổi họp 15 phút vào cuối tuần để trình diễn những gì đã làm được và thống nhất kế hoạch tuần tiếp theo.
- **Lưu trữ Credentials an toàn**: Khi khách hàng cung cấp tài khoản email, API Key của họ, luôn sử dụng các công cụ quản lý mật khẩu bảo mật (như 1Password hoặc Bitwarden) và xóa sạch thông tin khỏi máy sau khi bàn giao.

---

## 9. Common Mistakes (Sai lầm thường gặp)
- **Làm hộ các phần việc ngoài hợp đồng vì nể khách**: Khiến dự án bị phình to (scope creep), kéo dài thời gian làm việc của bạn và dẫn đến trễ hạn các mốc milestone chính. *Cách sửa*: Luôn yêu cầu ký Phụ lục thay đổi (Change Request) kèm chi phí bổ sung cho các tính năng phát sinh.
- **Bàn giao không kèm video hướng dẫn**: Gửi cho khách hàng một file PDF hướng dẫn dài 50 trang. Nhân viên của họ sẽ lười đọc và liên tục gọi điện hỏi bạn. *Cách sửa*: Quay 3 video Loom ngắn (mỗi video 3 phút) hướng dẫn trực quan từng tính năng chính.

---

## 10. Engineering Mindset (Tư duy kỹ sư)
Một kỹ sư thực chiến coi sự hài lòng của khách hàng (Client Satisfaction) là chỉ số quan trọng ngang với chất lượng code. Họ hiểu rằng một hệ thống AI dù thông minh đến đâu cũng sẽ bị coi là thất bại nếu nhân sự của khách hàng cảm thấy nó quá khó sử dụng và quay lại làm thủ công.

---

## 13. Capstone Project (Dự án kết khóa Volume)
Xem mô tả chi tiết tại [Project-05](file:///Users/dieptuhuy/Documents/AI%20Automation/AI-Automation-Playbook/Projects/Project-05-AI-Resume-Analyzer-Invoice-Reader/README.md).

---

## 14. Review Questions (Bloom Taxonomy - 30 câu hỏi)
### Level 1 — Remember (Nhớ)
1. Discovery Session là gì?
2. MVP trong phát triển phần mềm là gì?
3. Giai đoạn Hypercare thường kéo dài bao lâu?
4. Kể tên 3 công cụ quản lý dự án thường dùng.
5. Biên bản nghiệm thu bàn giao dự án dùng để làm gì?

### Level 2 — Understand (Hiểu)
6. Tại sao việc vẽ quy trình As-Is (Hiện tại) lại bắt buộc phải thực hiện trước khi thiết kế quy trình To-Be (Tương lai)?
7. Giải thích sự khác biệt giữa môi trường Staging (Thử nghiệm) và Production (Vận hành thực tế). Tại sao không nên test code trực tiếp trên Production?
8. Tại sao việc bàn giao một MVP chạy được vào tuần đầu tiên lại giúp củng cố lòng tin của khách hàng tốt hơn mọi lời hứa?
9. Quy trình tiếp nhận và duyệt một Yêu cầu thay đổi (Change Request) diễn ra như thế nào?
10. Tại sao việc quay video Loom hướng dẫn sử dụng lại hiệu quả hơn viết tài liệu văn bản dài dòng đối với nhân viên văn phòng?

### Level 3 — Apply (Áp dụng)
11. Soạn thảo danh sách 5 câu hỏi phỏng vấn khách hàng trong buổi Discovery Session để tìm hiểu về quy trình duyệt chi phí nội bộ của họ.
12. Vẽ sơ đồ Gantt dạng bảng mô tả kế hoạch triển khai dự án AI Chat PDF trong vòng 4 tuần.
13. Viết email thông báo cho khách hàng về việc phát hiện một yêu cầu phát sinh nằm ngoài SOW ban đầu và đề xuất chi phí bổ sung.
14. Soạn thảo cấu mục lục (Table of Contents) cho một cuốn Tài liệu bàn giao kỹ thuật (Handover Document).
15. Thiết lập một biểu mẫu Biên bản bàn giao bàn giao và nghiệm thu dự án (Acceptance Certificate) cơ bản.

### Level 4 — Analyze (Phân tích)
16. Phân tích nguyên nhân tại sao các dự án B2B thường gặp khó khăn ở khâu nghiệm thu cuối cùng và cách phòng tránh ngay từ khâu viết SOW.
17. So sánh hiệu quả của việc đào tạo nhân viên khách hàng bằng lớp học trực tiếp (Workshop) và bằng bộ video hướng dẫn tự xem.
18. Đánh giá rủi ro khi khách hàng chậm trễ trong việc cung cấp thông tin tài khoản API (Credentials) đối với tiến độ chung của dự án.
19. Phân tích tác động của việc thay đổi nhân sự phụ trách dự án phía khách hàng đối với việc nghiệm thu sản phẩm.
20. Tại sao việc thiết lập hệ thống giám sát lỗi (như LangFuse) trong giai đoạn Hypercare lại giúp kỹ sư phát hiện và sửa lỗi trước khi khách hàng biết?

### Level 5 — Design (Thiết kế)
21. Thiết kế quy trình bàn giao (Handover Pipeline) hoàn chỉnh gồm: nạp dữ liệu tri thức của khách -> kiểm thử cuối -> đào tạo -> ký biên bản -> go-live.
22. Đề xuất kịch bản kịch bản cho buổi họp Kick-off dự án (Họp khởi động) kéo dài 45 phút với sự tham gia của sếp và nhân viên khách hàng.
23. Thiết kế cấu trúc tài liệu Hướng dẫn sử dụng (User Guide) tối giản dành riêng cho đối tượng nhân sự HR không có kiến thức kỹ thuật.
24. Đề xuất giải pháp kỹ thuật để nhanh chóng khôi phục hệ thống (Rollback) về phiên bản cũ khi bản update mới trên production gặp sự cố nghiêm trọng.
25. Thiết kế kế hoạch hỗ trợ kỹ thuật sau bàn giao (Post-handover Support Plan) để chuyển đổi khách hàng từ hợp đồng dự án sang hợp đồng Retainer hàng tháng.

### Level 6 — Evaluate (Đánh giá)
26. Đánh giá tính hiệu quả của phương pháp quản lý dự án Agile/Scrum so với phương pháp Thác nước (Waterfall) truyền thống trong các dự án AI có độ không định hướng cao.
27. Đánh giá rủi ro về mặt bảo mật thông tin khi bàn giao toàn bộ mã nguồn và API key cho phòng IT của khách hàng quản lý.
28. Kiểm chứng chất lượng vận hành của hệ thống sau 1 tuần go-live bằng cách thu thập ý kiến đánh giá độ hài lòng của nhân viên trực tiếp sử dụng (NPS score).
29. Đánh giá các tiêu chí kỹ thuật cần đạt để một dự án AI được coi là đủ điều kiện go-live (ví dụ: tỷ lệ lỗi < 2%, thời gian phản hồi < 4s).
30. Lập luận bác bỏ hoặc đồng ý với quan điểm: *"Agency chỉ cần làm tốt phần kỹ thuật, còn quy trình quản lý dự án hay viết tài liệu chỉ là thủ tục rườm rà làm chậm tiến độ"*.

---

## 15. Checklist hoàn thành
- [ ] Soạn thảo thành công bộ câu hỏi khảo sát Discovery Questionnaire.
- [ ] Lên được kế hoạch dự án 4 tuần chuẩn Agile cho 1 dự án mẫu.
- [ ] Viết được tài liệu Hướng dẫn sử dụng tối giản cho người dùng cuối.
- [ ] Thiết kế được Biên bản nghiệm thu bàn giao chuẩn pháp lý.
- [ ] Trả lời đúng tối thiểu 80% câu hỏi ôn tập.

---

## 16. Resources (Tài liệu tham khảo)
- **Quản lý dự án**: *Scrum: The Art of Doing Twice the Work in Half the Time by Jeff Sutherland.*
- **Đọc thêm**: *The Lean Startup by Eric Ries (Về triết lý MVP và lặp cải tiến).*
- **Phần mềm**: [Trello / Notion / Jira (Các công cụ quản lý dự án phổ biến)](https://notion.so)
