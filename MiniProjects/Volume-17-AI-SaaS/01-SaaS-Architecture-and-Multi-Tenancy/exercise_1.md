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