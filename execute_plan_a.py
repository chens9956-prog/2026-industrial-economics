import os
import sys
import json
import shutil

sys.stdout.reconfigure(encoding='utf-8')

BACKUP_ROOT = r"F:\_Drive_Clean_Backup_"
REPORT_FILE = "full_scan_report.json"

def execute_plan_a():
    if not os.path.exists(REPORT_FILE):
        print(f"Report file {REPORT_FILE} not found!")
        return

    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    junk_list = data.get("junk_list", [])
    zero_byte_list = data.get("zero_byte_list", [])
    dup_groups = data.get("duplicate_groups", [])

    os.makedirs(BACKUP_ROOT, exist_ok=True)
    print(f"Backup isolation directory created: {BACKUP_ROOT}")

    moved_junk_count = 0
    moved_junk_bytes = 0

    moved_dup_count = 0
    moved_dup_bytes = 0

    # 1. 移动垃圾文件与 0 字节文件
    print("\n[Phase 1] Moving junk and zero-byte files to isolation...")
    for item in junk_list + zero_byte_list:
        src = item["path"]
        if os.path.exists(src):
            try:
                # 保持相对路径结构
                rel_path = src.replace(":", "")
                if rel_path.startswith("\\") or rel_path.startswith("/"):
                    rel_path = rel_path[1:]
                dest = os.path.join(BACKUP_ROOT, "Junk_And_ZeroByte", rel_path)
                os.makedirs(os.path.dirname(dest), exist_ok=True)

                sz = os.path.getsize(src)
                shutil.move(src, dest)
                moved_junk_count += 1
                moved_junk_bytes += sz
            except Exception as e:
                print(f"Failed to move {src}: {e}")

    # 2. 移动重复文件副本（第一份作为主文件留着，第二份及之后移动到隔离区）
    print("\n[Phase 2] Moving duplicate file copies to isolation...")
    for grp in dup_groups:
        paths = grp.get("paths", [])
        if len(paths) <= 1:
            continue

        # 第 0 个保留为主文件
        master_path = paths[0]
        duplicates_to_move = paths[1:]

        for src in duplicates_to_move:
            if os.path.exists(src) and src != master_path:
                try:
                    rel_path = src.replace(":", "")
                    if rel_path.startswith("\\") or rel_path.startswith("/"):
                        rel_path = rel_path[1:]
                    dest = os.path.join(BACKUP_ROOT, "Duplicate_Copies", rel_path)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)

                    sz = os.path.getsize(src)
                    shutil.move(src, dest)
                    moved_dup_count += 1
                    moved_dup_bytes += sz
                except Exception as e:
                    print(f"Failed to move duplicate {src}: {e}")

    moved_total_mb = (moved_junk_bytes + moved_dup_bytes) / (1024 * 1024)
    moved_total_gb = moved_total_mb / 1024

    print("\n=== PLAN A EXECUTION COMPLETED ===")
    print(f"Isolated Junk/Zero-Byte Files: {moved_junk_count} files ({moved_junk_bytes / (1024*1024):.2f} MB)")
    print(f"Isolated Duplicate Copies: {moved_dup_count} files ({moved_dup_bytes / (1024*1024):.2f} MB)")
    print(f"Total Isolated Space Freed: {moved_total_mb:.2f} MB ({moved_total_gb:.2f} GB)")
    print(f"All isolated files safely moved to: {BACKUP_ROOT}")

if __name__ == "__main__":
    execute_plan_a()
