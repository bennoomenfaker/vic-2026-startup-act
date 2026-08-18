#!/usr/bin/env python3
"""
Remplit les 2 sessions dont le PDF n'a pas de couche texte :
  - 12/2020 (Session 21, Décembre 2020)
  - 01/2021 (Session 22, Janvier 2021)

Source : texte du Compte-Rendu fourni par l'utilisateur (OCR du PDF, 18/08/2026).
Validation : les comptes correspondent aux données officielles (session_data) :
  - 12/2020 : 36 candidatures, 12 labels + 9 conversions = 21 labels, 8 prélabels
  - 01/2021 : 36 candidatures, 15 labels + 9 conversions = 24 labels, 7 prélabels

Actions :
  1. Met à jour public/data/session-pdfs-json/session_2020_12.json et session_2021_01.json
     (remplit `entrees`, garde `session_data` officiel inchangé).
  2. Met à jour /tmp/buffy_pdf_texts/ (texte + has_text=true + summary.json).
"""
import json
import os

JSON_DIR = "public/data/session-pdfs-json"
TMP_DIR = "/tmp/buffy_pdf_texts"

# (societe, fondateurs, secteur, resultat)
ENTREES_2020_12 = [
    ("Telum", "Nour Ehore Ghoseh Amal", "Logiciel", "label accorde"),
    ("Ma Formation Privilee", "Helmi Mash", "E-commerce", "label accorde"),
    ("AirGraph", "GHAYTH Bouygatta Lafalfa Rash Edouard Guilhot Daniel Balleger", "Robotique", "label accorde"),
    ("LG P", "Ahmed Miffes", "Autre contenu créatif", "label accorde"),
    ("WAMIA", "Abdereazak Ahlou Al Cherif Amri Kekasae", "E-commerce", "label accorde"),
    ("moudda.com", "Meeki Musselderb Karman Rokkane", "E-commerce", "label accorde"),
    ("wiTrade", "Mierten Nebi Zainib Nebi Taha Haitie", "E-commerce", "label accorde"),
    ("SOAR", "Aymen Tabi Nour Bourataize", "Health Tech", "label accorde"),
    ("Datagram", "Mohamed Ali Ben Aleya", "Big Data", "label accorde"),
    ("IBIS Technologies", "Khaled Bouchousha", "Agrtech", "label accorde"),
    ("PROSERVY", "Ahmed Didi Wassim Ioani Mohamed Diyan Koutini", "Logiciel", "label accorde"),
    ("Cagronte Fid", "Omar Bacar Cager Bouchousha", "E-commerce", "label accorde"),
    ("Smarth", "Ramzi Zefani", "Logiciel", "prelabel accorde"),
    ("NetShake", "Raith Bensi Abdalah Bakke", "EdTech", "prelabel accorde"),
    ("Go Staff", "Mohamed Hanoun Ouannes Wassim Khalfa", "Health Tech", "prelabel accorde"),
    ("Kn_Traffic", "Mohamed Salah Zaggar", "Autre contenu créatif", "prelabel accorde"),
    ("Bridge ITops", "Wald Saad", "Logiciel", "prelabel accorde"),
    ("WARM", "Marwa Ben Aissa", "E-commerce", "prelabel accorde"),
    ("LEEVVA Communication", "Wissem Bougulla Loc Lafhiq", "Telecom", "prelabel accorde"),
    ("BasketID", "Karmir Jabali Maker Chukai Wael Kaiso", "Fintech", "prelabel accorde"),
    ("Key Software", "Khaled Saddani", "Logiciel", "label non accorde"),
    ("BAIT", "Ahmed Trad", "Logiciel", "label non accorde"),
    ("The Mission", "Fatin Maslei Sandari Elbawi", "EdTech", "label non accorde"),
    ("instead", "Karmir Ben Abdalaziz Arwa Bel Hiji Taha Beri Amal Guzman", "Fintech", "label non accorde"),
    ("MICRO DEVICE TUNISA", "Hamdil Ben Amor", "IoT", "label non accorde"),
    ("Droopex", "Ahmed Allesch Waet Allesch", "Logistique", "label non accorde"),
    ("OnePack", "Sarra Fehail Firas Dheouad Malik Ahmed", "EdTech", "label non accorde"),
    ("Omaris Wood", "Omar Trabelsi", "Autre contenu créatif", "label non accorde"),
    ("OMNIUP", "Karim Jelliti Issam Essefi Ali Sakka", "Marketing", "label non accorde"),
    ("إبراهيم الدين - VirtuA Agency", "Siem Ouled Hsin", "Autre contenu créatif", "prelabel non accorde"),
    ("EVO ENERGIZE", "Maher Amara Safa Bouhajar", "IoT", "prelabel non accorde"),
    ("Pabitel.tn", "Syrine Zgueb", "Logiciel", "prelabel non accorde"),
    ("Jood Lab", "Mohamed Belghith Younes Ben Mabrouk", "Logiciel", "prelabel non accorde"),
    ("World Wide Security", "Mohamed Aziz Elmabrouk", "Autre contenu créatif", "prelabel non accorde"),
    ("Mat7irech", "Mohamed Harbaoui", "Mobile", "prelabel non accorde"),
    ("Flow", "Omar Guizani Maher Bouzid", "Fintech", "prelabel non accorde"),
]

