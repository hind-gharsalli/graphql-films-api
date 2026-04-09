# schema.py
import strawberry
from typing import List, Optional

@strawberry.type
class ActeurType:
    id: int
    nom: str
    films: List["FilmType"] 
@strawberry.type
class RealisateurType:
    id: int
    nom: str

@strawberry.type
class FilmType:
    id: int
    titre: str
    annee: Optional[int]
    note: Optional[float]
    genre: Optional[str]
    realisateur: Optional[RealisateurType]
    acteurs: List[ActeurType]
