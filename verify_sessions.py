import fitz

doc = fitz.open('/home/himawari/Desktop/startup-act/public/data/session-pdfs/session_2023_10.pdf')
for page_num, page in enumerate(doc):
    print(f"=== PAGE {page_num+1} ===")
    text = page.get_text()
    for i, line in enumerate(text.split('\n')):
        print(f"{i+1:3d}: {line}")
