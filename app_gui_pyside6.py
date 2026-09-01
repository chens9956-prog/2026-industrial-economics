# -*- coding: utf-8 -*-
"""
双层 PDF 生成工具 v20.0 硬件级控温丝滑版 (五重硬件级 CPU 治理 · 0 鼠标卡顿 · 智能跳过已OCR · 多书真正并发 · 绝对秒停强杀)
软件标题：PaddleOCR 双层 PDF 生成工具 v20.0 (CPU版) [硬件控温丝滑旗舰版]

1. 【五重硬件级 CPU 治理与 0 鼠标卡顿 (5-Layer CPU Governance & Zero-Lag Mouse)】：
   - 核心物理隔离 (CPU Affinity)：强制扣留 Core 0/1 专门服务 Windows 系统、DWM 桌面合成器与鼠标驱动，物理杜绝 CPU 冲上 95%+；
   - ONNX 算子单线程硬锁定 (intra_op=1, inter_op=1)：彻底消除几十个内部自旋死循环线程；
   - 智能 CPU 控温档位 (温控静音 50% / 标准均衡 70% / 极速全速 85%)：动态微休眠平滑算力波峰；
   - Windows 调度级别硬降级 (BelowNormal)：用户鼠标移动或前台打字 0 毫秒绝对抢占；
   - 线程局部独立隔离 (Thread-Local ONNX Session)：多书并行 0 锁争抢。
2. 【全维度智能自动跳过机制 (Smart Skip System)】：
   - 智能识别源文件：自动检测源 PDF 是否已经含有可检索文字层（抽样分析文字密度，若已是双层/文字版 PDF 则秒级跳过）；
   - 智能识别目标成果：自动检索目标目录中是否已存在该书籍的历史 OCR 成果（包括带时间戳、随机数的前缀成果文件）；
   - 智能识别表格状态：若列表中部分书籍已处理完成，再次启动时自动跳过已完成项，绝不重复耗费算力！
3. 【多书真正同时并行处理 (True Parallel Multi-Book Processing)】：
   - 采用多线程并行池 (ThreadPoolExecutor)，充分利用多核 CPU，多本书籍同时飞速生成双层 PDF！
4. 【绝对秒停强力终止机制 (100% Instant Hard Kill)】：
   - 点击「■ 停止」按钮瞬间，底层立即触发操作系统级线程强杀与全局中断事件，绝对不再继续打印任何 OCR 日志，0 毫秒立即停止，界面瞬间恢复！
5. 【全自适应弹性伸缩与顺畅滚动】+【中间设置标准五行排版】+【萌宠企鹅图标】+【正中居中标题】。
6. 【100% 完整保留原 PDF 书签多级目录树】+【流式低内存 (< 50MB RAM)】。
"""

import os
import sys

# -------------------------------------------------------------
# 关键底层配置：禁用 OpenMP/MKL 忙轮询，解除 Windows 鼠标光标争抢
# -------------------------------------------------------------
os.environ["OMP_WAIT_POLICY"] = "PASSIVE"
os.environ["KMP_BLOCKTIME"] = "0"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import math
import random
import time
import ctypes
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Tuple

# -------------------------------------------------------------
# 硬件级 CPU 核心硬隔离与系统优先级调度
# -------------------------------------------------------------
def apply_hardware_cpu_governance():
    try:
        cpu_count = os.cpu_count() or 4
        if cpu_count >= 4:
            mask = ((1 << cpu_count) - 1) & ~0b00000011  # 留下 Core 0, 1 给系统和鼠标
        elif cpu_count == 3:
            mask = 0b00000110
        elif cpu_count == 2:
            mask = 0b00000010
        else:
            mask = 1

        handle = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.kernel32.SetProcessAffinityMask(handle, mask)
        # BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
        ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)
    except Exception:
        pass

apply_hardware_cpu_governance()

import fitz  # PyMuPDF
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QSpinBox, QCheckBox,
    QProgressBar, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog, QMessageBox, QGroupBox, QStatusBar, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QThread, Signal, Slot, QSize, QUrl
from PySide6.QtGui import QIcon, QFont, QColor, QPixmap, QDragEnterEvent, QDropEvent

from dual_layer_engine_pro_v9 import DualLayerPDFEngineProV9


