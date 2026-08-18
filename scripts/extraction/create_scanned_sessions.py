#!/usr/bin/env python3
"""Create JSON files for the 3 scanned PDFs using OCR text provided by user"""
import json
from pathlib import Path

# OCR text for 12/2020 (provided by user)
session_2020_12_text = """Startup Act | Session 21 | Décembre 2020 | Compte-Rendu

| Société | Handlateurs | Seitur | Label/Prélibel | Zème Tour |  |  |  | Zème Tour |  | Resultat | Commentaires |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Société | Handlateurs | Seitur | Label/Prélibel | Receivable | Oui | Non | Pitching | Confitif | Oui | Resultat | Commentaires | Non |
| Telum | Nour Ehore Ghoseh Amal | Logiciel | Label | Oui | 8 | - | - | - | N.A | N.A | Label accorde | Label accorde des le 2ème tour |
| Ma Formation Privilee | Helmi Mash | E-commerce | Label | Oui | 6 | - | 3 | - | N.A | N.A | Label accorde | Label accorde des le 2ème tour |
| AirGraph | GHAYTH Bouygatta Lafalfa Rash Edouard Guilhot Daniel Balleger | Robotique | Label | Oui | 8 | - | - | - | N.A | N.A | Label accorde | Label accorde des le 2ème tour |
| LG P | Ahmed Miffes | Autre contenu créatif | Label | Oui | 8 | - | - | - | N.A | N.A | Label accorde | Label accorde des le 2ème tour |
| WAMIA | Abdereazak Ahlou Al Cherif Amri Kekasae | E-commerce | Label | Oui | 5 | 1 | 1 | 1 | N.A | N.A | Label accorde | Label accorde des le 2ème tour Eyjera jerba a déclare un conflit d'invente |
| moudda.com | Meeki Musselderb Karman Rokkane | E-commerce | Label | Oui | 7 | 1 | - | 1 | N.A | N.A | Label accorde | Label accorde des le 2ème tour Eyjera jerba a déclare un conflit d'invente |
| wiTrade | Mierten Nebi Zainib Nebi Taha Haitie | E-commerce | Label | Oui | 5 | - | 4 | - | N.A | N.A | Label accorde | Label accorde des le 2ème tour |
| SOAR | Aymen Tabi Nour Bourataize | Health Tech | Label | Oui | 5 | 1 | 3 | - | N.A | N.A | Label accorde | Label accorde des le 2ème tour |
| Datagram | Mohamed Ali Ben Aleya | Big Data | Label | Oui | 8 | - | - | - | N.A | N.A | Label accorde | Label accorde des le 2ème tour |
| IBIS Technologies | Khaled Bouchousha | Agrtech | Label | Oui | 7 | - | - | 1 | N.A | N.A | Label accorde | Label accorde des le 2ème tour Mohamed Salah Fadr a declare un conflit d'invente |
| PROSERVY | Ahmed Didi Wassim Ioani Mohamed Diyan Koutini | Logiciel | Label | Oui | 1 | 1 | 4 | - | 5 | 1 | Label accorde | Label accorde suite au pitching |
| Cagronte Fid | Omar Bacar Cager Bouchousha | E-commerce | Label | Oui | 4 | 1 | 3 | - | 6 | 1 | Label accorde | Label accorde suite au pitching |
| Smarth A smart and cloud based queue management system | Ramzi Zefani | Logiciel | Prelabel | Oui | 6 | 1 | 1 | - | N.A | N.A | Prelabel accorde | Prelabel accorde des le 2ème tour |
| NetShake Network Share Knowledge | Raith Bensi Abdalah Bakke | EdTech | Prelabel | Oui | 8 | - | - | - | N.A | N.A | Prelabel accorde | Prelabel accorde des le 2ème tour |
| Go Staff | Mohamed Hanoun Ouannes Wassim Khalfa | Health Tech | Prelabel | Oui | 8 | - | - | - | N.A | N.A | Prelabel accorde | Prelabel accorde des le 2ème tour |
| Kn_Traffic | Mohamed Salah Zaggar | Autre contenu créatif | Prelabel | Oui | 8 | - | - | - | N.A | N.A | Prelabel accorde | Prelabel accorde des le 2ème tour |
| Bridge ITops | Wald Saad | Logiciel | Prelabel | Oui | 8 | - | - | - | N.A | N.A | Prelabel accorde | Prelabel accorde des le 2ème tour |
| WARM | Marwa Ben Aissa | E-commerce | Prelabel | Oui | 4 | 3 | 1 | - | 5 | 1 | Prelabel accorde | Prelabel accorde suite au pitching |
| LEEVVA Communication | Wissem Bougulla Loc Lafhiq | Telecom | Prelabel | Oui | 1 | 3 | 4 | - | 5 | 3 | Prelabel accorde | Prelabel accorde suite au pitching |
| BasketID | Karmir Jabali Maker Chukai Wael Kaiso | Fintech | Prelabel | Oui | 4 | 1 | 3 | - | 5 | 1 | Prelabel accorde | Prelabel accorde suite au pitching |
| Key Software | Khaled Saddani | Logiciel | Label | Oui | - | 7 | 1 | - | N.A | N.A | Label non accorde | Label non accorde des le 2ème tour |
| BAIT | Ahmed Trad | Logiciel | Label | Oui | - | 8 | - | - | N.A | N.A | Label non accorde | Label non accorde des le 2ème tour |
| The Mission | Fatin Maslei Sandari Elbawi | EdTech | Label | Oui | - | 8 | - | - | N.A | N.A | Label non accorde | Label non accorde des le 2ème tour |
| instead | Karmir Ben Abdalaziz Arwa Bel Hiji Taha Beri Amal Guzman | Fintech | Label | Oui | - | 8 | - | - | N.A | N.A | Label non accorde | Label non accorde des le 2ème tour |
| MICRO DEVICE TUNISA | Hamdil Ben Amor | IoT | Label | Oui | 1 | 6 | 1 | - | N.A | N.A | Label non accorde | Label non accorde des le 2ème tour |
| Droopex | Ahmed Allesch Waet Allesch | Logistique | Label | Oui | 1 | 0 | 1 | - | N.A | N.A | Label non accorde | Label non accorde des le 2ème tour |
| OnePack | Sarra Fehail Firas Dheouad Malik Ahmed | EdTech | Label | Oui | 1 | 6 | 2 | - | N.A | N.A | Label non accorde | Label non accorde des le 2ème tour |

| Omaris Wood | Omar Trabelsi | Autre contenu créatif | Label | Oui | 1 | 7 | - | - | N.A | N.A | Label non accordé | Label non accordé dès le 2ème tour |
| OMNIUP | Karim Jelliti Issam Essefi Ali Sakka | Marketing | Label | Oui | - | 7 | 1 | - | N.A | N.A | Label non accordé | Label non accordé dès le 2ème tour |
| VirtuA Agency | Siem Ouled Hsin | Autre contenu créatif | Prélabel | Oui | - | 8 | - | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé dès le 2ème tour |
| EVO ENERGIZE | Maher Amara Safa Bouhajar | IoT | Prélabel | Oui | 1 | 6 | 2 | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé dès le 2ème tour |
| Pabitel.tn | Syrine Zgueb | Logiciel | Prélabel | Oui | - | 8 | - | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé dès le 2ème tour |
| Jood Lab | Mohamed Belghith Younes Ben Mabrouk | Logiciel | Prélabel | Oui | - | 6 | 2 | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé dès le 2ème tour |
| World Wide Security | Mohamed Aziz Elmabrouk | Autre contenu créatif | Prélabel | Oui | - | 8 | - | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé dès le 2ème tour |
| Mat7irech | Mohamed Harbaoui | Mobile | Prélabel | Oui | 3 | 3 | 2 | - | 0 | 6 | Prélabel non accordé | Prélabel non accordé suite au pitching |
| Flow | Omar Guizani Maher Bouzid | Fintech | Prélabel | Non | N.A | N.A | N.A | N.A | N.A | N.A | Prélabel non accordé | Dossier irrecevable pour manque d'autorisation de la part des autorités compétentes pour la pratique de l'activité présentée |

## Passage de Prélabels aux Labels

| Société | Projet | Fondateurs | Secteur | Session d'obtention du Prélabel | Résultat | Commentaires |
| --- | --- | --- | --- | --- | --- | --- |
| Certely Expert System | MTCE | Fares Amor Dhafer Ben Amor Nidhal Ben Amor | Autre contenu créatif | Août 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d'octroi |
| ArtGuru | Ba9chich | Melek Gharbi Bilel Ouersighni | Media | Novembre 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d'octroi |
| Sprindt Technologies | Sprindt | Habib Wenish Ramzi Hamrouni Hédi Akrout | Fintech | Mai 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d'octroi |
| Liberrex Tunisia | Liberrex | Achraf Ammar | Logiciel | Octobre 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d'octroi |
| Jeeby Technologies | Jeeby | Malek Zlitni Walid Bousnina Chamseddine Bezzaouia | E-commerce | Novembre 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d'octroi |
| BUS APP | Tchou-Tchou Your school bus tracking App | Narjes Ben Slimane | Logiciel | Avril 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d'octroi |
| Bioagri helpers | BIOAGRIHELPERS | Syrine Baghdadi Yosr Baghdadi Mayssa Ghazel | Agritech | Juillet 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d'octroi |
| E W | E W | Mohamed Baazaoui | E-commerce | Octobre 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d'octroi |
| FLAHTIK | GENI | Mohamed RAJHI Mohamed Ali TBESSI | Agritech | Août 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d'octroi |"""

