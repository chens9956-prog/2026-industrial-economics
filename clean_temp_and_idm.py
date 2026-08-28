import os
import sys
import shutil
import time

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 65)
print("🚀 启动【%temp% 临时垃圾与 IDM 缓存深度安全清理引擎】")
print("=" * 65)

def get_disk_free_gb(drive_letter):
    total, used, free = shutil.disk_usage(f"{drive_letter}:\\")
    return free / (1024**3)

c_free_before = get_disk_free_gb("C")
print(f"📊 清理前 C 盘可用空间: {c_free_before:.2f} GB")

cleaned_bytes = 0
deleted_files = 0
deleted_dirs = 0

def safe_clean_folder(folder_path, desc):
    global cleaned_bytes, deleted_files, deleted_dirs
    if not os.path.exists(folder_path):
        print(f"⚠️ 目录不存在，跳过: {folder_path}")
        return
    print(f"\n🧹 正在清理: {desc} ({folder_path})...")
    
    # Clean sub-items inside folder_path
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                sz = os.path.getsize(item_path)
                os.remove(item_path)
                cleaned_bytes += sz
                deleted_files += 1
            elif os.path.isdir(item_path):
                # Calculate size before removal
                for root, dirs, files in os.walk(item_path):
                    for f in files:
                        try:
                            cleaned_bytes += os.path.getsize(os.path.join(root, f))
                            deleted_files += 1
                        except Exception:
                            pass
                shutil.rmtree(item_path, ignore_errors=True)
                deleted_dirs += 1
        except Exception as e:
            # File locked by currently running app, safely skip
            pass

# 1. IDM DwnlData 临时碎片 (5.36 GB)
safe_clean_folder(r"C:\Users\ausu\AppData\Roaming\IDM\DwnlData", "IDM 历史下载临时分段碎片")

# 2. 用户级 Temp 目录 (%temp%)
safe_clean_folder(r"C:\Users\ausu\AppData\Local\Temp", "用户临时文件目录 (%temp%)")

# 3. 系统级 Temp 目录
safe_clean_folder(r"C:\Windows\Temp", "Windows 系统临时文件目录")

# 4. npm-cache 与 pnpm-cache 缓存
safe_clean_folder(r"C:\Users\ausu\AppData\Local\npm-cache", "NPM 开发构建包缓存")
safe_clean_folder(r"C:\Users\ausu\AppData\Local\pnpm-cache", "PNPM 依赖包缓存")
safe_clean_folder(r"C:\Users\ausu\AppData\Local\pip\cache", "Python Pip 下载包缓存")

# 5. 360 补丁缓存 (如果存在)
safe_clean_folder(r"C:\Users\ausu\AppData\Roaming\360Safe\CloudPatch\WinPatch", "360 历史补丁离线包")

c_free_after = get_disk_free_gb("C")
freed_gb = c_free_after - c_free_before

print("\n" + "=" * 65)
print("🎉🎉 临时文件与 IDM 碎片深度清理大获成功！")
print(f"🗑️ 共删除临时废弃文件: {deleted_files} 个")
print(f"🗑️ 共清理临时子目录:   {deleted_dirs} 个")
print(f"📈 累计释放空间:       {cleaned_bytes / (1024**3):.2f} GB (物理盘释放约 {freed_gb:.2f} GB)")
print(f"🌟 C 盘当前最新可用空间: {c_free_after:.2f} GB")
print("=" * 65)
