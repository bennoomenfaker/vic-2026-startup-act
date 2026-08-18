import fitz

def parse_session_2025_01():
    doc = fitz.open('/home/himawari/Desktop/startup-act/public/data/session-pdfs/session_2025_01.pdf')
    print("--- 2025_01 ---")
    # We manually listed:
    # Nouveaux labels (8): Vie verte BSF, Docic, 1FOR1 LEARNING, Amperon Technologies, Artizone, Pass excellence, Nativeads Ai, Otravers
    # Prelabels (2): Readdly, Dari
    # Conversions (5): VYZYOSCHOOL, ECOCODE, linkbook, Paytea, Production d'additifs alimentaires animale et consulting

def parse_session_2019_06():
    doc = fitz.open('/home/himawari/Desktop/startup-act/public/data/session-pdfs/session_2019_06.pdf')
    print("--- 2019_06 ---")

def parse_session_2025_05():
    doc = fitz.open('/home/himawari/Desktop/startup-act/public/data/session-pdfs/session_2025_05.pdf')
    print("--- 2025_05 ---")

def parse_session_2023_12():
    doc = fitz.open('/home/himawari/Desktop/startup-act/public/data/session-pdfs/session_2023_12.pdf')
    print("--- 2023_12 ---")

def parse_session_2023_10():
    doc = fitz.open('/home/himawari/Desktop/startup-act/public/data/session-pdfs/session_2023_10.pdf')
    print("--- 2023_10 ---")

parse_session_2025_01()
parse_session_2019_06()
parse_session_2025_05()
parse_session_2023_12()
parse_session_2023_10()
