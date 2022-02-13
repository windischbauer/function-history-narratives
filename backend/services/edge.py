from config import db
from models import Edge
from schemas import EdgeSchema
from services import dao


def read_all():
    return dao.read_all(Edge, EdgeSchema)


def read(eid):
    return dao.read(eid, Edge, EdgeSchema)


def create(edge, graph):
    e = dao.create(edge, Edge, EdgeSchema, Edge.query
                   .filter(Edge.from_ == edge.get('from_'))
                   .filter(Edge.to_ == edge.get('to_'))
                   .one_or_none(), internal=True)
    graph.edges.append(e)
    db.session.commit()
    return e


def update(eid, edge):
    return dao.update(eid, edge, Edge, EdgeSchema)


def delete(eid):
    return dao.delete(eid, Edge)
