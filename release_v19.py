# -*- coding: utf-8 -*-
"""
一键独立编译与全域自动部署脚本 v19.0
"""
import os
import sys
import shutil
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"l:\我的云端硬盘\2026产业经济学"
BUILD_DIR = r"C:\v19_release"

print("🚀 开始一键完整编译发布 v19.0 智能跳过并发旗舰版...")

# 1. 准备纯净构建目录
if os.path.exists(BUILD_DIR):
    try:
        shutil.rmtree(BUILD_DIR)
    except Exception:
        pass
os.makedirs(BUILD_DIR, exist_ok=True)

# 复制必要脚本和资源
shutil.copyfile(os.path.join(ROOT_DIR, "app_gui_pyside6.py"), os.path.join(BUILD_DIR, "app_gui_pyside6.py"))
shutil.copyfile(os.path.join(ROOT_DIR, "dual_layer_engine_pro_v9.py"), os.path.join(BUILD_DIR, "dual_layer_engine_pro_v9.py"))
shutil.copyfile(os.path.join(ROOT_DIR, "penguin_icon.png"), os.path.join(BUILD_DIR, "penguin_icon.png"))
shutil.copyfile(os.path.join(ROOT_DIR, "penguin_icon.ico"), os.path.join(BUILD_DIR, "penguin_icon.ico"))

# 2. 调用 PyInstaller 独立编译
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "--onefile",
    "--windowed",
    "--name", "DualLayerPDF_v19_Pro",
    "--icon", "penguin_icon.ico",
    "--add-data", "penguin_icon.png;.",
    "--add-data", "penguin_icon.ico;.",
    "--collect-all", "PySide6",
    "--collect-all", "shiboken6",
    "--collect-all", "rapidocr_onnxruntime",
    "--collect-all", "pymupdf",
    "--collect-all", "reportlab",
    "--collect-all", "pypdf",
    "--collect-all", "PIL",
    "--collect-all", "docx",
    "app_gui_pyside6.py"
]

print("📦 正在运行 PyInstaller 构建中 (预计 2-3 分钟)...")
t0 = time.time()
p = subprocess.run(cmd, cwd=BUILD_DIR, capture_output=True, text=True, errors='replace')
t1 = time.time()

print(f"PyInstaller 结束 (耗时: {t1-t0:.1f}s), 退出码: {p.returncode}")
if p.returncode != 0:
    print("❌ 编译失败，标准错误输出:")
    print(p.stderr[-1000:])
    sys.exit(1)

src_exe = os.path.join(BUILD_DIR, "dist", "DualLayerPDF_v19_Pro.exe")
if not os.path.exists(src_exe):
    print(f"❌ 未找到生成的可执行文件: {src_exe}")
    sys.exit(1)

size_mb = os.path.getsize(src_exe) / (1024 * 1024)
print(f"🎉 编译成功！生成文件: {src_exe} ({size_mb:.2f} MB)")

# 3. 强杀可能驻留的 OCR 进程以允许覆盖
subprocess.run(['powershell', '-Command', "Get-Process | Where-Object { $_.Path -like '*双层*' } | Stop-Process -Force -ErrorAction SilentlyContinue"], capture_output=True)
time.sleep(1)

# 4. 全域自动部署覆盖
targets = [
    r"E:\软件下载\双层可检索PDF制作神器_v19.0_智能跳过并发版.exe",
    r"E:\软件下载\双层可检索PDF制作神器.exe",
    r"C:\Users\ausu\Desktop\双层可检索PDF制作神器_v19.0_智能跳过并发版.exe"
]

for t in targets:
    os.makedirs(os.path.dirname(t), exist_ok=True)
    shutil.copyfile(src_exe, t)
    s_mb = os.path.getsize(t) / (1024 * 1024)
    mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(t)))
    print(f"  🟢 [成功部署] {t} ({s_mb:.2f} MB, {mtime})")

# 清理桌面旧版 v18.0 快捷方式以防用户混淆
old_desktop_v18 = r"C:\Users\ausu\Desktop\双层可检索PDF制作神器_v18.0_终极并发版.exe"
if os.path.exists(old_desktop_v18):
    try:
        os.remove(old_desktop_v18)
        print(f"  🧹 [已清理旧版桌面图标] {old_desktop_v18}")
    except Exception:
        pass
