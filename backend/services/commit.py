import sqlalchemy
from sqlalchemy import func

import schemas
from config import db
from models import Commit, Function, Graph, Vertex, Branch, Repo
from schemas import CommitSchema, RepoSchema, BranchSchema
from services import dao, vertex as _vertex, function as _function


def read_all():
    return dao.read_all(Commit, CommitSchema)


def read(cid):
    return dao.read(cid, Commit, CommitSchema)


def read_by_repo(rid):
    commits = Commit.query.filter()


# The resulting entity is directly used by function.create_or_update_from_graph
# so this should absolutely not be changed
def read_by_rev_string(rev_string):
    q = Commit.query \
        .filter(Commit.rev_string == rev_string) \
        .one_or_none()
    return q


def read_all_commits_from_function_name(function_name, rid):
    schema = CommitSchema(many=True)
    r = (db.session.query(Commit)
         .select_from(Function)
         .join(Commit.functions)
         .join(Branch)
         .join(Repo)
         .filter(Function.name == function_name)
         .filter(Repo.id == rid)
         .group_by(Function.body, Function.parameters)
         .order_by(func.min(Commit.id))
         .all())
    data = schema.dump(r)
    return data


def read_complete_commit_history(function_name, rid):
    a = read_all_commits_from_function_name(function_name, rid)
    b = read_all_commits_where_input_edge_changed(function_name, rid)
    for c in b:
        rev = c['rev_string']
        schema = schemas.CommitSchema()
        d = schema.dump(read_by_rev_string(rev))
        if not any(e['rev_string'] == rev for e in a):
            a += [d]
    return a


def read_all_commits_where_input_edge_changed(name, rid):
    q = (db.session.query(Graph.id.label('gid'), Vertex.id.label('vid'), Function.name, Graph.commit_rev_string,
                          Commit.id.label('commit_id'))
         .select_from(Commit)
         .join(Commit.functions)
         .join(Vertex)
         .join(Graph)
         .join(Branch)
         .join(Repo)
         .filter(Function.name == name)
         .filter(Repo.id == rid)
         .order_by(Commit.id, Vertex.id)
         .all())

    res = list()
    previous = list()
    first = True

    for row in q:

        vid = row['vid']
        rev = row['commit_rev_string']
        cid = row['commit_id']
        r = _vertex.read_previous(vid, rev, 1)

        if len(r) == 0:
            continue

        for i in r:
            del i['from_']
            del i['to_']
            del i['id']

        if first:
            first = False
            res += [{'rev_string': f'{rev}', 'commit_id': cid}]
            previous = r
            continue

        if __compare(previous[0], r[0]):
            continue

        res += [{'rev_string': f'{rev}', 'commit_id': cid}]
        previous = r
    return res


def read_all_commits_by_vertex_and_repo(vid, rid):
    f = _function.read_by_vertex(vid)
    return read_all_commits_from_function_name(f['name'], rid)


def __compare(a, b):
    if a.get('to_name') != b.get('to_name'):
        return False
    if a.get('from_name') != b.get('from_name'):
        return False
    return True


def create(commit):
    return dao.create(commit, Commit, CommitSchema, Commit.query
                      .filter(Commit.rev_string == commit.get('rev_string'))
                      .one_or_none())


def create_internal(commit):
    return dao.create(commit, Commit, CommitSchema, Commit.query
                      .filter(Commit.rev_string == commit.get('rev_string'))
                      .one_or_none(), internal=True)


def update(cid, commit):
    return dao.update(cid, commit, Commit, CommitSchema)


def delete(cid):
    return dao.delete(cid, Commit)