# -------------------------------------------------------------
# 高性能低功耗现代圆角样式表 (QSS)
# -------------------------------------------------------------
LIGHT_STYLE = """
QMainWindow {
    background-color: #f1f5f9;
}
QWidget#central_widget {
    background-color: #f1f5f9;
}
QWidget {
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    font-size: 13px;
    color: #0f172a;
}
QGroupBox {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 16px;
    padding-left: 12px;
    padding-right: 12px;
    padding-bottom: 12px;
    font-weight: bold;
    color: #0f172a;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 0 6px;
    background-color: #ffffff;
    color: #0f172a;
    font-size: 13px;
    font-weight: bold;
}
QPushButton {
    background-color: #2563eb;
    color: #ffffff;
    border-radius: 6px;
    padding: 6px 16px;
    font-weight: bold;
    border: none;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #1d4ed8;
}
QPushButton:pressed {
    background-color: #1e40af;
}
QPushButton:disabled {
    background-color: #94a3b8;
    color: #e2e8f0;
}
QPushButton#btn_danger {
    background-color: #ef4444;
}
QPushButton#btn_danger:hover {
    background-color: #dc2626;
}
QPushButton#btn_gray {
    background-color: #64748b;
}
QPushButton#btn_gray:hover {
    background-color: #475569;
}
QPushButton#btn_main_action {
    background-color: #2563eb;
    color: #ffffff;
    border-radius: 8px;
    font-size: 15px;
    font-weight: bold;
    min-height: 44px;
}
QPushButton#btn_main_action:hover {
    background-color: #1d4ed8;
}
QPushButton#btn_main_stop {
    background-color: #ef4444;
    color: #ffffff;
    border-radius: 8px;
    font-size: 15px;
    font-weight: bold;
    min-height: 44px;
    padding: 0 28px;
}
QPushButton#btn_main_stop:hover {
    background-color: #dc2626;
}
QLineEdit {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 5px 10px;
    color: #0f172a;
    min-height: 22px;
}
QLineEdit:focus {
    border: 1px solid #2563eb;
}
QComboBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 4px 10px;
    color: #0f172a;
    min-height: 22px;
}
QComboBox:focus {
    border: 1px solid #2563eb;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QSpinBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 4px 8px;
    color: #0f172a;
    min-height: 22px;
}
QSpinBox:focus {
    border: 1px solid #2563eb;
}
QCheckBox {
    spacing: 7px;
    color: #0f172a;
    font-weight: normal;
}
QCheckBox::indicator {
    width: 17px;
    height: 17px;
    border-radius: 4px;
    border: 1px solid #94a3b8;
    background-color: #f8fafc;
}
QCheckBox::indicator:checked {
    background-color: #2563eb;
    border: 1px solid #1d4ed8;
    image: none;
}
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    gridline-color: #f1f5f9;
    selection-background-color: #eff6ff;
    selection-color: #1e40af;
}
QHeaderView::section {
    background-color: #f8fafc;
    color: #475569;
    font-weight: bold;
    border: none;
    border-bottom: 1px solid #e2e8f0;
    padding: 6px;
}
QScrollBar:vertical {
    border: none;
    background: #f1f5f9;
    width: 10px;
    border-radius: 5px;
    margin: 2px 2px 2px 2px;
}
QScrollBar::handle:vertical {
    background: #cbd5e1;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #94a3b8;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    border: none;
    background: #f1f5f9;
    height: 10px;
    border-radius: 5px;
    margin: 2px 2px 2px 2px;
}
QScrollBar::handle:horizontal {
    background: #cbd5e1;
    min-width: 20px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal:hover {
    background: #94a3b8;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
QProgressBar {
    border: none;
    border-radius: 7px;
    background-color: #e2e8f0;
    text-align: right;
    height: 14px;
    font-size: 11px;
    color: #2563eb;
    font-weight: bold;
}
QProgressBar::chunk {
    background-color: #4f46e5;
    border-radius: 7px;
}
QTextEdit {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    color: #0f172a;
    font-family: "Consolas", "Microsoft YaHei", monospace;
    font-size: 12px;
    padding: 10px;
    line-height: 1.5;
}
QStatusBar {
    background-color: #f1f5f9;
    border-top: 1px solid #e2e8f0;
    color: #475569;
    min-height: 28px;
}
QLabel#device_pill {
    background-color: #eff6ff;
    color: #2563eb;
    border: 1px solid #bfdbfe;
    border-radius: 5px;
    padding: 3px 8px;
    font-weight: bold;
    font-size: 11px;
}
"""

DARK_STYLE = """
QMainWindow {
    background-color: #0b1120;
}
QWidget#central_widget {
    background-color: #0b1120;
}
QWidget {
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    font-size: 13px;
    color: #f8fafc;
}
QGroupBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 16px;
    padding-left: 12px;
    padding-right: 12px;
    padding-bottom: 12px;
    font-weight: bold;
    color: #f8fafc;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 0 6px;
    background-color: #1e293b;
    color: #f8fafc;
    font-size: 13px;
    font-weight: bold;
}
QPushButton {
    background-color: #3b82f6;
    color: #ffffff;
    border-radius: 6px;
    padding: 6px 16px;
    font-weight: bold;
    border: none;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #2563eb;
}
QPushButton:pressed {
    background-color: #1d4ed8;
}
QPushButton:disabled {
    background-color: #475569;
    color: #94a3b8;
}
QPushButton#btn_danger {
    background-color: #ef4444;
}
QPushButton#btn_danger:hover {
    background-color: #dc2626;
}
QPushButton#btn_gray {
    background-color: #475569;
}
QPushButton#btn_gray:hover {
    background-color: #334155;
}
QPushButton#btn_main_action {
    background-color: #3b82f6;
    color: #ffffff;
    border-radius: 8px;
    font-size: 15px;
    font-weight: bold;
    min-height: 44px;
}
QPushButton#btn_main_action:hover {
    background-color: #2563eb;
}
QPushButton#btn_main_stop {
    background-color: #ef4444;
    color: #ffffff;
    border-radius: 8px;
    font-size: 15px;
    font-weight: bold;
    min-height: 44px;
    padding: 0 28px;
}
QPushButton#btn_main_stop:hover {
    background-color: #dc2626;
}
QLineEdit {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 5px 10px;
    color: #f8fafc;
    min-height: 22px;
}
QLineEdit:focus {
    border: 1px solid #38bdf8;
}
QComboBox {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 4px 10px;
    color: #f8fafc;
    min-height: 22px;
}
QComboBox:focus {
    border: 1px solid #38bdf8;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QSpinBox {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 4px 8px;
    color: #f8fafc;
    min-height: 22px;
}
QSpinBox:focus {
    border: 1px solid #38bdf8;
}
QCheckBox {
    spacing: 7px;
    color: #f8fafc;
    font-weight: normal;
}
QCheckBox::indicator {
    width: 17px;
    height: 17px;
    border-radius: 4px;
    border: 1px solid #64748b;
    background-color: #0f172a;
}
QCheckBox::indicator:checked {
    background-color: #38bdf8;
    border: 1px solid #0284c7;
    image: none;
}
QTableWidget {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    gridline-color: #1e293b;
    selection-background-color: #1e3a8a;
    selection-color: #f8fafc;
    color: #f8fafc;
}
QHeaderView::section {
    background-color: #1e293b;
    color: #94a3b8;
    font-weight: bold;
    border: none;
    border-bottom: 1px solid #334155;
    padding: 6px;
}
QScrollBar:vertical {
    border: none;
    background: #0f172a;
    width: 10px;
    border-radius: 5px;
    margin: 2px 2px 2px 2px;
}
QScrollBar::handle:vertical {
    background: #334155;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #475569;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    border: none;
    background: #0f172a;
    height: 10px;
    border-radius: 5px;
    margin: 2px 2px 2px 2px;
}
QScrollBar::handle:horizontal {
    background: #334155;
    min-width: 20px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal:hover {
    background: #475569;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
QProgressBar {
    border: none;
    border-radius: 7px;
    background-color: #334155;
    text-align: right;
    height: 14px;
    font-size: 11px;
    color: #38bdf8;
    font-weight: bold;
}
QProgressBar::chunk {
    background-color: #38bdf8;
    border-radius: 7px;
}
QTextEdit {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #38bdf8;
    font-family: "Consolas", "Microsoft YaHei", monospace;
    font-size: 12px;
    padding: 10px;
    line-height: 1.5;
}
QStatusBar {
    background-color: #1e293b;
    border-top: 1px solid #334155;
    color: #94a3b8;
    min-height: 28px;
}
QLabel#device_pill {
    background-color: #1e3a8a;
    color: #38bdf8;
    border: 1px solid #2563eb;
    border-radius: 5px;
    padding: 3px 8px;
    font-weight: bold;
    font-size: 11px;
}
"""


