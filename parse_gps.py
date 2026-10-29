import sys
import math
import csv
import hashlib

input_file = "input_log.txt"

# Etape 1
def lire_et_filtrer_fichier(input_file):
    lignes_filtrees = []

    # Ouvrir le fichier avec l'encodage 'latin-1'
    with open(input_file, encoding="latin-1") as fichier:
        # Parcourir le fichier ligne par ligne
        for ligne in fichier:
            # Si la ligne contient "GNSS_ACCESS_LIB" ou "Trip Data",
            # l'ajouter à lines_filtrees 
            if "GNSS_ACCESS_LIB" in ligne or "Trip Data" in ligne:
                lignes_filtrees.append(ligne.strip())
                
    return lignes_filtrees

# Etape 2
def extraire_donnees_brutes(lines):
    records = []

    for line in lines:
        # Mettre en place un bloc try / except (ValueError, IndexError)
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
            date = champs[1]
            heure = champs[2].split(".", 1)[0]

            records.append({
                "date": date,
                "heure": heure,
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

            # Ignore le point s'il est à moins de 0.05° du dernier point validé
            if cleaned:
                dernier = cleaned[-1]
                if (
                    abs(record_arrondis["lat"] - dernier["lat"]) <= 0.05
                    and abs(record_arrondis["lon"] - dernier["lon"]) <= 0.05
                ):
                    continue

            cleaned.append(record_arrondis)

        except (KeyError, TypeError, ValueError):
            continue

    return cleaned

# Etape 4
def exporter_et_hasher(cleaned, output_file="output_cleaned.csv"):
    # Ouvre ou crée le fichier en écriture, avec un encodage utf-8
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Ecrit l'en-tête du fichier CSV
        writer.writerow(["date", "heure", "latitude", "longitude"])

        # Ecrit une ligne CSV pour chaque coordonnée nettoyée
        for record in cleaned:
            writer.writerow([
                record["date"],
                record["heure"],
                record["lat"],
                record["lon"],
            ])

    # Crée un objet pour calculer l'empreinte SHA-256
    hasher = hashlib.sha256()

    # Rouvre le fichier en mode binaire pour calculer son empreinte
    with open(output_file, "rb") as f:
        # Lit le fichier par blocs de 4096 octets
        for bloc in iter(
            lambda: f.read(4096), b""
        ):
            hasher.update(bloc)

    # Retourne l'empreinte SHA-256 en chaîne hexadécimale
    return hasher.hexdigest()


if __name__ == "__main__":
    lignes = lire_et_filtrer_fichier(input_file)
    records = extraire_donnees_brutes(lignes)
    points_nettoyes = nettoyer_et_dedoublonner(records)
    sha256_hash = exporter_et_hasher(points_nettoyes)

    print(f"[ETAPE 1] Lignes retenues : {len(lignes)}")  
    print(f"[ETAPE 2] Enregistrements valides : {len(records)}")
    print(f"[ETAPE 3] Points nettoyés et dédoublonnés: {len(points_nettoyes)}")
    print(f"[ETAPE 4] SHA-256: {sha256_hash}")
    print(f"[ETAPE 4] FLAG: FLAG_OCLCC_{sha256_hash[:12]}")
