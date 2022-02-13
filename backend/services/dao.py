from flask import make_response
from werkzeug.exceptions import abort

from config import db
import models
import schemas


def read_all(model, schema):
    # Create list of entities from our data
    entities = model.query.order_by(model.id).all()
    # Serialize the data for the response
    _schema = schema(many=True)
    data = _schema.dump(entities)
    return data


def read(oid, model, schema):
    entity = model.query.filter(model.id == oid).one_or_none()

    if entity is not None:
        _schema = schema()
        return _schema.dump(entity), 200
    else:
        abort(404, f'Object not found for id {oid}')


def create(obj, model, schema, filter, internal=False):

    _schema = schema()
    new_entity = _schema.load(obj, session=db.session)

    old_entity = filter

    if old_entity is None:
        db.session.add(new_entity)
        db.session.commit()
        # Serialize and return the newly created person in the response
        if internal:
            return new_entity
        else:
            data = _schema.dump(new_entity)
            return data, 201
    else:
        if internal:
            return old_entity
        else:
            data = _schema.dump(old_entity)
            return data, 409


def update(oid, obj, model, schema):
    old_entity = model.query.filter(model.id == oid).one_or_none()

    if old_entity is not None:
        _schema = schema()
        new_entity = _schema.load(obj, session=db.session)
        # Set id of updated function
        new_entity.id = old_entity.id
        # Merge/Update function in database
        db.session.merge(new_entity)
        db.session.commit()
        # Serialize and return the newly created person in the response
        data = _schema.dump(new_entity)
        return data, 200
    else:
        abort(404, f'Object not found for id {oid}')


def delete(oid, model):
    entity = model.query.filter(model.id == oid).one_or_none()

    if entity is not None:
        db.session.delete(entity)
        db.session.commit()
        return make_response(f'Object {entity.id} deleted', 200)
    else:
        abort(404, f'Object not found for id {oid}')
