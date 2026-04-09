# mutations.py
import strawberry
from typing import Optional
from models import Film, Realisateur, Acteur
from schema import FilmType

@strawberry.type
class Mutation:

    @strawberry.mutation
    def ajouter_film(
        self, info: strawberry.Info,
        titre: str,
        annee: Optional[int] = None,
        note: Optional[float] = None,
        genre: Optional[str] = None,
        realisateur_id: Optional[int] = None
    ) -> FilmType:
        # --- VÉRIFICATION DE SÉCURITÉ ---
        if not info.context.get("user"):
            raise Exception("Accès refusé : Vous devez être connecté pour ajouter un film !")
        # --------------------------------
        
        db = info.context["db"]
        film = Film(titre=titre, annee=annee, note=note, genre=genre, realisateur_id=realisateur_id)
        db.add(film)
        db.commit()
        db.refresh(film)
        
        # Notifier les subscribers
        if "pubsub" in info.context:
            info.context["pubsub"].publish("FILM_AJOUTE", film)
            
        return film

    @strawberry.mutation
    def modifier_film(self, info: strawberry.Info, id: int, titre: Optional[str] = None, note: Optional[float] = None) -> Optional[FilmType]:
        # --- VÉRIFICATION DE SÉCURITÉ ---
        if not info.context.get("user"):
            raise Exception("Accès refusé : Vous devez être connecté pour modifier un film !")
        # --------------------------------
        
        db = info.context["db"]
        film = db.query(Film).filter(Film.id == id).first()
        if not film:
            return None
            
        if titre: film.titre = titre
        if note: film.note = note
        db.commit()
        db.refresh(film)
        return film

    @strawberry.mutation
    def supprimer_film(self, info: strawberry.Info, id: int) -> bool:
        # --- VÉRIFICATION DE SÉCURITÉ ---
        if not info.context.get("user"):
            raise Exception("Accès refusé : Vous devez être connecté pour supprimer un film !")
        # --------------------------------
        
        db = info.context["db"]
        film = db.query(Film).filter(Film.id == id).first()
        if not film:
            return False
            
        db.delete(film)
        db.commit()
        return True
