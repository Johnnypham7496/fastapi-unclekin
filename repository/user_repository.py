from sqlalchemy.orm.session import Session
from db.user_db import Userdb


def get_all_users(db: Session):
    return db.query(Userdb).all()


def add_user(db: Session, _username, _email, _role):
    new_user = Userdb(username=_username, email=_email, role=_role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_by_username(db: Session, _username):
    query = db.query(Userdb).filter(Userdb.username==_username).first()
    return query


def add_user_td(db: Session):
    add_user(db, "darth.vader", "darth.vader@gmail.com", "villian")
    add_user(db, "bruce.wayne", "batman@gmail.com", "hero")
    add_user(db, "captain.america", "captain.america@gmail.com", "hero")