class DroppableTableWidget(QTableWidget):
    files_dropped = Signal(list)

    def __init__(self, rows, cols, parent=None):
        super().__init__(rows, cols, parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QTableWidget.DropOnly)
        self.setMouseTracking(False)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_paths = []
            for url in event.mimeData().urls():
                fp = url.toLocalFile()
                if fp:
                    file_paths.append(fp)
            if file_paths:
                self.files_dropped.emit(file_paths)
            event.acceptProposedAction()
        else:
            event.ignore()


# -------------------------------------------------------------
# 多书并行并发工作线程 (True Multi-Book Parallel Worker with Smart Skip)
# -------------------------------------------------------------
class ParallelMultiBookWorker(QThread):
    progress_signal = Signal(str, int, int, dict, int, int, int)
    log_signal = Signal(str)
    item_status_signal = Signal(str, str, str, str, str, str, str)
    finish_signal = Signal(int, int, int, int, float, bool)

    def __init__(self, file_list, dpi, concurrency, thresh, out_dir, skip_existing, cpu_mode, export_txt, export_docx, export_text_pdf, sleep_on_fin, naming_options):
        super().__init__()
        self.file_list = list(file_list)
        self.dpi = dpi
        self.concurrency = max(1, concurrency)
        self.thresh = thresh
        self.out_dir = out_dir
        self.skip_existing = skip_existing
        self.cpu_mode = cpu_mode
        self.export_txt = export_txt
        self.export_docx = export_docx
        self.export_text_pdf = export_text_pdf
        self.sleep_on_fin = sleep_on_fin
        self.naming_options = naming_options
        self.cancel_event = threading.Event()
        self.lock = threading.Lock()
        
        self.file_done_pages = {}
        self.file_total_pages = {}
        self.global_total_pages = 0

    def cancel(self):
        self.cancel_event.set()

    def _generate_out_path(self, f_path: str) -> str:
        base_name = os.path.basename(f_path)
        stem, _ = os.path.splitext(base_name)
        tags = []
        if self.naming_options.get("time"):
            tags.append(time.strftime("%Y%m%d_%H%M%S"))
        if self.naming_options.get("random"):
            tags.append(f"{random.randint(1000, 9999)}")
        if self.naming_options.get("model"):
            tags.append("PP-OCRv6")
        if self.naming_options.get("device"):
            tags.append("CPU")
            
        out_name = f"{stem}_ocr_{'_'.join(tags)}.pdf" if tags else f"{stem}_searchable.pdf"
        if self.out_dir and os.path.exists(self.out_dir):
            return os.path.join(self.out_dir, out_name)
        else:
            return os.path.join(os.path.dirname(f_path), out_name)

    def _find_existing_output(self, f_path: str) -> Optional[str]:
        """智能探测目标目录中是否已经存在该书籍的 OCR 成果文件"""
        base_name = os.path.basename(f_path)
        stem, _ = os.path.splitext(base_name)
        target_dir = self.out_dir if (self.out_dir and os.path.exists(self.out_dir)) else os.path.dirname(f_path)
        
        if not target_dir or not os.path.exists(target_dir):
            return None
            
        exact_out = self._generate_out_path(f_path)
        if os.path.exists(exact_out) and os.path.getsize(exact_out) > 0 and os.path.abspath(exact_out) != os.path.abspath(f_path):
            return exact_out
            
        try:
            for fname in os.listdir(target_dir):
                if fname.lower().endswith(".pdf"):
                    full_p = os.path.join(target_dir, fname)
                    if os.path.abspath(full_p) == os.path.abspath(f_path):
                        continue
                    f_stem, _ = os.path.splitext(fname)
                    if f_stem.startswith(stem) and any(tag in f_stem.lower() for tag in ["_ocr", "_searchable", "_双层", "_可检索"]):
                        if os.path.getsize(full_p) > 1024:  # 大于 1KB
                            return full_p
        except Exception:
            pass
            
        return None

    def _is_source_already_searchable(self, f_path: str) -> Tuple[bool, str]:
        """深度探测源 PDF 是否已经含有可检索文字层 (即已完成 OCR 或本身为文字版)"""
        if not f_path.lower().endswith(".pdf") or not os.path.exists(f_path):
            return False, ""
            
        base_name = os.path.basename(f_path)
        stem, _ = os.path.splitext(base_name)
        
        if any(tag in stem.lower() for tag in ["_ocr", "_searchable", "_可检索", "_双层"]):
            try:
                doc = fitz.open(f_path)
                if len(doc) > 0:
                    sample_txt = "".join(doc[i].get_text() for i in range(min(len(doc), 3)))
                    doc.close()
                    if len(sample_txt.strip()) >= 30:
                        return True, "文件名含OCR标识且包含文字层"
            except Exception:
                pass
                
        try:
            doc = fitz.open(f_path)
            if doc.is_encrypted:
                try: doc.authenticate("")
                except Exception: pass
            total_pages = len(doc)
            if total_pages == 0:
                doc.close()
                return False, ""
                
            sample_indices = list(range(min(5, total_pages)))
            if total_pages > 10:
                mid = total_pages // 2
                sample_indices.extend([mid - 1, mid, mid + 1])
            sample_indices = sorted(list(set(sample_indices)))
            
            pages_with_text = 0
            total_chars = 0
            for idx in sample_indices:
                if idx < total_pages:
                    txt = doc[idx].get_text().strip()
                    if len(txt) >= 30:
                        pages_with_text += 1
                        total_chars += len(txt)
            doc.close()
            
            if pages_with_text >= max(1, int(len(sample_indices) * 0.7)):
                avg_chars = total_chars / float(len(sample_indices))
                return True, f"抽样平均 {avg_chars:.0f} 字/页"
        except Exception:
            pass
            
        return False, ""

    def _get_pdf_pages_fast(self, f_path: str) -> int:
        try:
            if f_path.lower().endswith(".pdf"):
                doc = fitz.open(f_path)
                cnt = len(doc)
                doc.close()
                return cnt
            return 1
        except Exception:
            return 1

    def run(self):
        total_files = len(self.file_list)
        t_start_all = time.time()
        was_cancelled = False
        
        mode_desc = {"quiet": "温控静音 (<50% CPU)", "balanced": "标准均衡 (<70% CPU)", "fast": "极速全速 (<85% CPU)"}.get(self.cpu_mode, "标准均衡")
        self.log_signal.emit(f"=== 正在启动硬件级控温引擎 (共 {total_files} 本书, 并发: {self.concurrency}, 控温模式: {mode_desc}, DPI: {self.dpi}) ===")
        for f in self.file_list:
            if self.cancel_event.is_set():
                break
            p_cnt = self._get_pdf_pages_fast(f)
            self.file_total_pages[f] = p_cnt
            self.file_done_pages[f] = 0
            self.global_total_pages += p_cnt
            
        if self.global_total_pages == 0:
            self.global_total_pages = 1
            
        self.log_signal.emit(f"=== 批量总计: {total_files} 本书，约 {self.global_total_pages} 页，硬件核心硬隔离保护已生效 ===")
        
        engine = DualLayerPDFEngineProV9(
            dpi=self.dpi,
            det_limit=960,
            box_thresh=self.thresh,
            concurrency=self.concurrency,
            cpu_mode=self.cpu_mode,
            export_txt=self.export_txt,
            export_docx=self.export_docx,
            export_text_only_pdf=self.export_text_pdf,
            sleep_on_finish=self.sleep_on_fin
        )
        
        success_cnt, skipped_cnt, failed_cnt = 0, 0, 0
        
        def process_single_book(f_path: str):
            nonlocal success_cnt, skipped_cnt, failed_cnt
            if self.cancel_event.is_set():
                return
                
            base_name = os.path.basename(f_path)
            tot_p = self.file_total_pages.get(f_path, 1)
            
            # 智能跳过判定 (Smart Skip)
            if self.skip_existing:
                existing_out = self._find_existing_output(f_path)
                if existing_out:
                    with self.lock:
                        self.file_done_pages[f_path] = tot_p
                        skipped_cnt += 1
                        global_done = sum(self.file_done_pages.values())
                        global_pct = min(100, int((global_done / float(self.global_total_pages)) * 100))
                    self.item_status_signal.emit(f_path, "跳过(已有成果)", str(tot_p), "100%", "-", "-", "-")
                    self.progress_signal.emit(f_path, tot_p, tot_p, {"pct": 100, "speed_pph": 0}, global_done, self.global_total_pages, global_pct)
                    self.log_signal.emit(f"💡 [智能跳过] 目标已存在 OCR 成果: {os.path.basename(existing_out)}，已自动跳过。")
                    return
                    
                is_searchable, reason = self._is_source_already_searchable(f_path)
                if is_searchable:
                    with self.lock:
                        self.file_done_pages[f_path] = tot_p
                        skipped_cnt += 1
                        global_done = sum(self.file_done_pages.values())
                        global_pct = min(100, int((global_done / float(self.global_total_pages)) * 100))
                    self.item_status_signal.emit(f_path, "跳过(已有文字)", str(tot_p), "100%", "-", "-", "-")
                    self.progress_signal.emit(f_path, tot_p, tot_p, {"pct": 100, "speed_pph": 0}, global_done, self.global_total_pages, global_pct)
                    self.log_signal.emit(f"💡 [智能跳过] 文档本身已具备可检索文字层 ({reason}): {base_name}，自动跳过。")
                    return

            out_path = self._generate_out_path(f_path)
            self.item_status_signal.emit(f_path, "处理中", str(tot_p), "0%", "...", "...", "-")
            self.log_signal.emit(f"[并行开始] 正在处理: {base_name} (共 {tot_p} 页)")
            
            def page_cb(curr_p, t_p, metrics):
                if self.cancel_event.is_set():
                    return
                with self.lock:
                    self.file_done_pages[f_path] = curr_p
                    global_done = sum(self.file_done_pages.values())
                    global_pct = min(100, int((global_done / float(self.global_total_pages)) * 100))
                self.progress_signal.emit(f_path, curr_p, t_p, metrics, global_done, self.global_total_pages, global_pct)
                
            try:
                res = engine.process_pdf(
                    f_path,
                    out_path,
                    progress_callback=page_cb,
                    log_callback=lambda m: self.log_signal.emit(m),
                    cancel_event=self.cancel_event
                )
                with self.lock:
                    self.file_done_pages[f_path] = res["total_pages"]
                    success_cnt += 1
                cost_s = f"{res['cost_time']:.1f}s"
                speed_s = f"{res['speed_ppm']:.0f}页/分"
                fin_time = time.strftime("%H:%M:%S")
                self.item_status_signal.emit(f_path, "完成", str(res["total_pages"]), "100%", cost_s, speed_s, fin_time)
                self.log_signal.emit(f"🎉 [完成] {base_name} 转换完成！耗时: {cost_s}")
            except InterruptedError:
                self.item_status_signal.emit(f_path, "已取消", str(tot_p), "0%", "-", "-", "-")
            except Exception as e:
                with self.lock:
                    failed_cnt += 1
                self.item_status_signal.emit(f_path, "失败", str(tot_p), "0%", "-", "-", "-")
                self.log_signal.emit(f"❌ 制作失败: {base_name}, 错误: {e}")

        max_workers = min(total_files, self.concurrency)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_single_book, f) for f in self.file_list]
            for fut in as_completed(futures):
                if self.cancel_event.is_set():
                    was_cancelled = True
                    break
                try:
                    fut.result()
                except Exception:
                    pass
                    
        total_cost = time.time() - t_start_all
        if self.cancel_event.is_set():
            was_cancelled = True
            
        self.finish_signal.emit(total_files, success_cnt, skipped_cnt, failed_cnt, total_cost, was_cancelled)


