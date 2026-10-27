import sys
import math
import csv

input_file = "input_log.txt"

def lire_et_filtrer_fichier(input_file):
    lignes_filtrees = []

    # TODO: Ouvrir le fichier avec l'encodage 'latin-1'
    with open(input_file, encoding="latin-1") as fichier:
        # TODO: Parcourir le fichier ligne par ligne
        for ligne in fichier:
            # TODO: Si la ligne contient "GNSS_ACCESS_LIB" ou "Trip Data",
            # l'ajouter à lines_filtrees (pensez à faire .strip())
            if "GNSS_ACCESS_LIB" in ligne or "Trip Data" in ligne:
                lignes_filtrees.append(ligne.strip())
                
    return lignes_filtrees

def extraire_donnees_brutes(lines):
    records = []

    for line in lines:
        # TODO: Mettre en place un bloc try / except (ValueError, IndexError)
        try:
            champs = next(csv.reader([line]))

            # ignore lignes non CSV
            if len(champs) < 5 or champs[4].strip() != "GNSS_ACCESS_LIB":
                continue

            lat_txt, lon_txt = champs[3].split(",", 1)
            lat = float(lat_txt.strip())
            lon = float(lon_txt.strip())

            if not math.isfinite(lat) or not math.isfinite(lon):
                continue

            heure = champs[2].split(".", 1)[0]
            records.append({
                "timestamp": f"{champs[1]} {heure}",
                "lat": lat,
                "lon": lon,
            })

            if not math.isfinite(lat) or not math.isfinite(lon):
                continue

            heure = champs[2].split(".", 1)[0]
            records.append({
                "timestamp": f"{champs[1]} {heure}",
                "lat": lat,
                "lon": lon,
            })

        except (ValueError, IndexError, StopIteration):
            continue
            #print(f"Ligne ignorée : {line!r} - {error}")

    return records

if __name__ == "__main__":
    lignes = lire_et_filtrer_fichier(input_file)
    records = extraire_donnees_brutes(lignes)

    print(f"[ETAPE 1] Lignes retenues : {len(lignes)}")
    # Sortie Attendue: [ETAPE 1] Lignes retenues: 6
    print(f"[ETAPE 2] Enregistrements valides : {len(records)}")

