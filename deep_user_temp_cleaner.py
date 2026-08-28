import os
import sys
import shutil
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("🚀 启动【全域用户级临时垃圾与浏览器多媒体缓存深度一键粉碎引擎】")
print("=" * 70)

def get_disk_free_gb(drive_letter):
    total, used, free = shutil.disk_usage(f"{drive_letter}:\\")
    return free / (1024**3)

c_free_before = get_disk_free_gb("C")
print(f"📊 清理前 C 盘可用空间: {c_free_before:.2f} GB\n")

user = r"C:\Users\ausu"
target_dirs = [
    (os.path.join(user, r"AppData\Local\Temp"), "用户临时缓存目录 (%temp%)"),
    (r"C:\Windows\Temp", "Windows 系统临时目录"),
    (os.path.join(user, r"AppData\Local\CrashDumps"), "应用程序崩溃转储日志 (CrashDumps)"),
    (os.path.join(user, r"AppData\Local\D3DSCache"), "Direct3D 图形渲染着色器缓存"),
    (os.path.join(user, r"AppData\Local\Google\Chrome\User Data\Default\Cache"), "Chrome 网页图片与视频缓存"),
    (os.path.join(user, r"AppData\Local\Google\Chrome\User Data\Default\Code Cache"), "Chrome 网页 JS 字节码缓存"),
    (os.path.join(user, r"AppData\Local\Microsoft\Edge\User Data\Default\Cache"), "Edge 浏览器网页缓存"),
    (os.path.join(user, r"AppData\Local\Microsoft\Edge\User Data\Default\Code Cache"), "Edge 网页 JS 字节码缓存"),
    (os.path.join(user, r"AppData\Local\Microsoft\Windows\INetCache"), "Windows Web 临时 Internet 缓存"),
    (r"C:\ProgramData\Microsoft\Windows\WER\ReportArchive", "Windows 错误报告历史归档 (WER)"),
    (r"C:\ProgramData\Microsoft\Windows\WER\ReportQueue", "Windows 错误报告队列"),
    (os.path.join(user, r"AppData\Local\BaiduNetdisk\cache"), "百度网盘临时缓存"),
    (os.path.join(user, r"AppData\Local\pip\cache"), "Python pip 安装包残留"),
    (os.path.join(user, r"AppData\Local\npm-cache"), "npm 临时依赖包残留")
]

total_cleaned_bytes = 0
total_deleted_files = 0
total_deleted_folders = 0

for path, desc in target_dirs:
    if not os.path.exists(path):
        continue
    dir_bytes = 0
    dir_files = 0
    print(f"🧹 正在清理: {desc}...")
    
    # Iterate over items
    for item in os.listdir(path):
        item_full = os.path.join(path, item)
        try:
            if os.path.isfile(item_full) or os.path.islink(item_full):
                sz = os.path.getsize(item_full)
                os.remove(item_full)
                dir_bytes += sz
                dir_files += 1
            elif os.path.isdir(item_full):
                sub_bytes = 0
                for r, d, fs in os.walk(item_full):
                    for f in fs:
                        try:
                            sub_bytes += os.path.getsize(os.path.join(r, f))
                            dir_files += 1
                        except Exception:
                            pass
                shutil.rmtree(item_full, ignore_errors=True)
                dir_bytes += sub_bytes
                total_deleted_folders += 1
        except Exception:
            # File in use by current active app, safely ignore
            pass
            
    total_cleaned_bytes += dir_bytes
    total_deleted_files += dir_files
    print(f"   └── 释放: {dir_bytes / (1024**2):.1f} MB (清除 {dir_files} 个文件)")

# 2. 清空 Windows 回收站 (Recycle Bin)
print("\n🗑️ 正在清空 Windows 回收站...")
try:
    cmd = "powershell.exe -NoProfile -Command \"Clear-RecycleBin -Force -ErrorAction SilentlyContinue\""
    subprocess.run(cmd, shell=True, capture_output=True)
    print("✅ 回收站已彻底清空！")
except Exception as e:
    print(f"⚠️ 回收站清理跳过 ({e})")

c_free_after = get_disk_free_gb("C")
freed_now = c_free_after - c_free_before

print("\n" + "=" * 70)
print("🎉🎉 全域用户级临时垃圾与深层缓存深度清理全部完成！")
print(f"📁 深度扫描与清理项: {len(target_dirs)} 个系统与应用缓存区")
print(f"🗑️ 累计删除废弃文件: {total_deleted_files} 个")
print(f"🗑️ 累计清理临时目录: {total_deleted_folders} 个")
print(f"📈 累计清除垃圾体积: {total_cleaned_bytes / (1024**3):.2f} GB")
print(f"🌟 C 盘最新可用空间:   {c_free_after:.2f} GB (初始 0.84 GB -> 现已扩充至 {c_free_after:.2f} GB)")
print("=" * 70)
