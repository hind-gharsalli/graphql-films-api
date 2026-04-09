# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Table de liaison Film <-> Acteur (many-to-many)
film_acteur = Table(
    "film_acteur", Base.metadata,
    Column("film_id", Integer, ForeignKey("films.id")),
    Column("acteur_id", Integer, ForeignKey("acteurs.id"))
)

class Film(Base):
    __tablename__ = "films"
    id          = Column(Integer, primary_key=True)
    titre       = Column(String, nullable=False)
    annee       = Column(Integer)
    note        = Column(Float)
    genre       = Column(String)
    realisateur_id = Column(Integer, ForeignKey("realisateurs.id"))
    realisateur = relationship("Realisateur", back_populates="films")
    acteurs     = relationship("Acteur", secondary=film_acteur, back_populates="films")

class Realisateur(Base):
    __tablename__ = "realisateurs"
    id    = Column(Integer, primary_key=True)
    nom   = Column(String, nullable=False)
    films = relationship("Film", back_populates="realisateur")

class Acteur(Base):
    __tablename__ = "acteurs"
    id    = Column(Integer, primary_key=True)
    nom   = Column(String, nullable=False)
    films = relationship("Film", secondary=film_acteur, back_populates="acteurs")

