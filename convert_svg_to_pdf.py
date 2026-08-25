import re
import os
import sys
import pymupdf

sys.stdout.reconfigure(encoding='utf-8')

def markmap_svg_to_native_svg(svg_content):
    # Pattern to find foreignObject and extract coordinates and text
    def replace_fo(match):
        attrs = match.group(1)
        body = match.group(2)
        
        x_match = re.search(r'x="([^"]*)"', attrs)
        y_match = re.search(r'y="([^"]*)"', attrs)
        
        x = float(x_match.group(1)) if x_match else 8.0
        y = float(y_match.group(1)) if y_match else 0.0
        
        # clean text
        text = re.sub(r'<[^>]+>', '', body).strip()
        text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        
        # xml escape
        text_escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        y_pos = y + 15.0
        return f'<text x="{x}" y="{y_pos}" font-family="Microsoft YaHei, SimSun, sans-serif" font-size="13px" fill="#1e293b" font-weight="500">{text_escaped}</text>'

    pattern = r'<foreignObject([^>]*)>(.*?)</foreignObject>'
    native_svg = re.sub(pattern, replace_fo, svg_content, flags=re.DOTALL)
    
    # Ensure background white so it's not black/transparent in PDF
    if '<rect width="100%" height="100%"' not in native_svg:
        native_svg = re.sub(r'(<svg[^>]*>)', r'\1<rect width="100%" height="100%" fill="#ffffff"/>', native_svg, count=1)
        
    return native_svg

def convert_all_svgs():
    src_dir = r"I:\4产业经济学\2026产业经济学课件\思维导图\新建文件夹"
    
    svg_files = [f for f in os.listdir(src_dir) if f.lower().endswith('.svg') and f.upper().startswith('CH ')]
    svg_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))
    
    print(f"Found {len(svg_files)} SVG files to convert:")
    
    merged_pdf = pymupdf.open()
    
    for f in svg_files:
        svg_path = os.path.join(src_dir, f)
        base_name = os.path.splitext(f)[0]
        single_pdf_path = os.path.join(src_dir, f"{base_name}.pdf")
        
        with open(svg_path, 'r', encoding='utf-8') as sf:
            svg_data = sf.read()
            
        native_svg = markmap_svg_to_native_svg(svg_data)
        
        # Convert to single PDF
        svg_doc = pymupdf.open(stream=native_svg.encode('utf-8'), filetype='svg')
        pdf_bytes = svg_doc.convert_to_pdf()
        
        # Save individual PDF
        with open(single_pdf_path, 'wb') as out_f:
            out_f.write(pdf_bytes)
            
        # Append to merged PDF
        single_doc = pymupdf.open("pdf", pdf_bytes)
        merged_pdf.insert_pdf(single_doc)
        
        page = single_doc[0]
        text_len = len(page.get_text())
        print(f"  [Converted] {f:12s} -> {base_name + '.pdf':12s} (Page size: {page.rect.width:.0f}x{page.rect.height:.0f}, Text len: {text_len})")

    # Save merged PDF
    merged_pdf_path = os.path.join(src_dir, "2026产业经济学_思维导图全集_CH01-CH10.pdf")
    merged_pdf.save(merged_pdf_path)
    print(f"\n[Merged PDF Created] {merged_pdf_path} (Total Pages: {len(merged_pdf)})")

if __name__ == "__main__":
    convert_all_svgs()