ENTREES_2021_01 = [
    ("Menutium", "Salem Moubah Amine Milka", "Logiciel", "label accorde"),
    ("Mymall.tn", "Inks Béjar", "E-commerce", "label accorde"),
    ("IMMOTECH", "Cyrine Ben Ayed Andolsi Jhed Yasinie Lakib Mohamed Raafal Limam", "Logiciel", "label accorde"),
    ("XQant Software", "Chea Srun", "Fintech", "label accorde"),
    ("Medquick", "Ahmad Turki Mustapha Turkı", "E-commerce", "label accorde"),
    ("z healthcare", "Haryhem Zouauoul Mohamed Rush Bhar Khadjaj Moyoud Taha Harden", "Health Tech", "label accorde"),
    ("Coqira Tunisia", "Hatem Selami", "AI", "label accorde"),
    ("Linkedfishers/Hookedup", "Mahrem Zannouni Kake Iraq Ayed Gonbirni Abdessat Taipur Nareif Ben Moosaia", "Plateforme Sociale", "label accorde"),
    ("SeaBot", "Kebousu Rami Marwen Bosmina", "IoT", "label accorde"),
    ("Ms. Marion", "Selma Belkodja Insuf Hamdi", "E-commerce", "label accorde"),
    ("WKF par FLEXITEK", "Alexandre FLORES Mohamed DOMAA", "Logiciel", "label accorde"),
    ("e-Sola", "Sami Malaki David Simb", "EdTech", "label accorde"),
    ("Tinith IBPM Automation Booster", "Duassim Bourid Ramio Abidi", "Logiciel", "label accorde"),
    ("Pulpetech", "Wika Abbes Ousasian Ali", "AI", "label accorde"),
    ("MineClap", "Harned Khail Maaref Taha Yassine Chached Slim Maaref", "Logistique", "label accorde"),
    ("FinBudd.com", "Ors Bouali", "EdTech", "prelabel accorde"),
    ("YAGRI", "Yasser Belguesini Bouallagu Dorsaf", "Agritech", "prelabel accorde"),
    ("Zheema", "Amr Baik Salar Awald Tamer Shawer", "Cleantech", "prelabel accorde"),
    ("Arabclassroom", "Cheki Samaali", "EdTech", "prelabel accorde"),
    ("Smart Racing Hub", "Dussima Dhouadi", "Autre contenu créatif", "prelabel accorde"),
    ("société Lave rit", "Hedi Hrigua Oussai Hlauou", "Logistique", "prelabel accorde"),
    ("Arty", "Mohamed Ali Said Innis Gharrib Amour Kabel", "E-commerce", "prelabel accorde"),
    ("PLUS WEB Solutions", "Amina Triki", "Plateforme Sociale", "label non accorde"),
    ("AREAS (Agro Responsible Ecologic African Services)", "Zahra Shiri Hassen Ouerghemmi", "Agritech", "prelabel non accorde"),
    ("EZ-TOOL", "Mehdi Tatar Khalil Chelly", "Logiciel", "prelabel non accorde"),
    ("e-dengri", "Maroua Ben Charrada", "Plateforme Sociale", "prelabel non accorde"),
    ("JEY", "Belhaj Ines Seifedine Miladi Slim Sghir", "IoT", "prelabel non accorde"),
    ("SMARTravel", "Houcem Hajji", "Logiciel", "prelabel non accorde"),
    ("HiMyCoach.com", "Wajdi Bechaouech Rassil Rhouma Enkhanaa Achour", "Plateforme Sociale", "prelabel non accorde"),
    ("Itialus Fidexia North Africa", "Sami Ben Salem Wafa Cherid", "Autre contenu créatif", "prelabel non accorde"),
    ("zeromate", "Samir Chafai", "Gaming", "prelabel non accorde"),
    ("Koodys / Thor System", "Mohamed Salah Nachi Malek Redissi", "Logiciel", "label non accorde"),
    ("Chill&Lit", "Fares Kotti", "E-commerce", "label non accorde"),
    ("Overlapping UVs", "Youssef Mejri", "Autre contenu créatif", "prelabel non accorde"),
    ("ABC Dev", "Makrem Cherni Sdiri Mahdi Manel Ouerhani", "Logiciel", "label non accorde"),
    ("BOXSTOP", "Ghada Jandoubi Lauret Hanout", "Logistique", "label non accorde"),
]

