import os
import sys
import json
import base64
import time
import numpy as np
from PIL import Image
import pymupdf as fitz
from rapidocr_onnxruntime import RapidOCR
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

json_path = r"D:\文档下载\Coding Agent 大神：Google Antigravity 最強實戰指南_全部454页数据.json"
out_clean_pdf = r"I:\4产业经济学\Coding Agent 大神：Google Antigravity 最强实战指南（全454页完整版）_100%纯净标准Adobe版.pdf"
out_searchable_pdf = r"I:\4产业经济学\Coding Agent 大神：Google Antigravity 最强实战指南（全454页完整版）_双层可检索可复制版.pdf"
backup_searchable_pdf = r"D:\文档下载\Coding Agent 大神：Google Antigravity 最强实战指南（全454页完整版）_双层可检索可复制版.pdf"

print("=" * 70)
print("🚀 启动【Google Antigravity 最强实战指南】全书 454 页终极组装与 OCR 引擎")
print(f"📖 数据来源: {json_path}")
print("=" * 70)

if not os.path.exists(json_path):
    print(f"❌ 找不到数据文件: {json_path}")
    sys.exit(1)

size_mb = os.path.getsize(json_path) / 1024 / 1024
print(f"📦 JSON 数据包大小: {size_mb:.2f} MB")

print("正在解析 JSON 数据包...")
with open(json_path, 'r', encoding='utf-8') as f:
    data_urls = json.load(f)

total_pages = len(data_urls)
print(f"🎉 成功读取 {total_pages} 个高清页面数据！正在解包高清图像...")

temp_dir = r"I:\4产业经济学\temp_antigravity_454p"
os.makedirs(temp_dir, exist_ok=True)

img_paths = []
for i, du in enumerate(data_urls):
    if ',' in du:
        raw_bytes = base64.b64decode(du.split(',')[1])
        p_name = os.path.join(temp_dir, f"page_{i+1:04d}.jpg")
        with open(p_name, "wb") as f_out:
            f_out.write(raw_bytes)
        img_paths.append(p_name)
    if (i + 1) % 100 == 0 or (i + 1) == total_pages:
        print(f"  📂 已解包 {i+1:3d} / {total_pages} 张原图...")

print("\n🖼️ 正在合成 300 DPI 出版级标准 Adobe PDF...")
pil_imgs = [Image.open(p).convert("RGB") for p in img_paths]
first_w, first_h = pil_imgs[0].size
print(f"  第一页分辨率: {first_w} x {first_h} 像素 (视网膜超清)")

pil_imgs[0].save(out_clean_pdf, "PDF", resolution=300.0, save_all=True, append_images=pil_imgs[1:])
clean_size = os.path.getsize(out_clean_pdf) / 1024 / 1024
print(f"✅ 300 DPI 超清标准版合成完毕: {out_clean_pdf} ({clean_size:.2f} MB)")

# 多线程 RapidOCR 注入双层可检索文字
print("\n🧠 正在初始化 RapidOCR 多线程并发引擎注入透明文字层...")
engine = RapidOCR()

def ocr_single_page(idx, img_path):
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    img_np = np.array(img)
    ocr_result, _ = engine(img_np)
    return idx, w, h, img_path, ocr_result

start_time = time.time()
ocr_map = {}

print(f"⚡ 开始多线程并发 OCR 识别全书 {total_pages} 页...")
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(ocr_single_page, i, p) for i, p in enumerate(img_paths)]
    completed = 0
    for future in as_completed(futures):
        idx, w, h, p_path, ocr_res = future.result()
        ocr_map[idx] = (w, h, p_path, ocr_res)
        completed += 1
        if completed % 50 == 0 or completed == total_pages:
            elapsed = time.time() - start_time
            speed = completed / max(0.1, elapsed)
            eta = (total_pages - completed) / max(0.1, speed)
            print(f"  ⚡ OCR 进度: {completed:3d} / {total_pages} 页 ({completed/total_pages*100:5.1f}%) | 速度: {speed:3.1f} 页/秒 | 剩余: {eta:3.0f}秒", flush=True)

print("\n📦 正在构建注入双层文字的最终 PDF 文档...")
searchable_doc = fitz.open()

for i in range(total_pages):
    w, h, p_path, ocr_res = ocr_map[i]
    # Standard PDF points (72 DPI scale)
    pt_w = w * 72.0 / 300.0
    pt_h = h * 72.0 / 300.0
    scale = pt_w / float(w)
    
    new_page = searchable_doc.new_page(width=pt_w, height=pt_h)
    new_page.insert_image(fitz.Rect(0, 0, pt_w, pt_h), filename=p_path)
    
    if ocr_res:
        for item in ocr_res:
            box, text, score = item[0], item[1], item[2]
            x_min = min(b[0] for b in box) * scale
            x_max = max(b[0] for b in box) * scale
            y_min = min(b[1] for b in box) * scale
            y_max = max(b[1] for b in box) * scale
            
            font_size = max(5.0, (y_max - y_min) * 0.82)
            try:
                new_page.insert_textbox(
                    fitz.Rect(x_min, y_min, x_max, y_max),
                    text,
                    fontsize=font_size,
                    fontname="helv",
                    render_mode=3
                )
            except Exception:
                try:
                    new_page.insert_text(
                        fitz.Point(x_min, y_max - 1),
                        text,
                        fontsize=font_size,
                        fontname="helv",
                        render_mode=3
                    )
                except Exception:
                    pass

print("💾 正在写入目标文件到磁盘...")
searchable_doc.save(out_searchable_pdf, garbage=3, deflate=True)
searchable_doc.close()

searchable_sz = os.path.getsize(out_searchable_pdf) / 1024 / 1024
print(f"✅ 双层 PDF 已生成: {out_searchable_pdf} ({searchable_sz:.2f} MB)")

# 复制到下载备份目录
import shutil
shutil.copy2(out_searchable_pdf, backup_searchable_pdf)
print(f"✅ 已同步备份到: {backup_searchable_pdf}")

# 清理临时原图
for p in img_paths:
    try: os.remove(p)
    except Exception: pass
try: os.rmdir(temp_dir)
except Exception: pass

total_time = time.time() - start_time
print("=" * 70)
print(f"🎉🎉 全书 454 页超清双层可检索/可复制 PDF 组装大获成功！")
print(f"📁 主保存路径: {out_searchable_pdf}")
print(f"📁 下载备份路径: {backup_searchable_pdf}")
print(f"📊 全书总页数: {total_pages} 页")
print(f"📦 文件体积: {searchable_sz:.2f} MB")
print(f"⏱️ 总耗时: {total_time:.1f} 秒")
print("=" * 70)
