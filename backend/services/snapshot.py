import schemas
from config import db
from models import Snapshot, Commit, Function
from schemas import SnapshotSchema
from services import dao


def read_all():
    return dao.read_all(Snapshot, SnapshotSchema)


def read(sid):
    return dao.read(sid, Snapshot, SnapshotSchema)


def create(snapshot):
    return dao.create(snapshot, Snapshot, SnapshotSchema, Snapshot.query
                      .filter(Snapshot.filename == snapshot.get('filename'))
                      .filter(Snapshot.commit_id == snapshot.get('commit_id'))
                      .one_or_none())


def update(sid, snapshot):
    return dao.update(sid, snapshot, Snapshot, SnapshotSchema)


def delete(sid):
    return dao.delete(sid, Snapshot)


def read_by_commit_rev(commit_rev_string):
    schema = schemas.SnapshotSchema(many=True)
    r = (db.session.query(Snapshot)
         .join(Commit)
         .filter(Commit.rev_string == commit_rev_string)
         .all())
    data = schema.dump(r)
    return data


def read_by_commit_and_file_and_fname(commit_rev_string, filename, func_name):
    schema = schemas.ExtendedSnapshotSchema()
    q = (db.session.query(Snapshot.id,
                          Snapshot.commit_id,
                          Snapshot.commit,
                          Snapshot.content,
                          Snapshot.edit_list,
                          Snapshot.filename,
                          Function.lineno,
                          Function.end_lineno)
         .join(Commit)
         .join(Function, Commit.functions)
         .filter(Commit.rev_string == commit_rev_string)
         .filter(Snapshot.filename.ilike(f'%{filename}%'))
         .filter(Function.name == func_name)
         .all())
    data = schema.dump(q[0] if len(q) >= 1 else None)
    return data
