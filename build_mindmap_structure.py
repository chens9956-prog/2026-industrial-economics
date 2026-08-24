import pymupdf
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'G:\2020年国家级课题\黄河流域图书馆\纯扫描版\科学文库\书籍6.02\基于课题或获奖的专著\第九届高校获奖著作24.2.19\3 张智光生态文明和生态安全 人与自然共生演化理论_ocr_20260824_155227.pdf'

doc = pymupdf.open(pdf_path)
toc = doc.get_toc()

# 筛选并清理 4 层结构
# L1: 全书书名
# L2: 第一篇、第二篇、第三篇
# L3: 各章节 (第一章 - 第二十一章)
# L4: 核心小节/关键要点

mindmap_data = {
    "title": "《生态文明和生态安全：人与自然共生演化理论》（张智光 著）",
    "children": []
}

current_part = None
current_chap = None

for level, title, page in toc:
    title = title.strip()
    if title.startswith("第一篇") or title.startswith("第二篇") or title.startswith("第三篇"):
        current_part = {"title": title, "children": []}
        mindmap_data["children"].append(current_part)
        current_chap = None
    elif re.match(r'^第[一二三四五六七八九十百]+章', title):
        if current_part is not None:
            current_chap = {"title": title, "children": []}
            current_part["children"].append(current_chap)
    elif re.match(r'^第[一二三四五六七八九十]+节', title) or re.match(r'^[一二三四五六七八九十]+、', title):
        if current_chap is not None and len(current_chap["children"]) < 5:
            current_chap["children"].append(title)

print(f"Part count: {len(mindmap_data['children'])}")
for p in mindmap_data["children"]:
    print(f"Part: {p['title']} (Chapters: {len(p['children'])})")
