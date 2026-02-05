#!/usr/bin/env python3
import sys
import fitz  # PyMuPDF
import collections
import re

def extract_annotations(pdf_path):
    doc = fitz.open(pdf_path)
    results = collections.defaultdict(list)

    for page_index in range(len(doc)):
        page = doc[page_index]
        annot = page.first_annot
        page_annots = []

        while annot:
            info = annot.info or {}
            # annot.info には title(作成者), content(本文), subject, creationDate, modDate などが入る場合があります
            item = {
                "author": info.get("title"),
                "content": info.get("content"),  # 付箋本文など
                # "creationDate": info.get("creationDate"),
                # "modDate": info.get("modDate"),
                "rect": list(annot.rect),        # 注釈の位置
            }
            print(list(annot.rect))
            page_annots.append(item)
            annot = annot.next

        if page_annots:
            results[page_index+1].extend(page_annots)

    doc.close()
    return results

if __name__ == "__main__":
    for item in sys.argv[1:]:
        print(item)
        annots = extract_annotations(item)
        page_list = list(annots.keys())
        page_list.sort()
        print("(ページ番号はPDFファイルの最初を1としてカウント)")
        for n in page_list:
            print(f"【{n}ページ】")
            annots_list = annots[n]
            annots_list.sort(key = lambda x: x["rect"][1])
            for i, a in enumerate(annots[n], start=1):
                comment = re.sub(r"\s+", " ", a["content"]).strip()
                print(f"・{comment}")
            print("")