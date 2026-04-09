# collect_data.py
import requests
from database import SessionLocal, init_db
from models import Film, Realisateur, Acteur

API_KEY = "18d3a931b56a81126825badfdc6e888c"
BASE_URL = "https://api.themoviedb.org/3"

def fetch_and_insert_films():
    db = SessionLocal()
    init_db()

    for page in range(1, 6):  # 5 pages = ~100 films
        response = requests.get(
            f"{BASE_URL}/movie/popular",
            params={"api_key": API_KEY, "language": "fr-FR", "page": page}
        )
        films_data = response.json().get("results", [])

        for film_data in films_data:
            # Récupérer les détails + crédits du film
            details = requests.get(
                f"{BASE_URL}/movie/{film_data['id']}",
                params={"api_key": API_KEY, "append_to_response": "credits", "language": "fr-FR"}
            ).json()

            # Créer ou récupérer le réalisateur
            realisateur = None
            for member in details.get("credits", {}).get("crew", []):
                if member["job"] == "Director":
                    realisateur = db.query(Realisateur).filter_by(nom=member["name"]).first()
                    if not realisateur:
                        realisateur = Realisateur(nom=member["name"])
                        db.add(realisateur)
                        db.flush()
                    break

            # Créer le film
            film = Film(
                titre=details.get("title"),
                annee=int(details.get("release_date", "0000")[:4]) if details.get("release_date") else None,
                note=details.get("vote_average"),
                genre=details["genres"][0]["name"] if details.get("genres") else None,
                realisateur=realisateur
            )
            db.add(film)

            # Ajouter les acteurs (top 5)
            for cast_member in details.get("credits", {}).get("cast", [])[:5]:
                acteur = db.query(Acteur).filter_by(nom=cast_member["name"]).first()
                if not acteur:
                    acteur = Acteur(nom=cast_member["name"])
                    db.add(acteur)
                    db.flush()
                if acteur not in film.acteurs:
                    film.acteurs.append(acteur)

        db.commit()
        print(f"Page {page} insérée ✓")

    db.close()
    print("Base de données alimentée avec succès !")

if __name__ == "__main__":
    fetch_and_insert_films()
