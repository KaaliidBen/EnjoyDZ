from sqlalchemy import Column,Integer,String,ForeignKey,Boolean,TEXT,DateTime,Table
from db.database import Base
from sqlalchemy.orm import relationship


user_point_table = Table('user_point', Base.metadata,
                        Column('user_id', Integer, ForeignKey('utilisateurs.id')),
                        Column('point_id', Integer, ForeignKey('points.id'))
                        )
point_moyen_table = Table('point_moyen', Base.metadata,
                        Column('point_id', Integer, ForeignKey('points.id')),
                        Column('moyen_id', Integer, ForeignKey('transports.id'))
                        )

class PointInteret(Base):
    __tablename__ = 'points'
    id = Column(Integer,primary_key=True,index=True)
    Nom = Column(TEXT)
    Description = Column(TEXT)

    Carte_id = Column(Integer,ForeignKey('cartes.id'))
    carte = relationship("Carte",back_populates='points')

    Horaire_id = Column(Integer,ForeignKey('horaires.id'))
    horaires = relationship("Horaire",back_populates='hrPoints')

    commentaires = relationship("Commentaire",back_populates='cmPoint')

    moyenTransport = relationship("MoyenTransport",secondary=point_moyen_table, back_populates ='mtPoint')
    

    evenements = relationship("Evenement",back_populates='evPoint')

    Theme_id = Column(Integer,ForeignKey('themes.id'))
    themes = relationship("Theme",back_populates='tmPoint')

    Categorie_id = Column(Integer,ForeignKey('categories.id'))
    categories = relationship("Categorie",back_populates='ctPoint')

    fans = relationship('Utilisateur', secondary=user_point_table, back_populates='favoris')

    



class Horaire(Base):
    __tablename__ = 'horaires'
    id = Column(Integer, primary_key=True,index=True)
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)

    hrPoints = relationship("PointInteret",back_populates='horaires')
    
    hrEvenements = relationship("Evenement",back_populates='horaires')

    
class Carte(Base):
    __tablename__='cartes'
    id = Column(Integer, primary_key=True,index=True)
    Nom = Column(TEXT)
    points = relationship("PointInteret",back_populates='carte')

class Theme(Base):

    __tablename__='themes'
    id = Column(Integer, primary_key=True,index=True)
    Nom = Column(TEXT)
    tmPoint = relationship("PointInteret", back_populates="themes")

class Categorie(Base):
    __tablename__='categories'
    id = Column(Integer, primary_key=True,index=True)
    Nom = Column(TEXT)
    ctPoint = relationship("PointInteret", back_populates="categories")

class Commentaire(Base):
    __tablename__='commentaires'
    id = Column(Integer, primary_key=True,index=True)
    Nom = Column(TEXT)

    point_id = Column(Integer,ForeignKey('points.id'))
    cmPoint = relationship("PointInteret",back_populates='commentaires')

    user_id = Column(Integer, ForeignKey('utilisateurs.id'))
    cmUser = relationship("Utilisateur", back_populates='commentaires')

class MoyenTransport(Base):
    __tablename__='transports'
    id = Column(Integer, primary_key=True,index=True)
    Nom = Column(TEXT)

    mtPoint = relationship("PointInteret",secondary=point_moyen_table, back_populates = 'moyenTransport')

class Utilisateur(Base):
    __tablename__='utilisateurs'
    id = Column(Integer, primary_key=True,index=True)
    UserType = Column(Boolean,default=False)
    Nom = Column(TEXT)
    Email = Column(TEXT)

    favoris = relationship('PointInteret', secondary=user_point_table, back_populates='fans')

    commentaires = relationship("Commentaire", back_populates='cmUser')



class Evenement(Base):
    __tablename__='evenements'
    id = Column(Integer, primary_key = True, index = True)
    Nom = Column(TEXT)
    Description = Column(TEXT)

    Horaire_id = Column(Integer,ForeignKey('horaires.id'))
    horaires = relationship("Horaire",back_populates='hrEvenements')

    point_id = Column(Integer,ForeignKey('points.id'))
    evPoint = relationship("PointInteret",back_populates='evenements')    




