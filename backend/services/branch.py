from models import Branch
from schemas import BranchSchema
from services import dao


def read_all():
    return dao.read_all(Branch, BranchSchema)


def read(bid):
    return dao.read(bid, Branch, BranchSchema)


def create(branch):
    print(branch)
    return dao.create(branch, Branch, BranchSchema, Branch.query 
                      .filter(Branch.name == branch.get('name')) 
                      .filter(Branch.repo_id == branch.get('repo_id')) 
                      .one_or_none())


def update(bid, branch):
    return dao.update(bid, branch, Branch, BranchSchema)


def delete(bid):
    return dao.delete(bid, Branch)
