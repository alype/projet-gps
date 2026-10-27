import sys

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

if __name__ == "__main__":
    lignes = lire_et_filtrer_fichier(input_file)
    print(f"[ETAPE 1] Lignes retenues : {len(lignes)}")
    # Sortie Attendue: [ETAPE 1] Lignes retenues: 6

