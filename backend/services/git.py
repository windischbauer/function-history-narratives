from git import Repo
import ast

from tqdm.contrib import tenumerate

from models import Commit
from services import repo as _repo
from services import branch as _branch
from services import commit as _commit
from services import user as _user
from services import snapshot as _snapshot
from services import function as _function


def start(path):
    """
    Takes a path to a repository. Iterates through branches, commits, snapshots and users
    and commits them to the database. Files without the ending '.py' will be ignored.

    :param path: a json object containing only 'path'
    """

    # Creates repo if not exists and gets repo id
    repo = _repo.create(path)
    _repo_id = repo[0].get('id')
    _path = path.get('path')

    # Fetches the repository object via the repo path
    repository = Repo(_path)
    print(repository)

    # Iterates through the locally existing branches
    branches = repository.heads
    head = branches[0]

    # Can be added in the future but there is no logic to accommodate querying with multiple branches right now
    # Simply change head to branch
    # for branch in branches:
    print(head.name)

    # Creates branch if not exists and gets the branch id
    _branch_id = _branch.create({
        'name': head.name,
        'repo_id': _repo_id
    })[0].get('id')

    _user_id = None
    _username = None
    _email = None
    previous_commit = None
    commits = list(repository.iter_commits(rev=head, reverse=True))
    # Iterate through commits
    for i, commit in tenumerate(commits, total=len(commits), desc=f'Repo Progress'):
        try:
            repository.git.checkout(commit)

            # Create user if not exists and get user id
            if _username != commit.author.name and _email != commit.author.email:
                _username = commit.author.name
                _email = commit.author.email
                _user_id = _user.create({
                    'username': _username,
                    'email': _email
                })[0].get('id')

            _commit_time = str(commit.committed_datetime)[:-6]
            res = Commit.query.filter(Commit.rev_string == str(commit)).one_or_none()
            if res is not None:
                continue

            # Create commit if not exists and get commit id
            created_commit = _commit.create_internal({
                'full_message': commit.message,
                'commit_time': _commit_time,
                'rev_string': str(commit),
                'branch_id': _branch_id,
                'user_id': _user_id
            })
            _commit_id = created_commit.id
            _commit_rev_str = created_commit.rev_string

            # Get changed files
            changes = repository.index.diff(previous_commit)

            stack = [commit.tree]
            while len(stack) > 0:
                tree = stack.pop()
                # enumerate blobs (files) at this level
                # FIXME: no need to iterate over all files; just save the changed files
                #  This saves storage and consumes less time
                for b in tree.blobs:
                    # data is 'utf-8' encoded
                    if not b.path.endswith('.py'):
                        continue
                    if previous_commit is not None:
                        if not any(diff.a_path == b.path for diff in changes):
                            continue
                    # print(f'Committing {b.path} to the database')

                    data = b.data_stream.read()

                    _snapshot_id = _snapshot.create({
                        'filename': b.path,
                        'content': data.decode('utf-8'),
                        'edit_list': 'temporarily null',
                        'commit_id': _commit_id
                    })

                    content = _snapshot_id[0].get('content')
                    filename = _snapshot_id[0].get('filename')
                    try:
                        ast_tree = ast.parse(content)
                        # print(ast.dump(ast_tree, indent=3))
                        # Iterate over tree elements
                        for node in ast_tree.body:
                            if isinstance(node, ast.FunctionDef):
                                name_prefix = str(filename).removesuffix('py').replace('/', '.')
                                add_body(name_prefix=name_prefix,
                                         function=node,
                                         commit_rev_str=_commit_rev_str,
                                         commit=created_commit,
                                         lineno=node.lineno,
                                         end_lineno=node.end_lineno)

                            if isinstance(node, ast.ClassDef):
                                name_prefix = str(filename).removesuffix('py').replace('/', '.') + str(node.name) + '.'

                                for f in node.body:
                                    if isinstance(f, ast.FunctionDef):
                                        add_body(name_prefix=name_prefix,
                                                 function=f,
                                                 commit_rev_str=_commit_rev_str,
                                                 commit=created_commit,
                                                 lineno=f.lineno,
                                                 end_lineno=f.end_lineno)
                    except SyntaxError:
                        pass
                for subtree in tree.trees:
                    stack.append(subtree)

            previous_commit = commit
        except Exception as e:
            repository.git.checkout(head)
    repository.git.checkout(head)
    return repo


def add_body(name_prefix, function, commit_rev_str, commit, lineno, end_lineno):
    func_bod = ''
    for obj in function.body:
        func_bod += str(ast.dump(obj)) + '\n'

    func = _function.create_or_update_commit({
        'name': name_prefix + str(function.name),
        'parameters': str(ast.dump(function.args)),
        'body': func_bod,
        'lineno': lineno,
        'end_lineno': end_lineno
        # 'commit_rev_string': commit_rev_str
    }, commit)

# TODO: Diffing files can be done separately by searching for the filename,
#  grouping by their file name and sorting descending by their commit date.
#  This does not need to be done initially and could possibly done while
#  simultaneously generating call graphs
