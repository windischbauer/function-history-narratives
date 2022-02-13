import schemas
from config import db
from models import User, Commit, Branch, Repo
from schemas import UserSchema
from services import dao


def read_all():
    return dao.read_all(User, UserSchema)


def read(uid):
    return dao.read(uid, User, UserSchema)


def read_all_by_repo(rid):
    schema = schemas.UserSchema(many=True)
    q = (db.session.query(User)
         .join(User, Commit.user)
         .join(Branch)
         .join(Repo)
         .filter(Repo.id == rid)
         .group_by(User.id)
         .all())
    data = schema.dump(q)
    return data


def create(user):
    return dao.create(user, User, UserSchema, User.query
                      .filter(User.username == user.get('username'))
                      .filter(User.email == user.get('email'))
                      .one_or_none())


def update(uid, user):
    return dao.update(uid, user, User, UserSchema)


def delete(uid):
    return dao.delete(uid, User)
