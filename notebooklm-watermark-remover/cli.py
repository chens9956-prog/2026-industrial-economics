import os
import sys
import argparse
from watermark_engine import WatermarkRemover

if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="NotebookLM 水印粉碎器命令行工具 (PDF & PPTX)")
    parser.add_argument("target", help="需要去水印的 PDF/PPTX 文件路径，或文件夹路径")
    parser.add_argument("-o", "--output", help="输出文件路径或输出目录（可选）", default=None)
    parser.add_argument("--overwrite", action="store_true", help="是否直接覆盖原文件")
    parser.add_argument("--level", choices=["light", "standard", "deep"], default="standard", help="去水印强度 (默认 standard)")

    args = parser.parse_args()

    ratio_map = {
        "light": (0.18, 0.15),
        "standard": (0.25, 0.20),
        "deep": (0.30, 0.25)
    }
    rx, ry = ratio_map[args.level]
    remover = WatermarkRemover(corner_ratio_x=rx, corner_ratio_y=ry)

    if os.path.isfile(args.target):
        out = args.target if args.overwrite else args.output
        print(f"正在处理单个文件: {args.target}")
        res = remover.process_file(args.target, output_path=out)
        print(f"✅ 处理完成: {res['output_path']}")
    elif os.path.isdir(args.target):
        files_to_process = []
        for root_dir, _, files in os.walk(args.target):
            for f in files:
                if f.lower().endswith(('.pdf', '.pptx', '.ppt')) and not f.endswith('_clean.pdf') and not f.endswith('_clean.pptx'):
                    files_to_process.append(os.path.join(root_dir, f))
        
        print(f"在目录中找到 {len(files_to_process)} 个待处理文件...")
        for idx, fp in enumerate(files_to_process, 1):
            out = fp if args.overwrite else None
            try:
                res = remover.process_file(fp, output_path=out)
                print(f"[{idx}/{len(files_to_process)}] ✅ 成功: {os.path.basename(fp)} -> {os.path.basename(res['output_path'])}")
            except Exception as e:
                print(f"[{idx}/{len(files_to_process)}] ❌ 失败: {os.path.basename(fp)} ({e})")
    else:
        print(f"❌ 错误: 目标路径不存在: {args.target}")

if __name__ == "__main__":
    main()
