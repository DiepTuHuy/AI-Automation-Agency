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