import marshmallow.fields

from config import ma
from models import User, Repo, Branch, Commit, Snapshot, Function, Vertex, Edge, Graph


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = False
        load_instance = True


class RepoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Repo
        include_relationships = True
        load_instance = True


ExtendedRepoSchema = type('ExtendedRepoSchema',
                          (RepoSchema,),
                          {'commit_count': marshmallow.fields.Integer(attribute='commit_count', dump_only=True),
                           'last_commit_time': marshmallow.fields.String(attribute='last_commit_time',
                                                                         dump_only=True),
                           'last_commit_rev': marshmallow.fields.String(attribute='last_commit_rev'),
                           'function_count': marshmallow.fields.Integer(attribute='function_count', dump_only=True)})


class BranchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Branch
        include_relationships = True
        include_fk = True
        load_instance = True


class CommitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Commit
        include_relationships = False
        include_fk = True
        load_instance = True


class SnapshotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Snapshot
        include_relationships = True
        include_fk = True
        load_instance = True


ExtendedSnapshotSchema = type('ExtendedSnapshotSchema',
                              (SnapshotSchema,),
                              {'lineno': marshmallow.fields.Integer(attribute='lineno', dump_only=True),
                               'end_lineno': marshmallow.fields.Integer(attribute='end_lineno', dump_only=True)})


class FunctionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Function
        include_relationships = False
        include_fk = True
        load_instance = True


ExtendedFunctionSchema = type('ExtendedFunctionSchema',
                              (FunctionSchema,),
                              {'commit_rev_string': marshmallow.fields.String(attribute='rev_string', dump_only=True),
                               'commit_id': marshmallow.fields.Integer(attribute='commit_id', dump_only=True)})

FunctionListSchema = type(
    'FunctionListSchema',
    (FunctionSchema,),
    {'commit_count': marshmallow.fields.Integer(attribute='commit_count', dump_only=True),
     'last_commit_time': marshmallow.fields.String(attribute='last_commit_time', dump_only=True),
     'last_commit_rev': marshmallow.fields.String(attribute='last_commit_rev', dump_only=True)})


class VertexSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vertex
        include_relationships = True
        include_fk = True
        load_instance = True


class EdgeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Edge
        include_relationships = False
        include_fk = True
        load_instance = True


ExtendedEdgeSchema = type('ExtendedEdgeSchema',
                          (EdgeSchema,),
                          {'from_name': marshmallow.fields.String(attribute='from_name', dump_only=True),
                           'to_name': marshmallow.fields.String(attribute='to_name', dump_only=True)})


class GraphSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Graph
        include_relationships = True
        include_fk = True
        load_instance = True
