from sqlalchemy import Column,Integer,String,ForeignKey,Boolean,TEXT,DateTime,Table, Float
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
    id = Column(Integer, primary_key=True,index=True)
    Nom = Column(String)
    Description = Column(TEXT)
    Wilaya = Column(String)
    Region = Column(String)
    DateOuverture = Column(DateTime)
    DateFermeture = Column(DateTime)

    Latitude = Column(Float)
    Longitude = Column(Float)

    #Lieu_id = Column(Integer,ForeignKey('lieux.id'))
    #lieu = relationship("Lieu", back_populates='points')

    commentaires = relationship("Commentaire",back_populates='cmPoint')

    moyenTransport = relationship("MoyenTransport", secondary=point_moyen_table, back_populates ='mtPoint')
    
    evenements = relationship("Evenement", back_populates='evPoint')

    Theme_id = Column(Integer,ForeignKey('themes.id'))
    themes = relationship("Theme",back_populates='tmPoint')

    Categorie_id = Column(Integer,ForeignKey('categories.id'))
    categories = relationship("Categorie",back_populates='ctPoint')

    fans = relationship('Utilisateur', secondary=user_point_table, back_populates='favoris')

'''   
class Lieu(Base):
    __tablename__='lieux'
    id = Column(Integer, primary_key=True,index=True)
    Nom = Column(String)
    Description = Column(TEXT)

    points = relationship("PointInteret", back_populates='lieu')
'''

class Theme(Base):
    __tablename__='themes'
    id = Column(Integer, primary_key=True,index=True)
    Nom = Column(String)
    tmPoint = relationship("PointInteret", back_populates="themes")


class Categorie(Base):
    __tablename__='categories'
    id = Column(Integer, primary_key=True, index=True)
    Nom = Column(String)
    ctPoint = relationship("PointInteret", back_populates="categories")


class Commentaire(Base):
    __tablename__='commentaires'
    id = Column(Integer, primary_key=True,index=True)
    Content = Column(TEXT)

    point_id = Column(Integer,ForeignKey('points.id'))
    cmPoint = relationship("PointInteret",back_populates='commentaires')

    user_id = Column(Integer, ForeignKey('utilisateurs.id'))
    cmUser = relationship("Utilisateur", back_populates='commentaires')


class MoyenTransport(Base):
    __tablename__='transports'
    id = Column(Integer, primary_key=True,index=True)
    Type = Column(String)

    mtPoint = relationship("PointInteret",secondary=point_moyen_table, back_populates = 'moyenTransport')


class Utilisateur(Base):
    __tablename__='utilisateurs'
    id = Column(Integer, primary_key=True,index=True)
    UserType = Column(Boolean,default=False)
    #token = Column(TEXT)
    Nom = Column(String)
    Email = Column(String, unique=True)
    HashedPassword = Column(String)

    favoris = relationship('PointInteret', secondary=user_point_table, back_populates='fans')

    commentaires = relationship("Commentaire", back_populates='cmUser')

    notifications = relationship("Notification", back_populates='user_notifications')


class Evenement(Base):
    __tablename__ = 'evenements'
    id = Column(Integer, primary_key = True, index = True)
    Nom = Column(String)
    Description = Column(TEXT)
    DateDebut = Column(DateTime)
    DateFin = Column(DateTime)

    point_id = Column(Integer,ForeignKey('points.id'))
    evPoint = relationship("PointInteret", back_populates='evenements')  


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    Content = Column(TEXT)
    Read = Column(Boolean)

    user_id = Column(Integer, ForeignKey('utilisateurs.id'))
    user_notifications = relationship("Utilisateur", back_populates='notifications')