import sqlalchemy
from sqlalchemy import func

import services.vertex
from models import Function, Repo, Branch, Commit, Vertex
import schemas
from services import dao, commit as _commit, changes as _changes
from config import db


def read_all():
    return dao.read_all(Function, schemas.FunctionSchema)


def read(fid):
    return dao.read(fid, Function, schemas.FunctionSchema)


def create(function):
    return dao.create(function, Function, schemas.FunctionSchema, Function.query
                      .filter(Function.name == function.get('name'))
                      .filter(Function.commit_rev_string == function.get('commit_rev_string'))
                      .one_or_none())


def create_or_update_commit(function, commit):
    schema = schemas.FunctionSchema()
    new_function = schema.load(function, session=db.session)

    old_function = Function.query \
        .filter(Function.name == function.get('name')) \
        .filter(Function.parameters == function.get('parameters')) \
        .filter(Function.body == function.get('body')) \
        .one_or_none()

    if old_function is None:
        db.session.add(new_function)
        db.session.commit()
        commit.functions.append(new_function)
        data = schema.dump(new_function)
        return data
    else:
        commit.functions.append(old_function)
        data = schema.dump(old_function)
        return data


def query_function(rev_str, name):
    schema = schemas.FunctionSchema()
    query_result = Function.query \
        .filter(Function.commits.any(rev_string=rev_str)) \
        .filter(Function.name == name) \
        .one_or_none()
    data = schema.dump(query_result)
    return data


def create_or_update_from_graph(function, _rev_string):
    schema = schemas.FunctionSchema()
    new_function = schema.load(function, session=db.session)

    commit = _commit.read_by_rev_string(_rev_string)

    old_function = Function.query \
        .filter(Function.commits.any(rev_string=_rev_string)) \
        .filter(Function.name == function.get('name')) \
        .all()

    if len(old_function) == 0:
        old_function = Function.query \
            .filter(Function.name == function.get('name')) \
            .all()
        if len(old_function) == 0:
            db.session.add(new_function)
            db.session.commit()
            commit.functions.append(new_function)
            return new_function
        else:
            commit.functions.append(old_function[0])
            return old_function[0]
    else:
        commit.functions.append(old_function[0])
        return old_function[0]


def update(fid, function):
    return dao.update(fid, function, Function, schemas.FunctionSchema)


def delete(fid):
    return dao.delete(fid, Function)


def read_all_with_earliest_commit_time_by_repo(rid):
    r = (db.session.query(Function, func.min(Commit.commit_time))
         .select_from(Commit, Branch, Repo)
         .join(Commit.functions)
         .join(Branch, Commit.branch)
         .join(Repo)
         .filter(Repo.id == rid)
         .group_by(Function.id, Function.name)
         .order_by(Function.name, Commit.commit_time)
         .all())
    return r


def read_all_by_repo(rid):
    schema = schemas.FunctionSchema(many=True)
    r = (db.session.query(Function)
         .select_from(Commit, Branch, Repo)
         .join(Commit.functions)
         .join(Branch, Commit.branch)
         .join(Repo)
         .filter(Repo.id == rid)
         .group_by(Function.name)
         .order_by(Function.name)
         .all())
    data = schema.dump(r)
    return data


def read_all_by_repo_extended(rid):
    schema = schemas.FunctionListSchema(many=True)
    q = sqlalchemy.text("""
    SELECT res.name as name, count(res.name) as commit_count, res.parameters as parameters,
        max(res.ct) as last_commit_time, res.rev_string as last_commit_rev, res.body as body
    FROM
        (SELECT f.id, f.name, f.parameters, f.body, min(c.commit_time) as ct, c.rev_string
         FROM function f
             JOIN CommitFunction CF on f.id = CF.function_id
             JOIN "commit" c on CF.commit_rev_string = c.rev_string
             JOIN branch b on b.id = c.branch_id
             JOIN repository r on r.id = b.repo_id
         WHERE r.id = {}
         GROUP BY f.id, CF.function_id, f.name
         ORDER BY f.name, ct) as res
    GROUP BY res.name;
    """.format(rid))
    r = db.session.execute(q)
    # for row in r:
    #     print(row)
    #     print(dict(row))
    data = schema.dump(r)
    # NOTE: Adding this makes everything extremely slow
    # for row in data:
    #     edges = services.vertex.read_around_by_function_name(row['name'])
    #     if len(edges) > 0:
    #         row['has_graph'] = True
    #     else:
    #         row['has_graph'] = False
    return data


def read_all_versions_by_name(name, rid):
    schema = schemas.ExtendedFunctionSchema(many=True)
    r = (db.session.query(Function.id, Function.name, Function.parameters, Function.body, Commit.rev_string,
                          Commit.commit_time, Commit.id.label('commit_id'), func.min(Commit.id))
         .select_from(Commit)
         .join(Commit.functions)
         .join(Branch)
         .join(Repo)
         .filter(Function.name == name)
         .filter(Repo.id == rid)
         .group_by(Function.name, Function.parameters, Function.body)
         .order_by(func.min(Commit.id))
         # .order_by(Commit.id)
         .all())
    data = schema.dump(r)
    # return _changes.get_changes(data)
    return data


def read_by_vertex(vid):
    schema = schemas.FunctionSchema()
    r = (db.session.query(Function)
         .join(Vertex)
         .filter(Vertex.id == vid)
         .one_or_none())
    data = schema.dump(r)
    return data


def read_complete_history(name, rid):
    a = read_all_versions_by_name(name, rid)
    b = _commit.read_all_commits_where_input_edge_changed(name, rid)
    call_list = []
    for c in b:
        rev = c['rev_string']
        cid = c['commit_id']
        d = query_function(rev, name)
        d['commit_rev_string'] = rev
        d['commit_id'] = cid
        # print(d)
        if not any(e['commit_rev_string'] == rev for e in a):
            call_list += [d]
    a = _changes.get_changes(a)
    call_list = _changes.get_changes(call_list, call_only=True)
    result = a + call_list
    return sorted(result, key=lambda item: item['commit_id'])


def read_all_versions_by_vertex(vid, rid):
    f = read_by_vertex(vid)
    return _changes.get_changes(read_all_versions_by_name(f['name'], rid))
