import forms


def all():
    """
    json response of available interviewers
    :return:
    """
    return 'This is news'


def get(obj_id):
    """
    retrieves interviewer record matching obj_id
    :param obj_id:
    :return:
    """

    return


def create(*args, **kwargs):
    """
    creates new interviewer record
    :param args:
    :param kwargs:
    :return:
    """
    form = forms.InterviewForm()


def delete(obj_id):
    """
    deletes interviewer record matching obj_id
    :param obj_id:
    :return:
    """
    pass


def update(obj_id, *args, **kwargs):
    """
    updates interviewer record matching obj_id with data in request body
    :param obj_id:
    :param args:
    :param kwargs:
    :return:
    """
    pass