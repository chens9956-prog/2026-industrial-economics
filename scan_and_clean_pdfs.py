import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_dir = r"G:\2020年国家级课题\黄河流域图书馆\纯扫描版\皮书数据库"

if not os.path.exists(target_dir):
    print(f"Error: Directory does not exist: {target_dir}")
    sys.exit(1)

matching_files = []
total_bytes = 0

for root, dirs, files in os.walk(target_dir):
    for f in files:
        if f.lower().endswith('.pdf') and 'text' in f.lower():
            full_path = os.path.join(root, f)
            try:
                size = os.path.getsize(full_path)
            except Exception:
                size = 0
            matching_files.append((full_path, size))
            total_bytes += size

print(f"扫描完成：共匹配到 {len(matching_files)} 个文件名中带有 'text' 的 PDF 文档。")
print(f"总计占用空间：{total_bytes / (1024 * 1024):.2f} MB ({total_bytes} 字节)\n")

for idx, (path, size) in enumerate(matching_files, 1):
    print(f"{idx}. [{size / (1024 * 1024):.2f} MB] {path}")

# 执行删除操作
deleted_count = 0
deleted_bytes = 0
failed_files = []

for path, size in matching_files:
    try:
        os.remove(path)
        deleted_count += 1
        deleted_bytes += size
    except Exception as e:
        failed_files.append((path, str(e)))

print(f"\n================ 删除结果汇报 ================")
print(f"成功删除文件数：{deleted_count} 个")
print(f"释放存储空间：{deleted_bytes / (1024 * 1024):.2f} MB")

if failed_files:
    print(f"失败文件数：{len(failed_files)} 个")
    for path, err in failed_files:
        print(f"失败: {path} -> {err}")
