import sqlalchemy
from sqlalchemy import literal

from config import db
from models import Vertex, Edge, Function
from schemas import VertexSchema, EdgeSchema, ExtendedEdgeSchema
from services import dao


def read_all():
    return dao.read_all(Vertex, VertexSchema)


def read(vid):
    return dao.read(vid, Vertex, VertexSchema)


def create(vertex):
    return dao.create(vertex, Vertex, VertexSchema, Vertex.query
                      .filter(Vertex.function_id == vertex.get('function_id'))
                      .one_or_none())


def update(vid, vertex):
    return dao.update(vid, vertex, Vertex, VertexSchema)


def delete(vid):
    return dao.delete(vid, Vertex)


def read_around(vid):
    schema = EdgeSchema(many=True)
    # a = (db.session.query(Edge)
    #      .select_from(Vertex, Function)
    #      .join(Vertex, Edge.from_vertex)
    #      .join(Function)
    #      .filter(Function.id == fid)
    #      )
    # b = (db.session.query(Edge)
    #      .select_from(Vertex, Function)
    #      .join(Vertex, Edge.to_vertex)
    #      .join(Function)
    #      .filter(Function.id == fid)
    #      )
    # r = a.union_all(b).all()
    a = (db.session.query(Edge)
         .select_from(Vertex)
         .join(Vertex, Edge.from_vertex)
         .filter(Vertex.id == vid)
         )
    b = (db.session.query(Edge)
         .select_from(Vertex)
         .join(Vertex, Edge.to_vertex)
         .filter(Vertex.id == vid)
         )
    r = a.union_all(b).all()
    data = schema.dump(r)
    return data


def read_previous(vid, commit_rev_string, depth):
    if depth == 0:
        return []
    schema = ExtendedEdgeSchema(many=True)
    q = sqlalchemy.text("""
                            SELECT pid as 'id', pfrom as 'from_', pto as 'to_', f1.name as 'from_name', f2.name as 'to_name'
                            FROM    
                                -- recursive from_
                                (WITH previous AS (
                                    SELECT e.id, e.from_, e.to_, 1 as depth
                                    FROM vertex v 
                                        JOIN edge e on v.id = e.to_
                                        JOIN GraphEdge GE on e.id = GE.edge_id
                                        JOIN graph g on GE.graph_id = g.id
                                    WHERE v.id = {} AND g.commit_rev_string = '{}'
                                    UNION ALL
                                    SELECT ed.id, ed.from_, ed.to_, (previous.depth + 1) as depth
                                    FROM previous, vertex v 
                                        JOIN edge ed on v.id = ed.from_
                                        JOIN GraphEdge GE on ed.id = GE.edge_id
                                        JOIN graph g on GE.graph_id = g.id
                                    WHERE previous.from_ = ed.to_ AND previous.depth < {}
                                )
                                SELECT DISTINCT previous.id as pid, previous.from_ as pfrom, previous.to_ as pto FROM previous)
                                -- adding function names
                                JOIN vertex v1 ON v1.id = pfrom
                                JOIN vertex v2 ON v2.id = pto
                                JOIN function f1 ON v1.function_id = f1.id
                                JOIN function f2 ON v2.function_id = f2.id
                            ORDER BY from_name, to_name;
                        """.format(vid, commit_rev_string, depth))
    r = db.session.execute(q)
    data = schema.dump(r)
    return data


def read_all_previous(vid, commit_rev_string):
    return read_previous(vid, commit_rev_string, 100)


def read_next(vid, commit_rev_string, depth):
    if depth == 0:
        return []
    schema = ExtendedEdgeSchema(many=True)
    q = sqlalchemy.text("""
                            SELECT nid as 'id', nfrom as 'from_', nto as 'to_', f1.name as 'from_name', f2.name as 'to_name'
                            FROM
                                -- recursive to_
                                (WITH next AS (
                                    SELECT e.id, e.from_, e.to_, 1 as depth
                                    FROM vertex v
                                        JOIN edge e on v.id = e.from_
                                        JOIN GraphEdge GE on e.id = GE.edge_id
                                        JOIN graph g on GE.graph_id = g.id
                                    WHERE v.id = {} AND g.commit_rev_string = '{}'
                                    UNION ALL
                                    SELECT ed.id, ed.from_, ed.to_, (next.depth + 1) as depth
                                    FROM next, vertex v 
                                        JOIN edge ed on v.id = ed.from_
                                        JOIN GraphEdge GE on ed.id = GE.edge_id
                                        JOIN graph g on GE.graph_id = g.id
                                    WHERE next.to_ = ed.from_ AND next.depth < {}
                                )
                                SELECT DISTINCT next.id as nid, next.from_ nfrom, next.to_ as nto FROM next)
                                -- adding function names
                                JOIN vertex v1 ON v1.id = nfrom
                                JOIN vertex v2 ON v2.id = nto
                                JOIN function f1 ON v1.function_id = f1.id
                                JOIN function f2 ON v2.function_id = f2.id
                            ORDER BY from_name, to_name;
                        """.format(vid, commit_rev_string, depth))
    r = db.session.execute(q)
    data = schema.dump(r)
    return data


def read_all_next(vid, commit_rev_string):
    return read_next(vid, commit_rev_string, 100)


def read_by_function_id(fid):
    schema = VertexSchema()
    r = (db.session.query(Vertex)
         .join(Function)
         .filter(Function.id == fid)
         .one_or_none())
    data = schema.dump(r)
    return data


def read_all_around(vid, commit_rev_string):
    p = read_all_previous(vid, commit_rev_string)
    n = read_all_next(vid, commit_rev_string)
    res = p + n
    return res


def read_around_with_depth(vid, commit_rev_string, depth):
    p = read_previous(vid, commit_rev_string, depth)
    n = read_next(vid, commit_rev_string, depth)
    res = p + n
    return res


def read_around_by_function_name(fname):
    schema = EdgeSchema(many=True)
    a = (db.session.query(Edge)
         .select_from(Vertex, Function)
         .join(Vertex, Edge.from_vertex)
         .join(Function)
         .filter(Function.name == fname)
         )
    b = (db.session.query(Edge)
         .select_from(Vertex, Function)
         .join(Vertex, Edge.to_vertex)
         .join(Function)
         .filter(Function.name == fname)
         )
    r = a.union_all(b).all()
    data = schema.dump(r)
    return data
