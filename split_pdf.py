import os
import fitz  # PyMuPDF

def split_chapters(input_pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(input_pdf_path)
    toc = doc.get_toc()

    # Find all chapter bookmarks
    # In this specific PDF, chapters are level 1 bookmarks containing "第一章", "第二章" or they correspond to exactly 16 chapters
    # We saw in the earlier run that the 16 chapters start at certain indices.
    # Let's filter Level 1 bookmarks that contain "章"
    chapters = []
    for item in toc:
        level = item[0]
        title = item[1]
        page = item[2]
        if level == 1 and "章" in title:
            chapters.append({"title": title, "page": page})

    if not chapters:
        print("未找到章节目录，请检查大纲结构。")
        return

    # In the earlier output we saw exactly 16 level 1 chapters like "第一章", "第二章"... "第十六章".
    # Sometimes TOC page numbers are 1-based, PyMuPDF expects 0-based for processing.
    # The `page` in get_toc() is usually 1-based.
    
    total_pages = len(doc)
    
    for i, chapter in enumerate(chapters):
        if i >= 16:
            break
            
        start_page = chapter["page"] - 1 # 0-based
        
        # Calculate end page
        if i < len(chapters) - 1:
            end_page = chapters[i+1]["page"] - 2 # up to the page before next chapter
        else:
            # For the last chapter, we don't know exactly where the appendix starts unless we check TOC again,
            # but let's just go up to the end of the document or the next level 1 item.
            # Find the next level 1 item in the original TOC
            next_page = total_pages
            found_current = False
            for item in toc:
                if item[0] == 1 and item[1] == chapter["title"]:
                    found_current = True
                elif found_current and item[0] == 1:
                    next_page = item[2] - 1
                    break
            
            end_page = next_page - 1
            if end_page >= total_pages:
                end_page = total_pages - 1

        # Format output filename
        ch_num = f"{(i+1):02d}"
        output_filename = f"产业经济学CH{ch_num}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"Splitting Chapter {i+1}: {chapter['title']} (Pages {start_page+1} to {end_page+1}) -> {output_filename}")
        
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page)
        new_doc.save(output_path)
        new_doc.close()

    doc.close()
    print("All chapters successfully split!")

if __name__ == "__main__":
    input_pdf = r"I:\4产业经济学\产业经济学 第3版_刘志彪.pdf"
    output_directory = r"I:\4产业经济学\章节拆分"
    split_chapters(input_pdf, output_directory)
