import os
import hashlib
import json
from collections import defaultdict

SCAN_TARGETS = [
    "G:\\",
    "H:\\",
    "I:\\",
    "J:\\",
    "K:\\我的云端硬盘",
    "L:\\我的云端硬盘"
]

JUNK_EXTENSIONS = {'.tmp', '.bak', '.log', '.chk', '.old', '.dmp', '.DS_Store', '.swp'}
JUNK_FILES = {'thumbs.db', 'desktop.ini', '.ds_store', 'debug.log'}

def get_file_hash(filepath, block_size=65536):
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except Exception:
        return None

def scan():
    junk_list = []
    zero_byte_list = []
    size_to_files = defaultdict(list)
    
    scanned_files_count = 0
    scanned_bytes = 0

    print("Comprehensive scanning started across drives...")
    for target in SCAN_TARGETS:
        if not os.path.exists(target):
            continue
        print(f"Scanning target: {target}")
            
        for root, dirs, files in os.walk(target):
            if '$RECYCLE.BIN' in root or '.git' in root or '__pycache__' in root:
                continue

            for file in files:
                filepath = os.path.join(root, file)
                try:
                    stat = os.stat(filepath)
                    scanned_files_count += 1
                    size = stat.st_size
                    scanned_bytes += size

                    ext = os.path.splitext(file)[1].lower()
                    file_lower = file.lower()

                    if file_lower.startswith('~$') or ext in JUNK_EXTENSIONS or file_lower in JUNK_FILES:
                        junk_list.append({
                            'path': filepath,
                            'size': size,
                            'reason': '临时/垃圾文件'
                        })
                    elif size == 0:
                        zero_byte_list.append({
                            'path': filepath,
                            'size': 0,
                            'reason': '0字节文件'
                        })
                    else:
                        # 记录 50KB 以上文件的同尺寸候选
                        if size > 50 * 1024:
                            size_to_files[size].append(filepath)

                except Exception:
                    pass

    print(f"Total scanned: {scanned_files_count} files, {scanned_bytes / (1024*1024):.2f} MB")
    
    duplicate_groups = []
    candidates = {s: flist for s, flist in size_to_files.items() if len(flist) > 1}
    print(f"Hashing candidate duplicate groups ({len(candidates)} groups)...")

    for size, flist in candidates.items():
        hash_map = defaultdict(list)
        for path in flist:
            h = get_file_hash(path)
            if h:
                hash_map[h].append(path)

        for h, dup_paths in hash_map.items():
            if len(dup_paths) > 1:
                duplicate_groups.append({
                    'hash': h,
                    'size': size,
                    'total_wasted': size * (len(dup_paths) - 1),
                    'paths': dup_paths
                })

    summary = {
        'scanned_files_count': scanned_files_count,
        'scanned_bytes': scanned_bytes,
        'junk_list': junk_list,
        'zero_byte_list': zero_byte_list,
        'duplicate_groups': duplicate_groups
    }

    with open("full_scan_report.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("Full scan report written to full_scan_report.json")

if __name__ == "__main__":
    scan()
