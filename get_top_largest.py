import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

DRIVES = [
    r"K:\我的云端硬盘",
    r"L:\我的云端硬盘"
]

def format_size(size_bytes):
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    elif size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} Bytes"

def analyze_largest():
    all_files = []
    folder_sizes = {}

    for drive in DRIVES:
        if not os.path.exists(drive):
            continue

        for root, dirs, files in os.walk(drive):
            # 排除回收站等系统目录
            if '$RECYCLE.BIN' in root:
                continue

            current_folder_size = 0
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    size = os.path.getsize(filepath)
                    all_files.append((filepath, size))
                    current_folder_size += size
                except Exception:
                    pass

            # 记录文件夹及其上级文件夹大小
            rel_root = root
            while rel_root and rel_root not in DRIVES and len(rel_root) > 3:
                folder_sizes[rel_root] = folder_sizes.get(rel_root, 0) + current_folder_size
                rel_root = os.path.dirname(rel_root)

    # 排序最大文件
    all_files.sort(key=lambda x: x[1], reverse=True)
    top_files = all_files[:5]

    # 排序最大文件夹
    sorted_folders = sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True)
    top_folders = sorted_folders[:5]

    print("=== TOP 5 LARGEST FILES ===")
    for path, size in top_files:
        print(f"{format_size(size)} | {path}")

    print("\n=== TOP 5 LARGEST FOLDERS ===")
    for path, size in top_folders:
        print(f"{format_size(size)} | {path}")

if __name__ == "__main__":
    analyze_largest()