# Conversions "Passage de Prélabels aux Labels" (societe, projet, fondateurs, secteur, session_prelabel)
CONVERSIONS_2020_12 = [
    ("Certely Expert System", "MTCE", "Fares Amor Dhafer Ben Amor Nidhal Ben Amor", "Autre contenu créatif", "Août 2020"),
    ("ArtGuru", "Ba9chich", "Melek Gharbi Bilel Ouersighni", "Media", "Novembre 2020"),
    ("Sprindt Technologies", "Sprindt", "Habib Wenish Ramzi Hamrouni Hédi Akrout", "Fintech", "Mai 2020"),
    ("Liberrex Tunisia", "Liberrex", "Achraf Ammar", "Logiciel", "Octobre 2020"),
    ("Jeeby Technologies", "Jeeby", "Malek Zlitni Walid Bousnina Chamseddine Bezzaouia", "E-commerce", "Novembre 2020"),
    ("BUS APP", "Tchou-Tchou Your school bus tracking App", "Narjes Ben Slimane", "Logiciel", "Avril 2020"),
    ("Bioagri helpers", "BIOAGRIHELPERS", "Syrine Baghdadi Yosr Baghdadi Mayssa Ghazel", "Agritech", "Juillet 2020"),
    ("E W", "E W", "Mohamed Baazaoui", "E-commerce", "Octobre 2020"),
    ("FLAHTIK", "GENI", "Mohamed RAJHI Mohamed Ali TBESSI", "Agritech", "Août 2020"),
]

