# queries.py
import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from models import Film, Acteur, Realisateur
from schema import FilmType, ActeurType, RealisateurType

@strawberry.type
class Query:

    @strawberry.field
    def films(
        self,
        info: strawberry.Info ,
        genre: Optional[str] = None,
        tri_par: Optional[str] = "titre",
        page: int = 1,
        par_page: int = 10
    ) -> List[FilmType]:
        db: Session = info.context["db"]
        query = db.query(Film)
        if genre:
            query = query.filter(Film.genre == genre)
        if tri_par == "note":
            query = query.order_by(Film.note.desc())
        elif tri_par == "annee":
            query = query.order_by(Film.annee.desc())
        else:
            query = query.order_by(Film.titre)
        # Pagination
        offset = (page - 1) * par_page
        return query.offset(offset).limit(par_page).all()

    @strawberry.field
    def film(self, info:strawberry.Info, id: int) -> Optional[FilmType]:
        db: Session = info.context["db"]
        return db.query(Film).filter(Film.id == id).first()

    @strawberry.field
    def acteurs(self, info: strawberry.Info) -> List[ActeurType]:
        db: Session = info.context["db"]
        return db.query(Acteur).all()
    @strawberry.field
    def acteur(self, info: strawberry.Info, id: int) -> Optional[ActeurType]:
        db = info.context["db"]
        return db.query(Acteur).filter(Acteur.id == id).first()
