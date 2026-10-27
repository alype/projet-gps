import sys
import math
import csv

input_file = "input_log.txt"

# Etape 1
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

# Etape 2
def extraire_donnees_brutes(lines):
    records = []

    for line in lines:
        # TODO: Mettre en place un bloc try / except (ValueError, IndexError)
        try:
            champs = next(csv.reader([line]))

            # ignore les lignes trop courtes ou qui ne viennent pas de GNSS_ACCESS_LIB
            if len(champs) < 5 or champs[4].strip() != "GNSS_ACCESS_LIB":
                continue

            # Sépare les coordonnées dans le champ 3 et les convertir en nombres
            lat_txt, lon_txt = champs[3].split(",", 1)
            lat = float(lat_txt.strip())
            lon = float(lon_txt.strip())

            # Ignore les valeurs invalides (NaN par exemple)
            if not math.isfinite(lat) or not math.isfinite(lon):
                continue

            # Récupère la date et l'heure, en supprimant les microsecondes, et ajoute les valeurs valides à la liste records
            heure = champs[2].split(".", 1)[0]
            records.append({
                "timestamp": f"{champs[1]} {heure}",
                "lat": lat,
                "lon": lon,
            })

        # Ignore les lignes mal formées ou contenant des valeurs incorrectes
        except (ValueError, IndexError, StopIteration):
            continue

    return records

# Etape 3
def nettoyer_et_dedoublonner(records):
    cleaned = []
    for record in records:
        # TODO: Vérifier si lat, lon sont des NaN (math.isnan). Si oui, ignorer.
        try:
            lat = float(record["lat"])
            lon = float(record["lon"])

            # Ignore le point si la latitude ou la longitude est NaN
            if math.isnan(lat) or math.isnan(lon):
                continue

            # Ignore si lat ou lon incorrect
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                continue

            # Arrondis coordonnées
            record_arrondis = record.copy()
            record_arrondis["lat"] = round(lat, 2)
            record_arrondis["lon"] = round(lon, 2)

            # Ignore le point s'il est à moins de 1° du dernier point validé
            if cleaned:
                dernier = cleaned[-1]
                if (
                    abs(record_arrondis["lat"] - dernier["lat"]) <= 1.0
                    and abs(record_arrondis["lon"] - dernier["lon"]) <= 1.0
                ):
                    continue

            cleaned.append(record_arrondis)

        except (KeyError, TypeError, ValueError):
            continue

    return cleaned

if __name__ == "__main__":
    lignes = lire_et_filtrer_fichier(input_file)
    records = extraire_donnees_brutes(lignes)
    points_nettoyes = nettoyer_et_dedoublonner(records)

    print(f"[ETAPE 1] Lignes retenues : {len(lignes)}")
    print(f"[ETAPE 2] Enregistrements valides : {len(records)}")
    print(f"[ETAPE 3] Points nettoyés et dédoublonnés: {len(points_nettoyes)}")