CONVERSIONS_2021_01 = [
    ("DIGITRIS THINKERS", "Wanavaa", "Mohamed Ali Haddad Mohamed Amine Gharbi Sami Essid", "E-commerce", "Juillet 2020"),
    ("ELLZ AND BEYOND Tunisia", "ellz and beyond Tunisie", "Aymen ellouze", "Autre contenu créatif", "Juillet 2020"),
    ("GoStaff.io", "Go Staff", "Mohamed Haroun Ouanes Wassim Khalifa", "Health Tech", "Décembre 2020"),
    ("PURA Solutions", "PURA Solutions", "Jaweher CHATBRI Youssef GAALICHE Ahmed MRABET", "Health Tech", "Juin 2020"),
    ("HAKIM TECHNOLOGIE", "HAKIM TECHNOLOGIE", "Mondher Hakim", "Energie", "Août 2020"),
    ("Sté Anath Healthcare", "Meditech", "Ferid Kamel", "Health Tech", "Juillet 2020"),
    ("LoDeep", "LoDeep", "Ahmed Ghib Zied Ben Amar", "EdTech", "Novembre 2020"),
    ("JUST PUBLISH", "Alfikr part of JustPublish", "Brahim Jrah", "EdTech", "Novembre 2020"),
    ("IDARTY", "IDARTY", "Ahmed Zoghlami", "Plateforme Sociale", "Septembre 2020"),
]

SOURCE = "Texte du Compte-Rendu fourni par l'utilisateur (OCR du PDF sans couche texte) — 18/08/2026"


def render_text(entrees, conversions, header):
    """Rend le texte lisible de la session (format comparable au texte extrait des autres PDFs)."""
    lines = [header, ""]
    for soc, fond, sect, res in entrees:
        lines.append(f"{soc} | {fond} | {sect} | {res}")
    lines += ["", "Passage de Prélabels aux Labels", ""]
    for soc, projet, fond, sect, sess in conversions:
        lines.append(f"{soc} | {projet} | {fond} | {sect} | Prélabel {sess} | label accordé")
    return "\n".join(lines)


def update_project_json(session_file, entrees):
    path = os.path.join(JSON_DIR, session_file)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    data["nb_entrees"] = len(entrees)
    data["entrees"] = [
        {"societe": s, "fondateurs": f, "secteur": sect, "resultat": r}
        for s, f, sect, r in entrees
    ]
    data["source"] = SOURCE
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {session_file}: nb_entrees={len(entrees)}")


def update_tmp_json(name, text, pages):
    path = os.path.join(TMP_DIR, f"{name}.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    data["text_length"] = len(text)
    data["has_text"] = True
    data["source"] = SOURCE
    data["pages_text"] = [{"page": 1, "text": text}]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # summary.json
    summary_path = os.path.join(TMP_DIR, "summary.json")
    with open(summary_path, encoding="utf-8") as f:
        summary = json.load(f)
    summary[data["session"]]["text_length"] = len(text)
    summary[data["session"]]["has_text"] = True
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {name}.json (/tmp) : has_text=true, {len(text)} chars")


def main():
    print("1. Mise à jour des JSON projet (session-pdfs-json)")
    update_project_json("session_2020_12.json", ENTREES_2020_12)
    update_project_json("session_2021_01.json", ENTREES_2021_01)

    print("2. Mise à jour des JSON /tmp/buffy_pdf_texts")
    text_2020_12 = render_text(ENTREES_2020_12, CONVERSIONS_2020_12,
                               "Startup Act | Session 21 | Décembre 2020 | Compte-Rendu")
    text_2021_01 = render_text(ENTREES_2021_01, CONVERSIONS_2021_01,
                               "Startup Act | Session 22 | Janvier 2021 | Compte-Rendu")
    update_tmp_json("session_2020_12", text_2020_12, 2)
    update_tmp_json("session_2021_01", text_2021_01, 2)

    # Vérification des totaux vs session_data officiel
    for f in ["session_2020_12.json", "session_2021_01.json"]:
        d = json.load(open(os.path.join(JSON_DIR, f), encoding="utf-8"))
        n = len(d["entrees"])
        labels = sum(1 for e in d["entrees"] if e["resultat"] == "label accorde")
        prelabels = sum(1 for e in d["entrees"] if e["resultat"] == "prelabel accorde")
        print(f"\n  {f}: entrees={n}, labels accordés={labels}, prélabels accordés={prelabels} "
              f"(officiel: candidatures={d['session_data']['candidatures']}, "
              f"labels={d['session_data']['labels']}, preLabels={d['session_data']['preLabels']})")


if __name__ == "__main__":
    main()
