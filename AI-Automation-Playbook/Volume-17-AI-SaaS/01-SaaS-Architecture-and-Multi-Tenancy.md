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
Hãy viết một kịch bản SQL thiết lập cơ chế kiểm tra (Check) hoặc viết một hàm Python trung gian tự động kiểm quét mọi câu lệnh SELECT gửi tới database. Nếu câu lệnh truy vấn vào bảng `customer_leads` mà thiếu điều kiện `tenant_id` trong mệnh đề WHERE, hãy lập tức ném ra ngoại lệ Security Exception để ngắt kết nối an toàn.
