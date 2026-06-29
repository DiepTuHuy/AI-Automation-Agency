# Chương 01: Quản lý Đường dẫn Đa nền tảng bằng `pathlib`

## 1. Deep Dive (Phân tích chuyên sâu)

### Vấn đề dấu gạch chéo đường dẫn hệ điều hành (Path Separator)
Một trong những lỗi ngớ ngẩn và phổ biến nhất của lập trình viên mới bắt đầu là viết cứng (hardcode) đường dẫn file:
- Trên Windows: `data\\files\\invoice.pdf` (Dùng dấu gạch chéo ngược)
- Trên macOS/Linux: `data/files/invoice.pdf` (Dùng dấu gạch chéo xuôi)

Khi bạn viết cứng dấu gạch chéo, script của bạn sẽ ngay lập tức crash khi chuyển đổi môi trường chạy (ví dụ từ máy Windows của bạn lên server Linux Production).

### Thư viện `pathlib` (Python 3.4+)
`pathlib` giải quyết triệt để vấn đề này bằng cách coi đường dẫn là một **Đối tượng (Object)** thay vì một chuỗi ký tự (String). Thư viện tự động nhận biết hệ điều hành đang chạy và định dạng đường dẫn chuẩn xác.

Các ưu điểm vượt trội:
- Kết nối đường dẫn an toàn bằng toán tử `/` (ví dụ: `base_dir / "files" / "doc.txt"`).
- Dễ dàng lấy thông tin file (tên file, đuôi file, thư mục cha) mà không cần dùng regex hay cắt chuỗi.
- Kiểm tra file tồn tại, tạo thư mục con đệ quy chỉ bằng một dòng lệnh.

---

## 2. Demo: Sắp xếp tài liệu tự động bằng Pathlib

### Mục tiêu
Viết một script quét qua một thư mục hỗn hợp, tự động tạo các thư mục phân loại dựa trên đuôi file (PDF, Images, Text) và di chuyển các file đó vào đúng nơi.

### Mã nguồn (`file_organizer.py`)
```python
from pathlib import Path

def organize_folder(target_dir: str):
    # Khởi tạo đối tượng Path cho thư mục mục tiêu
    target_path = Path(target_dir)
    
    if not target_path.exists():
        print(f"Thư mục {target_path} không tồn tại!")
        return

    # Quét qua toàn bộ file trong thư mục (không quét đệ quy thư mục con)
    for file_path in target_path.iterdir():
        # Bỏ qua nếu là thư mục
        if file_path.is_dir():
            continue
            
        # Lấy đuôi file (ví dụ: .pdf, .png) và chuyển thành chữ thường
        file_extension = file_path.suffix.lower().replace(".", "")
        
        if not file_extension:
            continue # Bỏ qua file không có đuôi mở rộng
            
        # Xác định thư mục đích cho loại file này
        destination_folder = target_path / file_extension
        
        # Tạo thư mục đích nếu chưa tồn tại
        destination_folder.mkdir(exist_ok=True)
        
        # Di chuyển file vào thư mục đích
        new_file_path = destination_folder / file_path.name
        file_path.rename(new_file_path)
        print(f"Đã di chuyển: {file_path.name} -> {destination_folder.name}/")

if __name__ == "__main__":
    # Tạo môi trường test cục bộ
    test_dir = Path("./test_workspace")
    test_dir.mkdir(exist_ok=True)
    
    # Tạo các file giả lập để test
    (test_dir / "report1.pdf").write_text("PDF Content")
    (test_dir / "photo.png").write_text("Image Content")
    (test_dir / "note.txt").write_text("Text Content")
    
    print("Bắt đầu sắp xếp file...")
    organize_folder(test_dir)
    print("Hoàn thành!")
```

---

## 3. Mini Project

### Bài tập 1: Tự động sắp xếp và dọn dẹp thư mục Downloads (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python sử dụng thư viện `pathlib` để tự động quét thư mục `Downloads` của máy tính. Tiến hành phân loại các tệp tin theo phần mở rộng: di chuyển `.pdf`, `.docx` vào thư mục `Documents`; `.png`, `.jpg` vào thư mục `Images`; và các tệp khác vào thư mục `Others`.
* **Mã nguồn mẫu (`clean_downloads.py`)**:
```python
from pathlib import Path
import shutil

def organize_folder(target_dir: str):
    target_path = Path(target_dir)
    if not target_path.exists():
        print(f"Thư mục {target_dir} không tồn tại.")
        return

    # Tạo các thư mục con nếu chưa có
    dirs = {
        "Documents": target_path / "Documents",
        "Images": target_path / "Images",
        "Others": target_path / "Others"
    }
    for folder in dirs.values():
        folder.mkdir(exist_ok=True)

    # Duyệt qua các tệp tin và di chuyển
    for file in target_path.iterdir():
        if file.is_file():
            suffix = file.suffix.lower()
            if suffix in ['.pdf', '.docx', '.txt']:
                shutil.move(str(file), str(dirs["Documents"] / file.name))
            elif suffix in ['.png', '.jpg', '.jpeg', '.gif']:
                shutil.move(str(file), str(dirs["Images"] / file.name))
            else:
                shutil.move(str(file), str(dirs["Others"] / file.name))
            print(f"Đã di chuyển: {file.name}")

if __name__ == "__main__":
    # Thay đổi đường dẫn đến thư mục cần dọn dẹp của bạn
    organize_folder("./test_downloads")
```

### Bài tập 2: Quét và lưu trữ log cũ theo thời gian (Mức độ: Khó)
* **Đề bài**: Viết một script Python tự động tìm kiếm tất cả các tệp có đuôi `.log` trong một thư mục dự án. Kiểm tra ngày sửa đổi cuối cùng của tệp, nếu tệp đã được sửa đổi cách đây hơn 7 ngày, hãy nén tệp đó thành định dạng `.zip` và lưu vào thư mục `archive_logs`, sau đó xóa tệp `.log` gốc để tiết kiệm bộ nhớ.
* **Yêu cầu**: Bạn hãy tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng `Path.stat().st_mtime` để lấy thời gian sửa đổi cuối cùng của tệp.
  2. Sử dụng thư viện `zipfile` của Python để thực hiện nén tệp tin.
  3. Sử dụng `Path.unlink()` để xóa tệp gốc một cách an toàn.
