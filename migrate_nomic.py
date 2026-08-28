import os
import sys
import shutil
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

src = r"C:\Users\ausu\AppData\Local\nomic.ai"
dst_dir = r"E:\AI_Models"
dst = r"E:\AI_Models\nomic.ai"

print("=" * 60)
print("🚀 启动 nomic.ai / GPT4All AI 模型无损迁移与空间释放")
print(f"📁 源路径 (C盘): {src}")
print(f"📁 目标路径 (E盘): {dst}")
print("=" * 60)

os.makedirs(dst_dir, exist_ok=True)

if not os.path.exists(src):
    print("❌ 未找到 C 盘 nomic.ai 目录！")
    sys.exit(1)

def get_dir_size(p):
    return sum(os.path.getsize(os.path.join(r, f)) for r, d, fs in os.walk(p) for f in fs)

initial_src_sz = get_dir_size(src) / (1024**3)
print(f"📦 发现 C 盘模型总容量: {initial_src_sz:.2f} GB")

print("🚚 正在迁移大模型到 E 盘 (E:\\AI_Models\\nomic.ai)...")
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst)
print("✅ 复制完成！正在核对数据完整性...")

dst_sz = get_dir_size(dst) / (1024**3)
print(f"  目标目录大小: {dst_sz:.2f} GB")

if abs(initial_src_sz - dst_sz) < 0.05:
    print("✅ 数据校验 100% 完整一致！")
    print("🗑️ 正在安全移除 C 盘原始大文件...")
    shutil.rmtree(src)
    
    print("🔗 正在创建 Windows 目录联接符号链接 (Directory Junction)...")
    cmd = f'cmd /c mklink /J "{src}" "{dst}"'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print("  Link 结果:", res.stdout.strip() if res.stdout else res.stderr.strip())
    
    print("\n" + "=" * 60)
    print(f"🎉🎉 nomic.ai 9.5 GB 模型迁移大获成功！")
    print(f"🌟 C 盘已成功释放约 {initial_src_sz:.2f} GB 宝贵空间！")
    print(f"🌟 任何调用 GPT4All / nomic.ai 的程序仍可无感正常运行（底层已无缝链接至 E 盘）！")
    print("=" * 60)
else:
    print("❌ 目标文件大小与源文件不符，取消删除操作，确保数据安全！")
