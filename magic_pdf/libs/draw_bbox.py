from magic_pdf.libs.commons import fitz  # PyMuPDF
from magic_pdf.libs.ocr_content_type import ContentType


def draw_bbox_without_number(i, bbox_list, page, rgb_config):
    new_rgb = []
    for item in rgb_config:
        item = float(item) / 255
        new_rgb.append(item)
    page_data = bbox_list[i]
    for bbox in page_data:
        x0, y0, x1, y1 = bbox
        rect_coords = fitz.Rect(x0, y0, x1, y1)  # Define the rectangle
        page.draw_rect(rect_coords, color=new_rgb, fill=None, width=0.5, overlay=True)  # Draw the rectangle


def draw_bbox_with_number(i, bbox_list, page, rgb_config):
    new_rgb = []
    for item in rgb_config:
        item = float(item) / 255
        new_rgb.append(item)
    page_data = bbox_list[i]
    for j, bbox in enumerate(page_data):
        x0, y0, x1, y1 = bbox
        rect_coords = fitz.Rect(x0, y0, x1, y1)  # Define the rectangle
        page.draw_rect(rect_coords, color=new_rgb, fill=None, width=0.5, overlay=True)  # Draw the rectangle
        page.insert_text((x0, y0), str(j + 1), fontsize=10, color=new_rgb)  # Insert the index at the top left corner of the rectangle


def draw_layout_bbox(pdf_info_dict, pdf_bytes, out_path):
    layout_bbox_list = []
    dropped_bbox_list = []
    for page in pdf_info_dict.values():
        page_layout_list = []
        page_dropped_list = []
        for layout in page['layout_bboxes']:
            page_layout_list.append(layout['layout_bbox'])
        layout_bbox_list.append(page_layout_list)
        for drop_tag, dropped_bboxes in page['droped_bboxes'].items():
            for dropped_bbox in dropped_bboxes:
                page_dropped_list.append(dropped_bbox)
        dropped_bbox_list.append(page_dropped_list)
    pdf_docs = fitz.open("pdf", pdf_bytes)
    for i, page in enumerate(pdf_docs):
        draw_bbox_with_number(i, layout_bbox_list, page, [255, 0, 0])
        draw_bbox_without_number(i, dropped_bbox_list, page, [0, 255, 0])
    # Save the PDF
    pdf_docs.save(f"{out_path}/layout.pdf")

def draw_text_bbox(pdf_info_dict, pdf_bytes, out_path):
    text_list = []
    inline_equation_list = []
    interline_equation_list = []
    for page in pdf_info_dict.values():
        page_text_list = []
        page_inline_equation_list = []
        page_interline_equation_list = []
        for block in page['preproc_blocks']:
            for line in block['lines']:
                for span in line['spans']:
                    if span['type'] == ContentType.Text:
                        page_text_list.append(span['bbox'])
                    elif span['type'] == ContentType.InlineEquation:
                        page_inline_equation_list.append(span['bbox'])
                    elif span['type'] == ContentType.InterlineEquation:
                        page_interline_equation_list.append(span['bbox'])
        text_list.append(page_text_list)
        inline_equation_list.append(page_inline_equation_list)
        interline_equation_list.append(page_interline_equation_list)
    pdf_docs = fitz.open("pdf", pdf_bytes)
    for i, page in enumerate(pdf_docs):
        # 获取当前页面的数据
        draw_bbox_without_number(i, text_list, page, [255, 0, 0])
        draw_bbox_without_number(i, inline_equation_list, page, [0, 255, 0])
        draw_bbox_without_number(i, interline_equation_list, page, [0, 0, 255])

    # Save the PDF
    pdf_docs.save(f"{out_path}/text.pdf")