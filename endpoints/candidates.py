from flask import jsonify

import connexion

from app import forms, models, InvalidUsage

from services import common


def all():
    """
    json response of available interviewers
    :return:
    """
    url_params = connexion.request.args
    page = url_params.get('page', 0)
    limit = url_params.get('limit', 20)
    return jsonify([c.serialize() for c in models.Candidate.query.offset(page).limit(limit).all()])


def get(obj_id):
    """
    retrieves candidate record matching obj_id
    :param obj_id:
    :return:
    """
    candidate = models.Candidate.query.get(obj_id)

    if not candidate:
        raise InvalidUsage("Candidate not found matching id - %s" % obj_id, status_code=404)

    return jsonify(candidate.serialize())


def create(**kwargs):
    """
    creates new candidate record
    :param kwargs:
    :return:
    """
    request_data = kwargs.get('data')
    form = forms.CreateForm(csrf_enabled=False, obj=request_data)

    if form.validate_on_submit():

        if models.Candidate.query.filter_by(email=form.email.data).first():
            raise InvalidUsage("Candidate with email address already - %s exists" % form.email.data, status_code=400)

        candidate = models.Candidate()
        form.populate_obj(candidate)
        models.db.session.add(candidate)
        models.db.session.commit()
        return jsonify({"message": "Candidate with id - %s created" % candidate.id})

    raise InvalidUsage(form.errors, status_code=422)


def delete(obj_id):
    """
    deletes candidate record matching obj_id
    :param obj_id:
    :return:
    """
    candidate = models.Candidate.query.get(obj_id)

    if not candidate:
        raise InvalidUsage("Candidate not found matching id - %s" % obj_id, status_code=404)

    models.db.session.delete(candidate)
    models.db.session.commit()

    return common.success_response("Candidate successfully deleted", 204)


def update(obj_id, **kwargs):
    """
    updates candidate record matching obj_id with data in request body
    :param obj_id:
    :param args:
    :param kwargs:
    :return:
    """
    candidate = models.Candidate.query.get(obj_id)

    if not candidate:
        raise InvalidUsage("Candidate not found matching id - %s" % obj_id, status_code=404)

    request_data = kwargs.get('data')
    form = forms.UpdateForm(csrf_enabled=False, obj=request_data)

    if form.validate_on_submit():
        common.populate_object(candidate, **request_data)
        models.db.session.add(candidate)
        models.db.session.commit()
        return common.success_response({"message": "Candidate with id - %s successfully updated" % candidate.id}, 201)

    raise InvalidUsage(form.errors, status_code=422)