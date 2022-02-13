from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

import models

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = models.User
        interfaces = (relay.Node, )


class RepoType(SQLAlchemyObjectType):
    class Meta:
        model = models.Repo
        interfaces = (relay.Node, )


class BranchType(SQLAlchemyObjectType):
    class Meta:
        model = models.Branch
        interfaces = (relay.Node, )


class CommitType(SQLAlchemyObjectType):
    class Meta:
        model = models.Commit
        interfaces = (relay.Node, )


class SnapshotType(SQLAlchemyObjectType):
    class Meta:
        model = models.Snapshot
        interfaces = (relay.Node, )


class FunctionType(SQLAlchemyObjectType):
    class Meta:
        model = models.Function
        interfaces = (relay.Node, )


class VertexType(SQLAlchemyObjectType):
    class Meta:
        model = models.Vertex
        interfaces = (relay.Node, )


class EdgeType(SQLAlchemyObjectType):
    class Meta:
        model = models.Edge
        interfaces = (relay.Node, )


class GraphType(SQLAlchemyObjectType):
    class Meta:
        model = models.Graph
        interfaces = (relay.Node, )