# OCR text for 01/2021 (provided by user)
session_2021_01_text = """Startup Act | Session 22 | Janvier 2021 | Compte-Rendu

| Société | Fondation | Secteur | Label/Prélabel | Zème Tour |  |  |  | Zème Tour |  | Résultat | Commentaires |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Société | Fondation | Secteur | Label/Prélabel | Recevabilité | Oui | Non | Pitching | Confit | Oui | Résultat | Commentaires | Non |
| Menutium | Salem Moubah Amine Milka | Logiciel | Label | Oui | 7 | - | - | 1 | N.A | N.A | Label accorde | Label accorde des le 2e tour Eyes anta a déclair un conflit d'intérêt |
| Mymall.tn | Inks Béjar | E-commerce | Label | Oui | 7 | - | - | - | N.A | N.A | Label accorde | Label accorde des le 2e tour |
| IMMOTECH | Cyrine Ben Ayed Andolsi Jhed Yasinie Lakib Mohamed Raafal Limam | Logiciel | Label | Oui | 7 | - | - | - | N.A | N.A | Label accorde | Label accorde des le 2e tour |
| XQant Software | Chea Srun | Fintech | Label | Oui | 8 | - | - | - | N.A | N.A | Label accorde | Label accorde des le 2e tour |
| Medquick | Ahmad Turki Mustapha Turkı | E-commerce | Label | Oui | 5 | - | 3 | - | N.A | N.A | Label accorde | Label accorde des le 2e tour |
| z healthcare | Haryhem Zouauoul Mohamed Rush Bhar Khadjaj Moyoud Taha Harden | Health Tech | Label | Oui | 6 | - | - | 1 | N.A | N.A | Label accorde | Label accorde Mohamed Salah Frad a declaire un conflit d'intérêt |
| Coqira Tunisia | Hatem Selami | AI | Label | Oui | 7 | - | - | - | N.A | N.A | Label accorde | Label accorde des le 2e tour |
| Linkedfishers/Hookedup | Mahrem Zannouni Kake Iraq Ayed Gonbirni Abdessat Taipur Nareif Ben Moosaia | Plateforme Sociale | Label | Oui | 6 | - | 2 | - | N.A | N.A | Label accorde |  |
| SeaBot | Kebousu Rami Marwen Bosmina | IoT | Label | Oui | 6 | 1 | - | - | N.A | N.A | Label accorde | Label accorde des le 2e tour |
| Ms. Marion | Selma Belkodja Insuf Hamdi | E-commerce | Label | Oui | 5 | 1 | 1 | 1 | N.A | N.A | Label accorde | Label accorde des le 2e tour Hassen Harrabä a declair un conflit d'intérêt |
| WKF par FLEXITEK | Alexandre FLORES Mohamed DOMAA | Logiciel | Label | Oui | 3 | 1 | 4 | - | 6 | - | Label accorde | Label accorde suite au pitching |
| e-Sola | Sami Malaki David Simb | EdTech | Label | Oui | 3 | 4 | 1 | - | 7 | - | Label accorde | Label accorde suite au pitching |
| Tinith IBPM Automation Booster | Duassim Bourid Ramio Abidi | Logiciel | Label | Oui | 3 | - | 4 | - | 7 | 1 | Label accorde | Label accorde suite au pitching |
| Pulpetech | Wika Abbes Ousasian Ali | AI | Label | Oui | 3 | - | 5 | - | 8 | - | Label accorde | Label accorde suite au pitching |
| MineClap | Harned Khail Maaref Taha Yassine Chached Slim Maaref | Logistique | Label | Oui | 4 | - | 1 | 1 | 6 | 1 | Label accorde | Label accorde suite au pitching Hassen Harrabä a declair un conflit d'intérêt |
| FinBudd.com | Ors Bouali | EdTech | Prelabel | Oui | 8 | - | - | - | N.A | N.A | Prelabel accorde | Prelabel accorde des le 2e tour |
| YAGRI | Yasser Belguesini Bouallagu Dorsaf | Agritech | Prelabel | Oui | 7 | - | - | - | N.A | N.A | Prelabel accorde | Prelabel accorde des le 2e tour |
| Zheema | Amr Baik Salar Awald Tamer Shawer | Cleantech | Prelabel | Oui | 7 | - | - | - | N.A | N.A | Prelabel accorde | Prelabel accorde des le 2e tour |
| Arabclassroom | Cheki Samaali | EdTech | Prelabel | Oui | 6 | - | - | - | N.A | N.A | Prelabel accorde | Prelabel accorde des le 2e tour |
| Smart Racing Hub | Dussima Dhouadi Austre contenu creatif | Prelabel | Oui | 6 | - | 1 | - | - | N.A | N.A | Prelabel accorde | Prelabel accorde des le 2e tour |
| société Lave rit | Hedi Hrigua Oussai Hlauou Logistique | Prelabel | Oui | 7 | 1 | - | - | - | N.A | N.A | Prelabel accorde | Prelabel accorde des le 2e tour |
| Arty | Mohamed Ali Said Innis Gharrib Amour Kabel | E-commerce | Prelabel | Oui | 4 | 3 | - | 1 | 5 | 2 | Prelabel accorde | Prelabel accorde suite au pitching Hassen Harrabä a declair un conflit d'intérêt |

| PLUS WEB Solutions | Amina Triki | Plateforme Sociale | Label | Oui | - | 7 | - | - | N.A | N.A | Label non accordé | Label non accordé des le 2ème tour |
| AREAS (Agro Responsible Ecologic African Services ) | Zahra Shiri Hassen Ouerghemmi | Agritech | Prélabel | Oui | - | 6 | 3 | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé des le 2ème tour |
| EZ-TOOL | Mehdi Tatar Khalil Chelly | Logiciel | Prélabel | Oui | 1 | 5 | 2 | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé des le 2ème tour |
| e-dengri | Maroua Ben Charrada | Plateforme Sociale | Prélabel | Oui | - | 8 | - | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé des le 2ème tour |
| JEY | Belhaj Ines Seifedine Miladi Slim Sghir | IoT | Prélabel | Oui | 1 | 6 | - | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé des le 2ème tour |
| SMARTravel | Houcem Hajji | Logiciel | Prélabel | Oui | - | 7 | - | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé des le 2ème tour |
| HiMyCoach.com | Wajdi Bechaouech Rassil Rhouma Enkhanaa Achour | Plateforme Sociale | Prélabel | Oui | - | 7 | - | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé des le 2ème tour |
| Itialus Fidexia North Africa | Sami Ben Salem Wafa Cherid | Autre contenu créatif | Prélabel | Oui | - | 7 | - | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé des le 2ème tour |
| zeromate | Samir Chafai | Gaming | Prélabel | Oui | - | 8 | - | - | N.A | N.A | Prélabel non accordé | Prélabel non accordé des le 2ème tour |
| Koodys / Thor System | Mohamed Salah Nachi Malek Redissi | Logiciel | Label | Oui | 1 | 1 | 5 | - | 2 | 6 | Label non accordé | Label non accordé suite au pitching |
| Chill&Lit | Fares Kotti | E-commerce | Label | Oui | 3 | 2 | 2 | - | 3 | 4 | Label non accordé | Label non accordé suite au pitching |
| Overlapping UVs | Youssef Mejri | Autre contenu créatif | Prélabel | Oui | - | 3 | 5 | - | 2 | 5 | Prélabel non accordé | Prélabel non accordé suite au pitching |
| ABC Dev | Makrem Cherni Sdiri Mahdi Manel Ouerhani | Logiciel | Label | Non | N.A | N.A | N.A | N.A | N.A | N.A | Label non accordé | Dossier irreecevable pour non conformité du projet postulant pour son statut de personne physique, non morale. |
| BOXSTOP | Ghada Jandoubi Lauret Hanout | Logistique | Label | Non | N.A | N.A | N.A | N.A | N.A | N.A | Label non accordé | Dossier irreecevale pour présentation d'un document officiel altéré. |

## Passage de Prélabels aux Labels

| Société | Projet | Fondateurs | Secteur | Session d'obtention du Prélabel | Résultat | Commentaires |
| --- | --- | --- | --- | --- | --- | --- |
| DIGITRIS THINKERS | Wanavaa | Mohamed Ali Haddad Mohamed Amine Gharbi Sami Essid | E-commerce | Juillet 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d/octroi |
| ELLZ AND BEYOND Tunisia | ellz and beyond Tunisie | Aymen ellouze | Autre contenu créatif | Juillet 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d/octroi |
| GoStaff.io | Go Staff | Mohamed Haroun Ouanes Wassim Khalifa | Health Tech | Décembre 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d/octroi |
| PURA Solutions | PURA Solutions | Jaweher CHATBRI Youssef GAALICHE Ahmed MRABET | Health Tech | Juin 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d/octroi |
| HAKIM TECHNOLOGIE | HAKIM TECHNOLOGIE | Mondher Hakim | Energie | Août 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d/octroi |
| Sté Anath Healthcare | Meditech | Ferid Kamel | Health Tech | Juillet 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d/octroi |
| LoDeep | LoDeep | Ahmed Ghib Zied Ben Amar | EdTech | Novembre 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d/octroi |
| JUST PUBLISH | Alfikr part of JustPublish | Brahim Jrah | EdTech | Novembre 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d/octroi |
| IDARTY | IDARTY | Ahmed Zoghlami | Plateforme Sociale | Septembre 2020 | Label accordé | Label accordé suite à la création de la Startup et le respect des conditions d/octroi |"""

