from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# 1. Định nghĩa model ORM
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

if __name__ == "__main__":
    # Kết nối SQLite trong bộ nhớ phục vụ test nhanh
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 2. Thêm sản phẩm mới
    new_prod = Product(name="Bàn phím Leopold", price=150.0, stock=20)
    session.add(new_prod)
    session.commit()
    print(f"Đã thêm sản phẩm: {new_prod.name} (ID: {new_prod.id})")
    
    # 3. Cập nhật số lượng tồn kho
    prod_to_update = session.query(Product).filter_by(name="Bàn phím Leopold").first()
    prod_to_update.stock = 15
    session.commit()
    print(f"Đã cập nhật tồn kho mới: {prod_to_update.stock} chiếc.")