import os
import sys

# 保证无论从何处启动，均将当前脚本所在目录置于 sys.path 和当前工作目录首位
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
try:
    os.chdir(current_dir)
except Exception:
    pass

import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import pymupdf
from PIL import Image, ImageTk, ImageDraw

try:
    from watermark_engine import WatermarkRemover
except Exception as e:
    # 错误弹窗防呆
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("启动错误", f"无法加载核心模块 watermark_engine:\n{e}")
    sys.exit(1)

class ModernWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ NotebookLM / Gemini 水印粉碎器 Pro (精准无痕版)")
        self.root.geometry("860x680")
        self.root.minsize(800, 620)
        self.root.configure(bg="#f8fafc")

        # 设置可爱萌宠图标
        icon_ico = os.path.join(current_dir, "app_icon.ico")
        icon_png = os.path.join(current_dir, "app_icon.png")
        if os.path.exists(icon_ico):
            try:
                self.root.iconbitmap(icon_ico)
            except Exception:
                pass
        if os.path.exists(icon_png):
            try:
                img_icon = ImageTk.PhotoImage(file=icon_png)
                self.root.iconphoto(True, img_icon)
            except Exception:
                pass

        self.selected_files = []
        self.preview_doc = None
        self.preview_img_tk = None
        self.custom_color_hex = "#ffffff"

        self.setup_styles()
        self.create_layout()

    def setup_styles(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except Exception:
            pass

        self.primary_color = "#1E40AF"
        self.accent_color = "#2563EB"
        self.bg_color = "#f8fafc"

        self.style.configure("TLabel", background=self.bg_color, font=("Microsoft YaHei", 9))
        self.style.configure("Header.TLabel", font=("Microsoft YaHei", 14, "bold"), foreground="#1e293b", background=self.bg_color)
        self.style.configure("SubHeader.TLabel", font=("Microsoft YaHei", 9), foreground="#64748b", background=self.bg_color)
        
        self.style.configure("Action.TButton", font=("Microsoft YaHei", 10, "bold"), background=self.accent_color, foreground="#ffffff", padding=6)
        self.style.map("Action.TButton", background=[("active", "#1d4ed8")])

        self.style.configure("Secondary.TButton", font=("Microsoft YaHei", 9), background="#e2e8f0", foreground="#1e293b", padding=4)
        self.style.map("Secondary.TButton", background=[("active", "#cbd5e1")])

    def create_layout(self):
        # 1. 顶部 Header
        header = tk.Frame(self.root, bg="#f8fafc", padx=20, pady=12)
        header.pack(fill="x")

        title = ttk.Label(header, text="✨ NotebookLM / Gemini 课件去水印 Pro", style="Header.TLabel")
        title.pack(anchor="w")
        subtitle = ttk.Label(header, text="精准定位“Gemini Notebook / NotebookLM”微型水印 · 智能周边吸色融合同步 · 0 痕迹无损去标", style="SubHeader.TLabel")
        subtitle.pack(anchor="w", pady=(2, 0))

        # 2. 中间左右分栏
        content_frame = tk.Frame(self.root, bg="#f8fafc", padx=20)
        content_frame.pack(fill="both", expand=True)

        # 左侧：文件列表与操作 (占 55% 宽)
        left_pane = tk.Frame(content_frame, bg="#ffffff", bd=1, relief="solid", highlightbackground="#e2e8f0")
        left_pane.pack(side="left", fill="both", expand=True, padx=(0, 10))

        btn_bar = tk.Frame(left_pane, bg="#ffffff", padx=10, pady=10)
        btn_bar.pack(fill="x")

        btn_add_files = ttk.Button(btn_bar, text="📁 添加文件", style="Secondary.TButton", command=self.add_files)
        btn_add_files.pack(side="left", padx=(0, 6))

        btn_add_dir = ttk.Button(btn_bar, text="📂 添加文件夹", style="Secondary.TButton", command=self.add_dir)
        btn_add_dir.pack(side="left", padx=(0, 6))

        btn_clear = ttk.Button(btn_bar, text="🗑️ 清空", style="Secondary.TButton", command=self.clear_files)
        btn_clear.pack(side="right")

        # 列表视图
        list_frame = tk.Frame(left_pane, bg="#ffffff", padx=10)
        list_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(list_frame, columns=("name", "size", "status"), show="headings", height=10)
        self.tree.heading("name", text="文件名称", anchor="w")
        self.tree.heading("size", text="大小", anchor="center")
        self.tree.heading("status", text="状态", anchor="center")

        self.tree.column("name", width=220, anchor="w")
        self.tree.column("size", width=65, anchor="center")
        self.tree.column("status", width=75, anchor="center")

        scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_file_select)

        # 覆盖原文件复选框
        self.overwrite_var = tk.BooleanVar(value=False)
        chk_box = tk.Checkbutton(left_pane, text="直接覆盖原文件 (默认另存为 _clean 文件)", variable=self.overwrite_var, bg="#ffffff", font=("Microsoft YaHei", 8), fg="#dc2626")
        chk_box.pack(anchor="w", padx=12, pady=6)

        # 右侧：精准参数微调与右下角实时预览 (占 45% 宽)
        right_pane = tk.Frame(content_frame, bg="#ffffff", bd=1, relief="solid", highlightbackground="#e2e8f0", padx=12, pady=10)
        right_pane.pack(side="right", fill="both", expand=False)
        right_pane.config(width=360)

        tk.Label(right_pane, text="🎯 水印定位与色彩协调设置", bg="#ffffff", font=("Microsoft YaHei", 10, "bold"), fg="#1e293b").pack(anchor="w", pady=(0, 6))

        # 定位模式
        mode_frame = tk.Frame(right_pane, bg="#ffffff")
        mode_frame.pack(fill="x", pady=2)
        tk.Label(mode_frame, text="定位算法：", bg="#ffffff", font=("Microsoft YaHei", 9)).pack(side="left")
        self.mode_var = tk.StringVar(value="smart")
        r_smart = tk.Radiobutton(mode_frame, text="智能文本精准定位 (首选)", variable=self.mode_var, value="smart", bg="#ffffff", font=("Microsoft YaHei", 8, "bold"), fg="#2563eb", command=self.update_preview)
        r_smart.pack(side="left")
        r_manual = tk.Radiobutton(mode_frame, text="手动微调", variable=self.mode_var, value="manual", bg="#ffffff", font=("Microsoft YaHei", 8), command=self.update_preview)
        r_manual.pack(side="left")

        # 背景颜色融合同步
        color_frame = tk.Frame(right_pane, bg="#ffffff")
        color_frame.pack(fill="x", pady=4)
        tk.Label(color_frame, text="背景协调：", bg="#ffffff", font=("Microsoft YaHei", 9)).pack(side="left")
        self.color_mode_var = tk.StringVar(value="auto")
        r_auto = tk.Radiobutton(color_frame, text="智能吸取底色", variable=self.color_mode_var, value="auto", bg="#ffffff", font=("Microsoft YaHei", 8, "bold"), fg="#059669", command=self.update_preview)
        r_auto.pack(side="left")
        r_white = tk.Radiobutton(color_frame, text="纯白", variable=self.color_mode_var, value="white", bg="#ffffff", font=("Microsoft YaHei", 8), command=self.update_preview)
        r_white.pack(side="left")
        r_pick = tk.Radiobutton(color_frame, text="自选色", variable=self.color_mode_var, value="custom", bg="#ffffff", font=("Microsoft YaHei", 8), command=self.choose_custom_color)
        r_pick.pack(side="left")

        # 手工微调滑块 (宽/高/边距)
        slider_frame = tk.LabelFrame(right_pane, text="手工微调尺寸 (单位: pt)", bg="#ffffff", font=("Microsoft YaHei", 8))
        slider_frame.pack(fill="x", pady=5, padx=2)

        # 宽度
        w_f = tk.Frame(slider_frame, bg="#ffffff")
        w_f.pack(fill="x", pady=1)
        tk.Label(w_f, text="宽度:", bg="#ffffff", font=("Microsoft YaHei", 8), width=5).pack(side="left")
        self.w_var = tk.IntVar(value=145)
        self.w_slider = tk.Scale(w_f, from_=80, to=250, orient="horizontal", variable=self.w_var, bg="#ffffff", bd=0, highlightthickness=0, command=lambda x: self.update_preview())
        self.w_slider.pack(side="left", fill="x", expand=True)

        # 高度
        h_f = tk.Frame(slider_frame, bg="#ffffff")
        h_f.pack(fill="x", pady=1)
        tk.Label(h_f, text="高度:", bg="#ffffff", font=("Microsoft YaHei", 8), width=5).pack(side="left")
        self.h_var = tk.IntVar(value=26)
        self.h_slider = tk.Scale(h_f, from_=15, to=60, orient="horizontal", variable=self.h_var, bg="#ffffff", bd=0, highlightthickness=0, command=lambda x: self.update_preview())
        self.h_slider.pack(side="left", fill="x", expand=True)

        # 右边距 & 底边距
        m_f = tk.Frame(slider_frame, bg="#ffffff")
        m_f.pack(fill="x", pady=1)
        tk.Label(m_f, text="右距:", bg="#ffffff", font=("Microsoft YaHei", 8), width=5).pack(side="left")
        self.mr_var = tk.IntVar(value=10)
        self.mr_slider = tk.Scale(m_f, from_=0, to=50, orient="horizontal", variable=self.mr_var, bg="#ffffff", bd=0, highlightthickness=0, command=lambda x: self.update_preview())
        self.mr_slider.pack(side="left", fill="x", expand=True)

        mb_f = tk.Frame(slider_frame, bg="#ffffff")
        mb_f.pack(fill="x", pady=1)
        tk.Label(mb_f, text="底距:", bg="#ffffff", font=("Microsoft YaHei", 8), width=5).pack(side="left")
        self.mb_var = tk.IntVar(value=10)
        self.mb_slider = tk.Scale(mb_f, from_=0, to=50, orient="horizontal", variable=self.mb_var, bg="#ffffff", bd=0, highlightthickness=0, command=lambda x: self.update_preview())
        self.mb_slider.pack(side="left", fill="x", expand=True)

        # 实时预览区域
        preview_box = tk.LabelFrame(right_pane, text="右下角效果实时预览", bg="#ffffff", font=("Microsoft YaHei", 8))
        preview_box.pack(fill="both", expand=True, pady=(4, 0))

        self.preview_canvas = tk.Canvas(preview_box, bg="#f1f5f9", height=130, highlightthickness=0)
        self.preview_canvas.pack(fill="both", expand=True, padx=4, pady=4)

        # 3. 底部状态与操作栏
        footer = tk.Frame(self.root, bg="#f8fafc", padx=20, pady=12)
        footer.pack(fill="x")

        self.progress = ttk.Progressbar(footer, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=(0, 8))

        self.status_lbl = ttk.Label(footer, text="就绪：请添加 NotebookLM 生成的 PDF / PPTX 文件", style="SubHeader.TLabel")
        self.status_lbl.pack(side="left")

        self.btn_exec = ttk.Button(footer, text="🚀 开始精准去水印", style="Action.TButton", command=self.run_process)
        self.btn_exec.pack(side="right")

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="选择 PDF 或 PPTX 文件",
            filetypes=[("PDF & PPTX 文件", "*.pdf;*.pptx;*.ppt"), ("PDF 课件", "*.pdf"), ("PowerPoint 演示文稿", "*.pptx;*.ppt")]
        )
        if files:
            for f in files:
                if f not in self.selected_files:
                    self.selected_files.append(f)
                    self.tree.insert("", "end", values=(os.path.basename(f), f"{os.path.getsize(f)/1024:.1f} KB", "待处理"))
            self.status_lbl.config(text=f"已载入 {len(self.selected_files)} 个文件")
            # 自动预览第一个 PDF
            self.load_preview(self.selected_files[0])

    def add_dir(self):
        d = filedialog.askdirectory(title="选择包含课件的文件夹")
        if d:
            added = 0
            for root_dir, _, files in os.walk(d):
                for f in files:
                    if f.lower().endswith(('.pdf', '.pptx', '.ppt')) and not f.endswith('_clean.pdf') and not f.endswith('_clean.pptx'):
                        full_p = os.path.join(root_dir, f)
                        if full_p not in self.selected_files:
                            self.selected_files.append(full_p)
                            self.tree.insert("", "end", values=(os.path.basename(full_p), f"{os.path.getsize(full_p)/1024:.1f} KB", "待处理"))
                            added += 1
            self.status_lbl.config(text=f"新增 {added} 个文件，当前共 {len(self.selected_files)} 个")
            if self.selected_files:
                self.load_preview(self.selected_files[0])

    def clear_files(self):
        self.selected_files.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.preview_doc = None
        self.preview_canvas.delete("all")
        self.status_lbl.config(text="列表已清空")
        self.progress["value"] = 0

    def on_file_select(self, event):
        sel = self.tree.selection()
        if sel:
            idx = self.tree.index(sel[0])
            if idx < len(self.selected_files):
                self.load_preview(self.selected_files[idx])

    def choose_custom_color(self):
        color = colorchooser.askcolor(title="选择水印消除填充背景色")
        if color[1]:
            self.custom_color_hex = color[1]
            self.color_mode_var.set("custom")
            self.update_preview()

    def load_preview(self, file_path):
        if not file_path.lower().endswith('.pdf'):
            self.preview_canvas.delete("all")
            self.preview_canvas.create_text(150, 60, text="[PPTX 矢量无痕删除模式]\n无需预览擦除块，底层图形将 100% 抹除", fill="#64748b", font=("Microsoft YaHei", 9), justify="center")
            return
        try:
            self.preview_doc = pymupdf.open(file_path)
            self.update_preview()
        except Exception as e:
            print("Preview error:", e)

    def update_preview(self):
        if not self.preview_doc:
            return

        page = self.preview_doc[0]
        pw = page.rect.width
        ph = page.rect.height

        # 截取右下角 35% x 25% 区域用于放大显示
        clip_rect = pymupdf.Rect(pw * 0.65, ph * 0.75, pw, ph)
        pix = page.get_pixmap(clip=clip_rect, dpi=120)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # 确定水印抹除框
        mode = self.mode_var.get()
        target_rect = None

        if mode == "smart":
            for kw in ["Gemini Notebook", "Gemini", "NotebookLM", "Notebook"]:
                rects = page.search_for(kw)
                for r in rects:
                    if r.x0 >= pw * 0.60 and r.y0 >= ph * 0.75:
                        target_rect = pymupdf.Rect(max(0, r.x0 - 26), max(0, r.y0 - 3), min(pw, r.x1 + 4), min(ph, r.y1 + 4))
                        break
                if target_rect:
                    break

        if not target_rect:
            bw = self.w_var.get()
            bh = self.h_var.get()
            mr = self.mr_var.get()
            mb = self.mb_var.get()
            target_rect = pymupdf.Rect(pw - mr - bw, ph - mb - bh, pw - mr, ph - mb)

        # 将 target_rect 映射到 clip 坐标系
        scale_x = pix.width / clip_rect.width
        scale_y = pix.height / clip_rect.height

        x0 = (target_rect.x0 - clip_rect.x0) * scale_x
        y0 = (target_rect.y0 - clip_rect.y0) * scale_y
        x1 = (target_rect.x1 - clip_rect.x0) * scale_x
        y1 = (target_rect.y1 - clip_rect.y0) * scale_y

        draw = ImageDraw.Draw(img)
        # 绘制半透明消除红框标识
        draw.rectangle([x0, y0, x1, y1], outline="#ef4444", width=2)

        # 缩放至 Canvas
        c_w = self.preview_canvas.winfo_width() or 300
        c_h = self.preview_canvas.winfo_height() or 130
        img.thumbnail((c_w, c_h), Image.Resampling.LANCZOS)

        self.preview_img_tk = ImageTk.PhotoImage(img)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(c_w//2, c_h//2, image=self.preview_img_tk)

    def run_process(self):
        if not self.selected_files:
            messagebox.showwarning("提示", "请先添加待处理的 PDF 或 PPTX 文件！")
            return

        self.btn_exec.config(state="disabled")
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        mode = self.mode_var.get()
        cbox = {
            "width_pt": self.w_var.get(),
            "height_pt": self.h_var.get(),
            "margin_right_pt": self.mr_var.get(),
            "margin_bottom_pt": self.mb_var.get()
        }
        color_mode = self.color_mode_var.get()

        # 解析自选 RGB
        c_rgb = (1.0, 1.0, 1.0)
        if color_mode == "custom" and self.custom_color_hex:
            h = self.custom_color_hex.lstrip('#')
            c_rgb = tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))

        remover = WatermarkRemover(
            mode=mode,
            custom_box=cbox,
            bg_color_mode=color_mode,
            custom_bg_rgb=c_rgb
        )

        total = len(self.selected_files)
        overwrite = self.overwrite_var.get()
        success = 0

        tree_items = self.tree.get_children()

        for idx, (item_id, fp) in enumerate(zip(tree_items, self.selected_files)):
            try:
                self.tree.set(item_id, "status", "处理中...")
                self.status_lbl.config(text=f"正在处理 ({idx+1}/{total}): {os.path.basename(fp)}")
                
                out_path = fp if overwrite else None
                remover.process_file(fp, output_path=out_path)
                
                self.tree.set(item_id, "status", "✅ 成功")
                success += 1
            except Exception as e:
                self.tree.set(item_id, "status", "❌ 失败")
                print("Error on", fp, e)

            self.progress["value"] = int(((idx + 1) / total) * 100)

        self.btn_exec.config(state="normal")
        self.status_lbl.config(text=f"🎉 处理完成！成功处理 {success}/{total} 个文件")

        if success > 0:
            first_dir = os.path.dirname(self.selected_files[0])
            if messagebox.askyesno("完成", f"已成功精准去除 {success} 个文件中的水印！\n是否打开所在文件夹查看？"):
                os.startfile(first_dir)

def main():
    root = tk.Tk()
    app = ModernWatermarkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
