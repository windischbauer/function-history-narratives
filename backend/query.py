import graphene
from graphene import relay, Field, NonNull, List, String
from graphene.utils.str_converters import to_snake_case
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphql_relay.connection.arrayconnection import connection_from_list_slice
from graphql_relay.connection.connectiontypes import PageInfo
from sqlalchemy import asc, desc

import gqltypes


ORDER_FUNCTIONS = {'asc': asc, 'desc': desc}


class InstrumentedQuery(SQLAlchemyConnectionField):
    def __init__(self, type, **kwargs):
        self.query_args = {}
        for k, v in type._meta.fields.items():
            if isinstance(v, Field):
                field_type = v.type
                if isinstance(field_type, NonNull):
                    field_type = field_type.of_type
                self.query_args[k] = field_type()
        args = kwargs.pop('args', dict())
        args.update(self.query_args)
        args['sort_by'] = List(String, required=False)
        super().__init__(type, args=args, **kwargs)

    def get_query(self, model, info, **args):
        query_filters = {k: v for k, v in args.items() if k in self.query_args}
        query = model.query.filter_by(**query_filters)
        if 'sort_by' in args:
            criteria = [self.get_order_by_criterion(model, *arg.split(' ')) for arg in args['sort_by']]
            query = query.order_by(*criteria)
        return query

    def connection_resolver(self, resolver, connection, model, root, info, **args):
        query = resolver(root, info, **args) or self.get_query(model, info, **args)
        count = query.count()
        connection = connection_from_list_slice(
            query,
            args,
            slice_start=0,
            list_length=count,
            list_slice_length=count,
            connection_type=connection,
            pageinfo_type=PageInfo,
            edge_type=connection.Edge,
        )
        connection.iterable = query
        connection.length = count
        return connection

    @staticmethod
    def get_order_by_criterion(model, name, direction='asc'):
        return ORDER_FUNCTIONS[direction.lower()](getattr(model, to_snake_case(name)))


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(gqltypes.UserType.connection)
    all_repos = SQLAlchemyConnectionField(gqltypes.RepoType)
    all_branches = SQLAlchemyConnectionField(gqltypes.BranchType.connection)
    all_commits = SQLAlchemyConnectionField(gqltypes.CommitType.connection)
    all_snapshots = SQLAlchemyConnectionField(gqltypes.SnapshotType.connection)
    all_functions = SQLAlchemyConnectionField(gqltypes.FunctionType.connection)
    all_vertices = SQLAlchemyConnectionField(gqltypes.VertexType.connection)
    all_edges = SQLAlchemyConnectionField(gqltypes.EdgeType.connection)
    all_graphs = SQLAlchemyConnectionField(gqltypes.GraphType.connection)

    user = InstrumentedQuery(gqltypes.UserType)
    repo = InstrumentedQuery(gqltypes.RepoType)
    branch = InstrumentedQuery(gqltypes.BranchType)
    commit = InstrumentedQuery(gqltypes.CommitType)
    snapshot = InstrumentedQuery(gqltypes.CommitType)
    function = InstrumentedQuery(gqltypes.FunctionType)
    vertex = InstrumentedQuery(gqltypes.VertexType)
    edge = InstrumentedQuery(gqltypes.EdgeType)
    graph = InstrumentedQuery(gqltypes.GraphType)



schema = graphene.Schema(query=Query)