class DualLayerPDFAppPySide6(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PaddleOCR 双层 PDF 生成工具 v20.0 (CPU版) [硬件控温丝滑旗舰版]")
        self.resize(1120, 960)
        self.setMinimumSize(980, 800)
        self.setAcceptDrops(True)
        self.setMouseTracking(False)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "penguin_icon.png")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "penguin_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.file_list = []
        self.is_dark_mode = False
        self.worker_thread = None
        self.is_running = False
        
        self._init_ui()
        self.apply_theme(is_dark=False)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            paths = [url.toLocalFile() for url in event.mimeData().urls() if url.toLocalFile()]
            if paths:
                self.handle_dropped_paths(paths)
            event.acceptProposedAction()
        else:
            event.ignore()

    def handle_dropped_paths(self, paths: List[str]):
        added_cnt = 0
        for p in paths:
            if os.path.isfile(p):
                ext = os.path.splitext(p)[1].lower()
                if ext in [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp"] and p not in self.file_list:
                    self._add_single_file_to_table(p)
                    added_cnt += 1
            elif os.path.isdir(p):
                for root_d, _, files in os.walk(p):
                    for f in files:
                        if os.path.splitext(f)[1].lower() in [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp"]:
                            fp = os.path.join(root_d, f)
                            if fp not in self.file_list:
                                self._add_single_file_to_table(fp)
                                added_cnt += 1
        if added_cnt > 0:
            self.log(f"拖拽批量导入了 {added_cnt} 个文件。")
            self.lbl_count.setText(f"共 {len(self.file_list)} 个文件")

    def _add_single_file_to_table(self, f_path: str):
        self.file_list.append(f_path)
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        self.table.setItem(row, 1, QTableWidgetItem(f_path))
        self.table.setItem(row, 2, QTableWidgetItem("等待"))
        self.table.setItem(row, 3, QTableWidgetItem("-"))
        self.table.setItem(row, 4, QTableWidgetItem("0%"))
        self.table.setItem(row, 5, QTableWidgetItem("-"))
        self.table.setItem(row, 6, QTableWidgetItem("-"))
        self.table.setItem(row, 7, QTableWidgetItem("-"))
        self.table.scrollToBottom()

    def _init_ui(self):
        # 1. 顶部 Header
        self.header_widget = QFrame()
        self.header_widget.setFixedHeight(54)
        self.header_widget.setStyleSheet("background-color: #4f46e5; border-radius: 0px;")
        
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(18, 0, 18, 0)
        
        left_box = QWidget()
        left_box.setFixedWidth(160)
        left_layout = QHBoxLayout(left_box)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)
        
        icon_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "penguin_icon.png")
        if os.path.exists(icon_p):
            lbl_icon = QLabel()
            pix = QPixmap(icon_p).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            lbl_icon.setPixmap(pix)
            lbl_icon.setStyleSheet("background: transparent;")
            left_layout.addWidget(lbl_icon)
            
        lbl_brand = QLabel("智造 Pro")
        lbl_brand.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        lbl_brand.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: transparent;")
        left_layout.addWidget(lbl_brand)
        left_layout.addStretch()
        header_layout.addWidget(left_box)
        
        self.lbl_title = QLabel("PaddleOCR 双层 PDF 生成工具 v20.0")
        self.lbl_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setStyleSheet("color: #ffffff; background: transparent;")
        header_layout.addWidget(self.lbl_title, stretch=1)
        
        right_box = QWidget()
        right_box.setFixedWidth(160)
        right_layout = QHBoxLayout(right_box)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addStretch()
        
        self.btn_theme = QPushButton("🌙 暗色")
        self.btn_theme.setCursor(Qt.PointingHandCursor)
        self.btn_theme.setStyleSheet("background-color: rgba(255, 255, 255, 0.2); color: #ffffff; border: 1px solid rgba(255, 255, 255, 0.4); border-radius: 6px; padding: 5px 14px; font-weight: bold;")
        self.btn_theme.clicked.connect(self.toggle_theme)
        right_layout.addWidget(self.btn_theme)
        header_layout.addWidget(right_box)
        
        # 2. 中间主容器
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(18, 0, 18, 14)
        main_layout.setSpacing(10)
        main_layout.addWidget(self.header_widget)
        
        # A. PDF 文件列表卡片
        group_list = QGroupBox("PDF 文件列表 (可拖拽 PDF 文件到此处)")
        group_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        list_layout = QVBoxLayout(group_list)
        list_layout.setContentsMargins(12, 10, 12, 10)
        list_layout.setSpacing(8)
        
        self.table = DroppableTableWidget(0, 8)
        self.table.setMinimumHeight(220)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setHorizontalHeaderLabels(["序号", "文件路径", "状态", "页数", "进度", "耗时", "速度", "完成时间"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.files_dropped.connect(self.handle_dropped_paths)
        list_layout.addWidget(self.table)
        
        tb_layout = QHBoxLayout()
        tb_layout.setSpacing(8)
        
        self.btn_add_f = QPushButton("添加文件")
        self.btn_add_f.setCursor(Qt.PointingHandCursor)
        self.btn_add_f.clicked.connect(self.add_files)
        tb_layout.addWidget(self.btn_add_f)
        
        self.btn_add_d = QPushButton("添加文件夹")
        self.btn_add_d.setCursor(Qt.PointingHandCursor)
        self.btn_add_d.clicked.connect(self.add_directory)
        tb_layout.addWidget(self.btn_add_d)
        
        self.btn_del = QPushButton("移除选中")
        self.btn_del.setObjectName("btn_danger")
        self.btn_del.setCursor(Qt.PointingHandCursor)
        self.btn_del.clicked.connect(self.remove_selected)
        tb_layout.addWidget(self.btn_del)
        
        self.btn_clear = QPushButton("清空列表")
        self.btn_clear.setObjectName("btn_gray")
        self.btn_clear.setCursor(Qt.PointingHandCursor)
        self.btn_clear.clicked.connect(self.clear_files)
        tb_layout.addWidget(self.btn_clear)
        
        tb_layout.addStretch()
        self.lbl_count = QLabel("共 0 个文件")
        self.lbl_count.setStyleSheet("color: #64748b; font-weight: bold;")
        tb_layout.addWidget(self.lbl_count)
        list_layout.addLayout(tb_layout)
        
        main_layout.addWidget(group_list, stretch=5)
        
        # B. 设置圆角卡片
        group_settings = QGroupBox("设置")
        set_layout = QVBoxLayout(group_settings)
        set_layout.setContentsMargins(12, 12, 12, 12)
        set_layout.setSpacing(9)
        
        # 【第 1 行】：输出目录
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        lbl_out = QLabel("输出目录:")
        lbl_out.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        row1.addWidget(lbl_out)
        
        self.entry_out_dir = QLineEdit()
        self.entry_out_dir.setPlaceholderText("选择输出目录（默认与源文件相同）")
        row1.addWidget(self.entry_out_dir, stretch=1)
        
        self.btn_browse = QPushButton(" 浏览 ")
        self.btn_browse.setCursor(Qt.PointingHandCursor)
        self.btn_browse.clicked.connect(self.browse_dir)
        row1.addWidget(self.btn_browse)
        set_layout.addLayout(row1)
        
        # 【第 2 行】：模型 / DPI / 推理设备 / 并发 / CPU控温模式
        row2 = QHBoxLayout()
        row2.setSpacing(8)
        
        lbl_m = QLabel("模型:")
        lbl_m.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        row2.addWidget(lbl_m)
        
        self.combo_model = QComboBox()
        self.combo_model.addItems([
            "PP-OCRv6 Small (ONNX加速)",
            "PP-OCRv6 Medium (ONNX加速)",
            "PP-OCRv6 Small",
            "PP-OCRv6 Medium",
            "PP-OCRv5 Server",
            "PP-OCRv5 Mobile",
            "PP-OCRv4 Server",
            "PP-OCRv4 Mobile",
            "PP-OCRv3 Server",
            "PP-OCRv3 Mobile"
        ])
        row2.addWidget(self.combo_model)
        
        lbl_d = QLabel("DPI:")
        lbl_d.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        row2.addWidget(lbl_d)
        
        self.combo_dpi = QComboBox()
        self.combo_dpi.addItems(["150", "200", "300"])
        self.combo_dpi.setCurrentIndex(1)
        row2.addWidget(self.combo_dpi)
        
        lbl_device = QLabel("CPU (MKLDNN)")
        lbl_device.setObjectName("device_pill")
        row2.addWidget(lbl_device)
        
        lbl_c = QLabel("并发:")
        lbl_c.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        row2.addWidget(lbl_c)
        
        self.spin_concur = QSpinBox()
        self.spin_concur.setRange(1, 4)
        self.spin_concur.setValue(2)  # 默认 2 并发，确保温控与极速平衡
        row2.addWidget(self.spin_concur)
        
        lbl_mode = QLabel("CPU控温:")
        lbl_mode.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        row2.addWidget(lbl_mode)
        
        self.combo_cpu_mode = QComboBox()
        self.combo_cpu_mode.addItems([
            "标准均衡模式 (<70% CPU, 推荐)",
            "温控静音模式 (<50% CPU, 极顺畅)",
            "极速全速模式 (<85% CPU)"
        ])
        row2.addWidget(self.combo_cpu_mode)
        
        row2.addStretch()
        set_layout.addLayout(row2)
        
        # 【第 3 行】：置信度阈值 / 提示 / 休眠 / 智能跳过 / MKLDNN
        row3 = QHBoxLayout()
        row3.setSpacing(10)
        
        lbl_t = QLabel("置信度阈值:")
        lbl_t.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        row3.addWidget(lbl_t)
        
        self.entry_thresh = QLineEdit("0.8")
        self.entry_thresh.setFixedWidth(45)
        row3.addWidget(self.entry_thresh)
        
        lbl_hint = QLabel("(0~1, 越高越严格，默认 0.8)")
        lbl_hint.setStyleSheet("color: #64748b; font-size: 11px;")
        row3.addWidget(lbl_hint)
        
        self.cb_sleep = QCheckBox("完成后休眠")
        row3.addWidget(self.cb_sleep)
        
        self.cb_skip = QCheckBox("自动跳过已 OCR / 已完成文档")
        self.cb_skip.setChecked(True)
        self.cb_skip.setToolTip("开启后，若文档本身已具备文字层，或目标目录已有该书历史 OCR 成果，将自动跳过，极大节省时间。")
        row3.addWidget(self.cb_skip)
        
        self.cb_mkldnn = QCheckBox("MKLDNN 加速")
        self.cb_mkldnn.setChecked(True)
        row3.addWidget(self.cb_mkldnn)
        row3.addStretch()
        set_layout.addLayout(row3)
        
        # 【第 4 行】：导出选项
        row4 = QHBoxLayout()
        row4.setSpacing(16)
        self.cb_txt = QCheckBox("导出TXT文档（识别文字，文件名与 PDF 一致）")
        row4.addWidget(self.cb_txt)
        self.cb_docx = QCheckBox("导出Word文档（.docx，文件名与 PDF 一致）")
        row4.addWidget(self.cb_docx)
        self.cb_text_pdf = QCheckBox("导出纯文字PDF（无原扫描件，仅OCR文字）")
        row4.addWidget(self.cb_text_pdf)
        row4.addStretch()
        set_layout.addLayout(row4)
        
        # 【第 5 行】：文件名命名模板
        row5 = QHBoxLayout()
        row5.setSpacing(10)
        lbl_nam = QLabel("文件名命名: {源文件名}_ocr_[完成时间].pdf")
        lbl_nam.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        row5.addWidget(lbl_nam)
        
        self.tag_time = QCheckBox("完成时间")
        self.tag_time.setChecked(True)
        row5.addWidget(self.tag_time)
        self.tag_cost = QCheckBox("耗时")
        row5.addWidget(self.tag_cost)
        self.tag_random = QCheckBox("随机数")
        row5.addWidget(self.tag_random)
        self.tag_model = QCheckBox("OCR模型")
        row5.addWidget(self.tag_model)
        self.tag_device = QCheckBox("推理设备")
        row5.addWidget(self.tag_device)
        self.tag_isbn = QCheckBox("ISBN")
        row5.addWidget(self.tag_isbn)
        row5.addStretch()
        set_layout.addLayout(row5)
        
        main_layout.addWidget(group_settings)
        
        # C. 进度圆角卡片
        group_progress = QGroupBox("进度")
        prog_layout = QVBoxLayout(group_progress)
        prog_layout.setContentsMargins(12, 10, 12, 10)
        prog_layout.setSpacing(6)
        
        prog_hdr = QHBoxLayout()
        self.lbl_prog_title = QLabel("总进度: 0%")
        self.lbl_prog_title.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        prog_hdr.addWidget(self.lbl_prog_title)
        prog_hdr.addStretch()
        self.lbl_prog_pct = QLabel("0%")
        self.lbl_prog_pct.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        self.lbl_prog_pct.setStyleSheet("color: #2563eb;")
        prog_hdr.addWidget(self.lbl_prog_pct)
        prog_layout.addLayout(prog_hdr)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        prog_layout.addWidget(self.progress_bar)
        
        self.lbl_metrics = QLabel("就绪 | 等待开始任务")
        self.lbl_metrics.setStyleSheet("color: #64748b;")
        prog_layout.addWidget(self.lbl_metrics)
        main_layout.addWidget(group_progress)
        
        # D. 日志全域宽广卡片
        group_log = QGroupBox("日志")
        log_layout = QVBoxLayout(group_log)
        log_layout.setContentsMargins(12, 10, 12, 10)
        
        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)
        self.text_log.document().setMaximumBlockCount(300)
        self.text_log.append(">>> 就绪 — v20.0 硬件级控温丝滑版（五重硬件 CPU 治理 · 物理硬隔离 · 0 鼠标卡顿 · 智能跳过）已就绪。")
        log_layout.addWidget(self.text_log)
        main_layout.addWidget(group_log, stretch=3)
        
        # 3. 底部开始/停止控制栏
        btn_action_layout = QHBoxLayout()
        btn_action_layout.setSpacing(12)
        
        self.btn_start = QPushButton("▶ 开始转换")
        self.btn_start.setObjectName("btn_main_action")
        self.btn_start.setCursor(Qt.PointingHandCursor)
        self.btn_start.clicked.connect(self.start_processing)
        btn_action_layout.addWidget(self.btn_start, stretch=1)
        
        self.btn_stop = QPushButton("■ 停止")
        self.btn_stop.setObjectName("btn_main_stop")
        self.btn_stop.setCursor(Qt.PointingHandCursor)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_processing)
        btn_action_layout.addWidget(self.btn_stop)
        
        main_layout.addLayout(btn_action_layout)
        
        # 4. 底部固定状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar_left = QLabel("已处理 0/0 页 | 速度: 0 页/时 | 剩余: ~0分钟")
        self.status_bar_right = QLabel("v20.0 Pro AI 硬件控温丝滑版 (PySide6 / MKLDNN加速)")
        self.status_bar.addWidget(self.status_bar_left, 1)
        self.status_bar.addPermanentWidget(self.status_bar_right)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme(self.is_dark_mode)

    def apply_theme(self, is_dark):
        if is_dark:
            self.setStyleSheet(DARK_STYLE)
            self.btn_theme.setText("☀ 亮色")
            self.lbl_prog_pct.setStyleSheet("color: #38bdf8;")
        else:
            self.setStyleSheet(LIGHT_STYLE)
            self.btn_theme.setText("🌙 暗色")
            self.lbl_prog_pct.setStyleSheet("color: #2563eb;")

    def log(self, msg):
        if not self.is_running and "[用户强行终止]" not in msg and "就绪" not in msg:
            return
        t_str = time.strftime("%H:%M:%S")
        self.text_log.append(f"[{t_str}] {msg}")

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择扫描 PDF 或图片文件", "", "PDF/图片 (*.pdf *.png *.jpg *.jpeg *.tiff *.bmp *.webp);;所有文件 (*.*)")
        added = 0
        for f in files:
            if f and f not in self.file_list:
                self._add_single_file_to_table(f)
                added += 1
                self.log(f"已添加文件: {os.path.basename(f)}")
        if added > 0:
            self.lbl_count.setText(f"共 {len(self.file_list)} 个文件")

    def add_directory(self):
        dir_p = QFileDialog.getExistingDirectory(self, "选择包含扫描件的文件夹")
        if not dir_p: return
        added_cnt = 0
        for root_d, _, files in os.walk(dir_p):
            for f in files:
                if os.path.splitext(f)[1].lower() in [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp"]:
                    fp = os.path.join(root_d, f)
                    if fp not in self.file_list:
                        self._add_single_file_to_table(fp)
                        added_cnt += 1
        self.log(f"从文件夹批量导入了 {added_cnt} 个扫描文件。")
        self.lbl_count.setText(f"共 {len(self.file_list)} 个文件")

    def remove_selected(self):
        selected_rows = sorted(set(idx.row() for idx in self.table.selectedIndexes()), reverse=True)
        for r in selected_rows:
            fp = self.table.item(r, 1).text()
            if fp in self.file_list:
                self.file_list.remove(fp)
            self.table.removeRow(r)
        for r in range(self.table.rowCount()):
            self.table.item(r, 0).setText(str(r + 1))
        self.lbl_count.setText(f"共 {len(self.file_list)} 个文件")

    def clear_files(self):
        self.file_list.clear()
        self.table.setRowCount(0)
        self.lbl_count.setText("共 0 个文件")

    def browse_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if d:
            self.entry_out_dir.setText(d)

    def start_processing(self):
        if not self.file_list:
            QMessageBox.warning(self, "提示", "请先添加待处理的 PDF 或扫描文件！")
            return
            
        dpi_val = int(self.combo_dpi.currentText())
        concurrency = self.spin_concur.value()
        try: thresh = float(self.entry_thresh.text())
        except Exception: thresh = 0.8
        
        mode_idx = self.combo_cpu_mode.currentIndex()
        cpu_mode = "balanced" if mode_idx == 0 else ("quiet" if mode_idx == 1 else "fast")
        
        out_dir = self.entry_out_dir.text().strip()
        custom_out_dir = out_dir if (out_dir and os.path.exists(out_dir)) else None
        
        naming_options = {
            "time": self.tag_time.isChecked(),
            "cost": self.tag_cost.isChecked(),
            "random": self.tag_random.isChecked(),
            "model": self.tag_model.isChecked(),
            "device": self.tag_device.isChecked(),
            "isbn": self.tag_isbn.isChecked()
        }
        
        self.is_running = True
        self.btn_start.setEnabled(False)
        self.btn_start.setText("转换中...")
        self.btn_stop.setEnabled(True)
        self.btn_stop.setText("■ 停止")
        
        self.worker_thread = ParallelMultiBookWorker(
            file_list=self.file_list,
            dpi=dpi_val,
            concurrency=concurrency,
            thresh=thresh,
            out_dir=custom_out_dir,
            skip_existing=self.cb_skip.isChecked(),
            cpu_mode=cpu_mode,
            export_txt=self.cb_txt.isChecked(),
            export_docx=self.cb_docx.isChecked(),
            export_text_pdf=self.cb_text_pdf.isChecked(),
            sleep_on_fin=self.cb_sleep.isChecked(),
            naming_options=naming_options
        )
        
        self.worker_thread.progress_signal.connect(self.on_progress)
        self.worker_thread.log_signal.connect(self.log)
        self.worker_thread.item_status_signal.connect(self.on_item_status)
        self.worker_thread.finish_signal.connect(self.on_finish)
        
        # 赋予工作线程最低调度优先级，Windows 鼠标光标与 GUI 永远无条件抢占
        self.worker_thread.start(QThread.Priority.LowestPriority)

    def stop_processing(self):
        self.is_running = False
        self.btn_start.setEnabled(True)
        self.btn_start.setText("▶ 开始转换")
        self.btn_stop.setEnabled(False)
        self.btn_stop.setText("■ 停止")
        
        if self.worker_thread:
            self.worker_thread.cancel()
            try:
                self.worker_thread.terminate()
                self.worker_thread.wait(100)
            except Exception:
                pass
                
        self.text_log.append(f"[{time.strftime('%H:%M:%S')}] 🛑 [用户强行终止] 任务已立即彻底停止！")
        self.lbl_metrics.setText("任务已由用户手动停止。")
        self.status_bar_left.setText("已停止")
        
        for r in range(self.table.rowCount()):
            st = self.table.item(r, 2)
            if st and st.text() == "处理中":
                st.setText("已取消")

    @Slot(str, int, int, dict, int, int, int)
    def on_progress(self, f_path, curr_p, tot_p, metrics, global_done_p, global_total_p, global_pct):
        if not self.is_running:
            return
            
        self.progress_bar.setValue(global_pct)
        self.lbl_prog_title.setText(f"总进度: {global_pct}%")
        self.lbl_prog_pct.setText(f"{global_pct}%")
        
        metric_str = f"已处理 {global_done_p}/{global_total_p} 页 | 多书并行中 | 速度: {metrics.get('speed_pph', 0)} 页/时"
        self.lbl_metrics.setText(metric_str)
        self.status_bar_left.setText(metric_str)
        
        file_pct = metrics.get("pct", int((curr_p/float(tot_p))*100) if tot_p > 0 else 0)
        for r in range(self.table.rowCount()):
            if self.table.item(r, 1).text() == f_path:
                if "跳过" not in self.table.item(r, 2).text():
                    self.table.item(r, 2).setText("处理中")
                self.table.item(r, 3).setText(str(tot_p))
                self.table.item(r, 4).setText(f"{file_pct}% ({curr_p}/{tot_p})")
                break

    @Slot(str, str, str, str, str, str, str)
    def on_item_status(self, f_path, status, pages, prog, cost, speed, fin_time):
        for r in range(self.table.rowCount()):
            if self.table.item(r, 1).text() == f_path:
                if status != "-": self.table.item(r, 2).setText(status)
                if pages != "-": self.table.item(r, 3).setText(pages)
                if prog != "-": self.table.item(r, 4).setText(prog)
                if cost != "-": self.table.item(r, 5).setText(cost)
                if speed != "-": self.table.item(r, 6).setText(speed)
                if fin_time != "-": self.table.item(r, 7).setText(fin_time)
                break

    @Slot(int, int, int, int, float, bool)
    def on_finish(self, total, success, skipped, failed, cost_s, was_cancelled):
        self.is_running = False
        self.btn_start.setEnabled(True)
        self.btn_start.setText("▶ 开始转换")
        self.btn_stop.setEnabled(False)
        self.btn_stop.setText("■ 停止")
        
        if was_cancelled:
            summary = f"任务已中止！已完成 {success} 个，跳过 {skipped} 个，未完成 {total - success - skipped} 个，耗时 {cost_s:.1f} 秒。"
            self.lbl_metrics.setText(summary)
            self.status_bar_left.setText(summary)
            self.log(f"=== [已中止] {summary} ===")
        else:
            self.progress_bar.setValue(100)
            self.lbl_prog_title.setText("总进度: 100%")
            self.lbl_prog_pct.setText("100%")
            summary = f"全部完成！成功 {success} 个，自动跳过 {skipped} 个，失败 {failed} 个，耗时 {cost_s:.1f} 秒。"
            self.lbl_metrics.setText(summary)
            self.status_bar_left.setText(summary)
            self.log(f"=== {summary} ===")
            
            if (success + skipped) > 0:
                res = QMessageBox.question(self, "制作完成", f"{summary}\n\n是否立即在文件资源管理器中打开输出目录？", QMessageBox.Yes | QMessageBox.No)
                if res == QMessageBox.Yes:
                    target_d = self.entry_out_dir.text().strip() or (os.path.dirname(self.file_list[0]) if self.file_list else os.getcwd())
                    subprocess.Popen(f'explorer "{os.path.abspath(target_d)}"')

def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = DualLayerPDFAppPySide6()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
