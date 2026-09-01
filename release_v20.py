# -*- coding: utf-8 -*-
"""
一键全自动纯净编译部署 v20.0 硬件级控温丝滑版
"""

import os
import sys
import shutil
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8')

def build_and_deploy():
    print("🚀 开始编译发布 v20.0 硬件控温丝滑版（五重硬件 CPU 治理 · 物理硬隔离 · 0 鼠标卡顿）...")
    
    release_dir = r"C:\v20_release"
    os.makedirs(release_dir, exist_ok=True)
    
    src_gui = r"l:\我的云端硬盘\2026产业经济学\app_gui_pyside6.py"
    src_eng = r"l:\我的云端硬盘\2026产业经济学\dual_layer_engine_pro_v9.py"
    src_icon_png = r"l:\我的云端硬盘\2026产业经济学\penguin_icon.png"
    src_icon_ico = r"l:\我的云端硬盘\2026产业经济学\penguin_icon.ico"
    
    shutil.copyfile(src_gui, os.path.join(release_dir, "app_gui_pyside6.py"))
    shutil.copyfile(src_eng, os.path.join(release_dir, "dual_layer_engine_pro_v9.py"))
    shutil.copyfile(src_icon_png, os.path.join(release_dir, "penguin_icon.png"))
    shutil.copyfile(src_icon_ico, os.path.join(release_dir, "penguin_icon.ico"))
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name", "DualLayerPDF_v20_Pro",
        "--icon", "penguin_icon.ico",
        "--add-data", "penguin_icon.png;.",
        "--add-data", "penguin_icon.ico;.",
        "--collect-all", "PySide6",
        "--collect-all", "rapidocr_onnxruntime",
        "--collect-all", "pymupdf",
        "--collect-all", "reportlab",
        "--collect-all", "pypdf",
        "--collect-all", "PIL",
        "--collect-all", "docx",
        "app_gui_pyside6.py"
    ]
    
    print("📦 正在运行 PyInstaller 构建中...")
    t0 = time.time()
    res = subprocess.run(cmd, cwd=release_dir, capture_output=True, text=True, errors="replace")
    cost = time.time() - t0
    
    if res.returncode != 0:
        print("❌ 编译失败:", res.stderr)
        return
        
    dist_exe = os.path.join(release_dir, "dist", "DualLayerPDF_v20_Pro.exe")
    if not os.path.exists(dist_exe):
        print("❌ 未找到生成的 EXE 文件！")
        return
        
    size_mb = os.path.getsize(dist_exe) / (1024 ** 2)
    print(f"🎉 编译成功！生成文件: {dist_exe} ({size_mb:.2f} MB, 耗时: {cost:.1f}s)")
    
    # 强杀旧进程防止写入冲突
    try:
        subprocess.run(["powershell", "-Command", "Get-Process | Where-Object { $_.Path -like '*双层*' } | Stop-Process -Force -ErrorAction SilentlyContinue"], capture_output=True)
    except Exception:
        pass
    time.sleep(1)
    
    deploy_targets = [
        r"E:\软件下载\双层可检索PDF制作神器_v20.0_硬件控温丝滑版.exe",
        r"E:\软件下载\双层可检索PDF制作神器.exe",
        r"C:\Users\ausu\Desktop\双层可检索PDF制作神器_v20.0_硬件控温丝滑版.exe"
    ]
    
    for t in deploy_targets:
        try:
            os.makedirs(os.path.dirname(t), exist_ok=True)
            shutil.copyfile(dist_exe, t)
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(t)))
            print(f"  🟢 [成功部署] {t} ({os.path.getsize(t)/(1024**2):.2f} MB, {mtime})")
        except Exception as e:
            print(f"  ⚠️ 部署失败 {t}: {e}")

    # 清理所有旧版快捷方式与文件
    old_files = [
        r"C:\Users\ausu\Desktop\双层可检索PDF制作神器_v19.2_极速丝滑并发版.exe",
        r"C:\Users\ausu\Desktop\双层可检索PDF制作神器_v19.0_智能跳过并发版.exe",
        r"C:\Users\ausu\Desktop\双层可检索PDF制作神器_v18.0_终极并发版.exe",
        r"E:\软件下载\双层可检索PDF制作神器_v19.2_极速丝滑并发版.exe",
        r"E:\软件下载\双层可检索PDF制作神器_v19.0_智能跳过并发版.exe",
        r"E:\软件下载\双层可检索PDF制作神器_v18.0_终极并发版.exe"
    ]
    for old_f in old_files:
        if os.path.exists(old_f):
            try:
                os.remove(old_f)
                print(f"  🧹 [已清理旧版]: {old_f}")
            except Exception:
                pass

if __name__ == "__main__":
    build_and_deploy()
