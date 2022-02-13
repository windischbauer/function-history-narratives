from sqlalchemy import UniqueConstraint, Table
from sqlalchemy.orm import relationship

import config

class User(config.db.Model):
    __tablename__ = 'user'
    id = config.db.Column(config.db.Integer, primary_key=True)
    username = config.db.Column(config.db.String(255), nullable=False)
    email = config.db.Column(config.db.String(255), nullable=False)
    commits = relationship('Commit', back_populates='user')

    __table_args__ = (
        UniqueConstraint('username', 'email'),
    )

    def __str__(self):
        return self.email

    def __repr__(self):
        return f'<User(username={self.username!r}, email={self.email!r})>'


class Repo(config.db.Model):
    __tablename__ = 'repository'
    id = config.db.Column(config.db.Integer, primary_key=True)
    path = config.db.Column(config.db.String(255), nullable=False, unique=True)
    branches = relationship('Branch',
                            back_populates='repo',
                            primaryjoin='Repo.id==Branch.repo_id')


class Branch(config.db.Model):
    __tablename__ = 'branch'
    id = config.db.Column(config.db.Integer, primary_key=True)
    name = config.db.Column(config.db.String(255), nullable=False)
    repo_id = config.db.Column(config.db.Integer, config.db.ForeignKey('repository.id'), nullable=False)
    repo = relationship('Repo', back_populates='branches')
    commits = relationship('Commit', back_populates='branch')

    __table_args__ = (
        UniqueConstraint('name', 'repo_id'),
    )


CommitFunction = Table('CommitFunction', config.db.metadata,
                       config.db.Column('commit_rev_string', config.db.ForeignKey('commit.rev_string'), primary_key=True),
                       config.db.Column('function_id', config.db.ForeignKey('function.id'), primary_key=True))


class Commit(config.db.Model):
    __tablename__ = 'commit'
    id = config.db.Column(config.db.Integer, primary_key=True)
    full_message = config.db.Column(config.db.Text)
    commit_time = config.db.Column(config.db.DateTime, nullable=False)
    rev_string = config.db.Column(config.db.String(255), unique=True)
    branch_id = config.db.Column(config.db.Integer, config.db.ForeignKey('branch.id'), nullable=False)
    user_id = config.db.Column(config.db.Integer, config.db.ForeignKey('user.id'), nullable=False)
    branch = relationship('Branch', back_populates='commits')
    user = relationship('User', back_populates='commits')
    snapshots = relationship('Snapshot', back_populates='commit')
    functions = relationship('Function', secondary=CommitFunction,
                             backref=config.db.backref('commits'))


class Snapshot(config.db.Model):
    __tablename__ = 'snapshot'
    id = config.db.Column(config.db.Integer, primary_key=True)
    filename = config.db.Column(config.db.Text, nullable=False)
    content = config.db.Column(config.db.Text)
    edit_list = config.db.Column(config.db.Text)
    commit_id = config.db.Column(config.db.Integer, config.db.ForeignKey('commit.id'), nullable=False)
    commit = relationship('Commit', back_populates='snapshots')


class Function(config.db.Model):
    __tablename__ = 'function'
    id = config.db.Column(config.db.Integer, primary_key=True)
    name = config.db.Column(config.db.String(255), nullable=False)
    parameters = config.db.Column(config.db.Text)
    body = config.db.Column(config.db.Text)
    lineno = config.db.Column(config.db.Integer)
    end_lineno = config.db.Column(config.db.Integer)
    # vertex = relationship('Vertex',
    #                       back_populates='function')


class Vertex(config.db.Model):
    __tablename__ = 'vertex'
    id = config.db.Column(config.db.Integer, primary_key=True)
    function_id = config.db.Column(config.db.Integer, config.db.ForeignKey('function.id'))
    # function = relationship('Function',
    #                         back_populates='vertex')


GraphEdge = Table('GraphEdge', config.db.metadata,
                  config.db.Column('graph_id', config.db.ForeignKey('graph.id'), primary_key=True),
                  config.db.Column('edge_id', config.db.ForeignKey('edge.id'), primary_key=True))


class Edge(config.db.Model):
    __tablename__ = 'edge'
    id = config.db.Column(config.db.Integer, primary_key=True)
    from_ = config.db.Column(config.db.Integer, config.db.ForeignKey('vertex.id'), nullable=False)
    to_ = config.db.Column(config.db.Integer, config.db.ForeignKey('vertex.id'), nullable=False)
    from_vertex = relationship('Vertex',
                               foreign_keys=[from_],
                               primaryjoin="Vertex.id==Edge.from_")
    to_vertex = relationship('Vertex',
                             foreign_keys=[to_],
                             primaryjoin="Vertex.id==Edge.to_"
                             )
    __table_args__ = (
        UniqueConstraint('from_', 'to_'),
    )
    # graphs = relationship('Graph', secondary='graph_edge_table')

# ************** Schemas **************


class Graph(config.db.Model):
    __tablename__ = 'graph'
    id = config.db.Column(config.db.Integer, primary_key=True)
    commit_rev_string = config.db.Column(config.db.String(255), config.db.ForeignKey('commit.rev_string'))
    commit = relationship('Commit')
    edges = relationship('Edge', secondary='GraphEdge',
                         backref=config.db.backref('graphs'))
#
#
# class GraphSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Edge
#         include_relationships = True
#         load_instance = True


# class GraphEdgeTable(config.db.Model):
#     __tablename__ = 'graph_edge_table'
#     graph_id = config.db.Column(config.db.Integer, config.db.ForeignKey('graph.id'), primary_key=True)
#     edge_id = config.db.Column(config.db.Integer, config.db.ForeignKey('edge.id'), primary_key=True)


# class GraphEdgeTableSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Edge
#         include_relationships = True
#         load_instance = True