# 07/2020 - keep empty (partial scan, very limited text)
session_2020_07_text = ""

def parse_table_text(text):
    """Parse markdown table text into entries"""
    import re
    lines = text.split('\n')
    entries = []
    
    for line in lines:
        if '|' not in line or line.count('|') < 3:
            continue
        
        cells = [c.strip() for c in line.strip('|').split('|')]
        
        # Skip headers
        header_keywords = ['société', 'fondateurs', 'fondation', 'secteur', 'résultat', 'handlateurs', 'seitur']
        if any(kw in ' '.join(cells).lower() for kw in header_keywords):
            continue
        
        if all(c in ['', '-', '---'] for c in cells):
            continue
        
        if len(cells) >= 10 and cells[0]:
            entry = {
                'societe': cells[0],
                'fondateurs': cells[1] if len(cells) > 1 else '',
                'secteur': cells[2] if len(cells) > 2 else '',
                'type_label': cells[3] if len(cells) > 3 else '',
                'recevabilite': cells[4] if len(cells) > 4 else '',
                'oui': cells[5] if len(cells) > 5 else '0',
                'non': cells[6] if len(cells) > 6 else '0',
                'resultat': cells[10] if len(cells) > 10 else '',
                'commentaires': cells[11] if len(cells) > 11 else ''
            }
            entries.append(entry)
    
    return entries

def main():
    output_dir = Path('public/data/firecrawl_sessions')
    
    sessions = [
        ('session_2020_12', '2020', '12', session_2020_12_text),
        ('session_2021_01', '2021', '01', session_2021_01_text),
        ('session_2020_07', '2020', '07', session_2020_07_text),
    ]
    
    for session_id, year, month, text in sessions:
        entries = parse_table_text(text) if text else []
        
        session_data = {
            'session': f'{month}/{year}',
            'year': int(year),
            'month': int(month),
            'total_entries': len(entries),
            'source': 'ocr_user' if text else 'empty',
            'entries': entries
        }
        
        output_file = output_dir / f'{session_id}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        print(f'{"✅" if len(entries) > 0 else "⚠️"} {month}/{year}: {len(entries)} entries')

if __name__ == '__main__':
    main()
