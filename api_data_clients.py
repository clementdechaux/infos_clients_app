def get_entreprise_infos(nom, code_postal=None, adresse=None):
    """
    Recherche une entreprise par nom (obligatoire), code postal (optionnel) et adresse (optionnelle).
    Retourne un DataFrame pandas avec Nom Entreprise, Adresse, Code Postal, SIREN, TVA.
    Prend uniquement le premier résultat retourné par l'API.
    """
    import requests
    import pandas as pd

    params = {
        "q": nom,
        "per_page": 5
    }
    if code_postal:
        params["code_postal"] = code_postal
    if adresse:
        params["adresse"] = adresse
    url = "https://recherche-entreprises.api.gouv.fr/search"
    headers = {"accept": "application/json", "User-Agent": "outil_devis_demo/1.0"}
    response = requests.get(url, params=params, headers=headers)
    if not response.ok:
        raise Exception(f"Erreur API: {response.status_code} {response.text}")
    data = response.json()
    results = data.get("results", [])
    if not results:
        return pd.DataFrame(columns=["Nom Entreprise", "Adresse", "Code Postal", "SIREN", "TVA"])
    r = results[0]
    nom_ent = r.get("nom_complet")
    siege = r.get("siege", {})
    adresse_ent = siege.get("adresse")
    code_postal_ent = siege.get("code_postal")
    siren = r.get("siren")
    def tva_fr(siren):
        siren = str(siren)
        if len(siren) != 9 or not siren.isdigit():
            return None
        cle = (12 + 3 * (int(siren) % 97)) % 97
        return f"FR{cle:02d}{siren}"
    tva = tva_fr(siren)
    row = {
        "Nom Entreprise": nom_ent,
        "Code Postal": code_postal_ent,
        "SIREN": siren,
        "TVA": tva,
        "Adresse": adresse_ent,
        "Code Postal": code_postal_ent,
    }
    return pd.DataFrame([row])
