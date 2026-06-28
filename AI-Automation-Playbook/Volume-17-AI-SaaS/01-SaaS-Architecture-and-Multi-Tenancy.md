# Chương 01: Kiến trúc Multi-tenancy & Cô lập dữ liệu Khách hàng

## 1. Deep Dive (Phân tích chuyên sâu)

### Từ Tự Động Hóa Đơn Lẻ sang SaaS Đa Khách Thuê (Multi-tenancy)
Khi bạn làm dịch vụ AAA: mỗi khách hàng có 1 VPS riêng, 1 database riêng. Quy trình này không thể scale khi bạn có 1,000 người dùng cá nhân đăng ký sử dụng phần mềm. Bạn không thể thuê 1,000 VPS riêng cho họ.

Chúng ta chuyển sang kiến trúc **Multi-tenancy (Đa khách thuê)**: Một máy chủ web duy nhất, một database duy nhất phục vụ đồng thời hàng nghìn khách hàng, giúp tối ưu hóa chi phí hạ tầng máy chủ về mức thấp nhất.

### Các mô hình cô lập dữ liệu (Data Isolation)
1. **Database-per-Tenant (Cô lập cấp DB)**: Mỗi khách hàng có một database vật lý riêng. 
   - *Ưu điểm*: Bảo mật tuyệt đối, dễ backup dữ liệu của từng khách hàng độc lập.
   - *Nhược điểm*: Tốn tài nguyên quản lý kết nối, khó scale lên hàng nghìn khách hàng.
2. **Shared Database, Shared Schema (Dùng chung DB và Bảng)**: Tất cả khách hàng dùng chung các bảng dữ liệu. Mỗi bảng bắt buộc phải có cột `tenant_id` để phân biệt.
   - *Ưu điểm*: Rất rẻ, cực kỳ dễ bảo trì và cập nhật schema.
   - *Nhược điểm*: Nguy cơ bảo mật cao nhất. Chỉ cần một lỗi lập trình thiếu câu lệnh filter `tenant_id` trong câu lệnh SQL, dữ liệu của khách hàng A sẽ lập tức bị lộ sang khách hàng B.

---

## 2. Demo: Thiết kế Database Multi-tenant bằng SQLAlchemy

### Mục tiêu
Định nghĩa cấu trúc bảng dữ liệu dùng chung, cấu hình cơ chế tự động chèn bộ lọc `tenant_id` để đảm bảo an toàn truy vấn.

### Mã nguồn (`multi_tenant_models.py`)
```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Bảng quản lý khách thuê (Ví dụ: Công ty A, Công ty B)
class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(String(50), primary_key=True) # Ví dụ: 'tenant_company_a'
    name = Column(String(100), nullable=False)

# Bảng dữ liệu nghiệp vụ (Dùng chung bảng vật lý)
class CustomerLead(Base):
    __tablename__ = "customer_leads"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Bắt buộc phải có khóa ngoại liên kết tới Tenant
    tenant_id = Column(String(50), ForeignKey("tenants.id"), index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    
    # Quan hệ liên kết ngược
    tenant = relationship("Tenant")

# Ví dụ về câu lệnh truy vấn an toàn bắt buộc phải dùng trong code
def get_leads_for_tenant(session, tenant_id: str):
    # Luôn luôn filter theo tenant_id ở mọi truy vấn đọc ghi
    return session.query(CustomerLead).filter(CustomerLead.tenant_id == tenant_id).all()
```

---

## 3. Mini Project

### Bài tập 1: Thiết kế cơ sở dữ liệu Multi-Tenancy cho AI SaaS (Mức độ: Trung bình)
* **Đề bài**: Hãy thiết kế cấu trúc các bảng dữ liệu SQL cơ bản cho hệ thống AI SaaS hỗ trợ nhiều doanh nghiệp đăng ký sử dụng (Multi-Tenancy) theo phương pháp chia sẻ chung database (Shared Database, Separate Schemas).
* **Mã nguồn mẫu SQL (`saas_schema.sql`)**:
```sql
-- 1. Bảng quản lý các Doanh nghiệp đăng ký (Tenants)
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    plan_type VARCHAR(20) DEFAULT 'free', -- free, premium, enterprise
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Bảng quản lý người dùng của từng Doanh nghiệp
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'member'
);
```

### Bài tập 2: Cấu hình phân tách dữ liệu Tenant trong truy vấn API (Mức độ: Khó)
* **Đề bài**: Viết mã nguồn Python mô phỏng (hoặc viết đặc tả logic) cách thức một API Endpoint của hệ thống SaaS thực hiện lọc dữ liệu: Khi một người dùng gửi request lấy danh sách hóa đơn, API phải bắt buộc kiểm tra trường `tenant_id` của người dùng đó và chỉ trả về các hóa đơn thuộc về doanh nghiệp của họ, tuyệt đối không làm lộ dữ liệu của doanh nghiệp khác.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Sử dụng SQLAlchemy ORM để tự động chèn điều kiện lọc `filter(Invoice.tenant_id == current_user.tenant_id)` cho tất cả các câu truy vấn cơ sở dữ liệu.
  - Viết mã kiểm thử để giả lập hành vi hack đổi `tenant_id` trong request và bảo đảm hệ thống chặn đứng hành vi này.
