from os import abort, path

import sqlalchemy
from sqlalchemy import func
from werkzeug.exceptions import abort

import schemas
from config import db
from models import Repo, Commit, Branch
from schemas import RepoSchema
from services import dao


def read_all():
    return dao.read_all(Repo, RepoSchema)


def read(rid):
    return dao.read(rid, Repo, RepoSchema)


def _read(rid):
    repo = Repo.query.filter(Repo.id == rid).one_or_none()

    if repo is not None:
        _schema = RepoSchema()
        return repo
    else:
        abort()


def create(repo):
    repo_path = str(repo.get('path'))
    if repo_path.endswith('.git'):
        repo_path = repo_path.removesuffix('.git')
    if repo_path.endswith('/'):
        repo_path = repo_path.removesuffix('/')
    repo['path'] = repo_path
    if not path.exists(repo_path):
        abort(404, f'Path does not exist {repo_path}')
    if not path.exists(repo_path + '/.git'):
        abort(404, f'Path does not contain a repository {repo.get("path")}')
    return dao.create(repo, Repo, RepoSchema, Repo.query
                      .filter(Repo.path == repo.get('path'))
                      .one_or_none())


def update(rid, repo):
    return dao.update(rid, repo, Repo, RepoSchema)


def delete(rid):
    return dao.delete(rid, Repo)


def read_all_extended():
    schema = schemas.ExtendedRepoSchema(many=True)
    q = sqlalchemy.text("""
    SELECT repos.id as id, funcs.path as path, commit_count as commit_count, 
        max(repos.ct) as last_commit_time, func_count as function_count, repos.rev_string as last_commit_rev
    FROM (
             SELECT path, rev_string, count(path) as func_count
             FROM
                 (SELECT r.path, count(c.id), c.rev_string
                  FROM repository r
                           JOIN branch b on r.id = b.repo_id
                           JOIN "commit" c on b.id = c.branch_id
                           JOIN CommitFunction CF on c.rev_string = CF.commit_rev_string
                           JOIN function f on CF.function_id = f.id
                  GROUP BY r.id, f.name)
             GROUP BY path) as funcs
        JOIN
        (
            SELECT r.path, count(c.id) as commit_count, max(c.commit_time) as ct, c.rev_string, r.id
            FROM repository r
                     JOIN branch b on r.id = b.repo_id
                     JOIN "commit" c on b.id = c.branch_id
            GROUP BY r.id
            ) as repos on funcs.path = repos.path
    GROUP BY funcs.path, repos.id
    ORDER BY repos.id;
    """)
    r = db.session.execute(q)
    data = schema.dump(r)

    return data
