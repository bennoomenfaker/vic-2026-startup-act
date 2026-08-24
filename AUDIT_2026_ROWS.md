# Audit des lignes PDF 04/2026–06/2026

## Conclusion

L’hypothèse est confirmée par la comparaison des PDF locaux et des métadonnées JSON. Les fichiers `session-pdfs-json` ne contiennent pas toutes les lignes du tableau principal : ils contiennent les lignes officielles déjà extraites, mais plusieurs candidatures du bloc principal ont été omises. Les compteurs `session_data` permettent de contrôler l’écart attendu :

| Session | Candidatures officielles | Conversions prélabel → label | Retraits | Lignes PDF attendues | Entrées JSON actuelles | Écart constaté |
|---|---:|---:|---:|---:|---:|---:|
| 04/2026 | 41 | 4 | 5 | 50 | 47 | 3 |
| 05/2026 | 40 | 5 | 3 | 48 | 42 | 6 |
| 06/2026 | 40 | 4 | 3 | 47 | 45 | 2 |

La formule de contrôle est `lignes attendues = candidatures officielles + conversions + retraits`. Elle ne signifie pas que chaque ligne documentaire est une nouvelle candidature institutionnelle : les conversions et retraits sont des lignes documentaires supplémentaires.

## Lignes retrouvées dans les PDF mais absentes des JSON

04/2026 : Mathix Academy (EdTech, Label non accordé au 2ème tour), SURUS (Transportation, Label accordé au 3ème tour) et Tunisia transfert (TravelTech, Prélabel non accordé au 2ème tour).

05/2026 : Deep SaaS (RH, Prélabel non accordé au 3ème tour), Carbon Zero Tech (Energy, Prélabel non accordé au 2ème tour), NFASS (HealthTech, Prélabel non accordé au 2ème tour), FIXITECHPRO (ERP, Prélabel accordé au 2ème tour), Cuber (Other, Prélabel accordé au 3ème tour) et shopyia (Marketplace / e-commerce, Prélabel non accordé au 2ème tour).

06/2026 : Nvitee (Websites and mobile apps, Label non accordé au 2ème tour) et Creedex (Other, Prélabel non accordé au 2ème tour).

Les PDF locaux et les PDF du dépôt ont été comparés par SHA-256 et sont identiques pour ces trois sessions. Les noms et décisions ci-dessus proviennent donc bien des PDF versionnés.

## Conséquence sur les totaux

Le corpus actuel est sous-compté de 11 lignes documentaires : 3 + 6 + 2. Si ces lignes sont intégrées dans les JSON canoniques, les lignes PDF passeraient de 3 555 à 3 566, et la série corrigée incluant les 3 ajournés hors PDF passerait de 3 558 à 3 569. Les compteurs officiels de candidatures, labels, prélabels, conversions et retraits restent séparés et ne doivent pas être remplacés par le seul nombre de lignes PDF.

Aucune régénération globale n’a été appliquée pendant cet audit. Une validation est requise avant de modifier les JSON, CSV, SQL, Excel, rapports et affichages du site.
