import json
import subprocess
import sys
from tqdm import tqdm
from tqdm.contrib import tenumerate

from models import Graph
from schemas import GraphSchema
from services import repo as _repo, function as _function, edge as _edge, vertex as _vertex, commit as _commit, snapshot as _snapshot, dao
from git import Repo

cache = dict()  # might use at a later stage


def read(rid):
    return dao.read(rid, Graph, GraphSchema)


def create_or_skip(graph):
    res = Graph.query \
        .filter(Graph.commit_rev_string == graph.get('commit_rev_string')) \
        .one_or_none()
    if res is None:
        return dao.create(graph, Graph, GraphSchema, res, internal=True)
    else:
        return 1


# PyCG cannot deal with whitespace in path
def start(rid):
    path = _repo.read(rid)[0].get('path')
    print('Starting to generate call graphs for: ')
    print(path)
    iterate_through_revisions(path)


def iterate_through_revisions(path, start=0, count=sys.maxsize):
    repository = Repo(path)
    print(f'This is the active repository: {repository}')

    # Iterates through the locally existing branches
    branches = repository.heads
    head = branches[0]

    # Can be added in the future but there is no logic to accommodate querying with multiple branches right now
    # Simply change head to branch
    # for branch in branches:

    print(f'This is the initial branch: {head.name}')
    commits = list(repository.iter_commits(rev=head, reverse=True))
    total = min(count, len(commits))

    for i, commit in tenumerate(commits, total=total, desc=f'Branch progress'):
        if i < start:
            continue
        elif i >= start + count:
            break

        # Checks if the commit has relevant files changed, otherwise there is no need to create a graph
        if len(_snapshot.read_by_commit_rev(str(commit))) == 0:
            continue

        # print(f'This is the commit: {commit}')
        try:
            repository.git.checkout(commit)
            # print(f'This is the new active branch: {repository.active_branch}')

            graph = create_or_skip({'commit_rev_string': str(commit)})
            if graph != 1:
                response = subprocess.check_output('pycg --package ' + path +
                                                   ' $(find ' + path + ' -type f -name "*.py")', shell=True)
                parse(response, str(commit), graph)

        except Exception as e:
            repository.git.checkout(head)

    repository.git.checkout(head)


def parse(response, commit, _graph):
    graph = json.loads(response.decode('utf-8'))
    # print('*********************** START OUTPUT ***********************')
    # # Prints the whole graph
    # print(response)
    # # print(graph.get(1))
    # print('*********************** END OUTPUT ***********************')
    for edge in tqdm(graph, desc=f'Commit {str(commit)} progress'):
        f = _function.create_or_update_from_graph({'name': edge}, commit)
        v = _vertex.create({'function_id': f.id})

        function_list = graph[edge]
        if len(function_list) > 0:
            # print(f'from:{edge} -> to:{function_list}')
            for function in function_list:
                # print(f'from:{edge} -> to:{function} \tfor graph:{_graph}')
                f2 = _function.create_or_update_from_graph({'name': function}, commit)
                v2 = _vertex.create({'function_id': f2.id})
                e = _edge.create({'from_': v[0].get('id'), 'to_': v2[0].get('id')}, _graph)
        else:
            # print(f'from:{edge} -> to:{function_list}')
            pass
