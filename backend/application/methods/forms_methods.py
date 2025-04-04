from sqlalchemy.orm import joinedload

from application import FormCategory
from application.models import Form, Submission, db
from application.helpers.exceptions import LogicException
from application.helpers.decorators import transaction


def get_form_by_id(form_id):
    form = Form.query.filter_by(id=form_id, deleted_at=None).first()
    if not form:
        raise LogicException("Форма не найдена", 404)
    return form


def get_forms():
    return Form.query.filter_by(deleted_at=None).all()


def get_form_categories():
    return FormCategory.query.filter_by(deleted_at=None).all()


def get_category_by_id(category_id):
    category = FormCategory.query.filter_by(id=category_id, deleted_at=None).first()

    if not category:
        raise LogicException("Категория не найдена", 404)

    return category


@transaction
def create_form(user, category, data):
    new_form = Form(
        name=data["name"],
        available_params=data.get("available_params", []),
        fields=data.get("fields", []),
        creator_id=user.id,
        category_id=category.id
    )
    db.session.add(new_form)
    return new_form


@transaction
def update_form(form, data):
    form.name = data.get("name", form.name)
    form.available_params = data.get("available_params", form.available_params)
    form.fields = data.get("fields", form.fields)
    return form


@transaction
def delete_form(user, form):
    form.deleted_at = db.func.now()
    form.deleter_id = user.id


def get_submission_by_id(sub_id):
    sub = Submission.query.filter_by(id=sub_id).first()
    if not sub:
        raise LogicException("Ответ не найден", 404)
    return sub


def get_object_submissions(object):
    return (
        db.session.query(Submission)
        # Подгружаем связанные данные:
        .options(
            joinedload(Submission.form).joinedload(Form.category)
        )
        .filter(
            Submission.object_id == object.id
        )
        .all()
    )


def get_form_submissions(form):
    return (
        db.session.query(Submission)
        # Подгружаем связанные данные:
        .options(
            joinedload(Submission.object)
        )
        .filter(
            Submission.form_id == form.id,
            Submission.deleted_at.is_(None)
        )
        .all()
    )


@transaction
def create_submission(user, form, object, data):
    new_submission = Submission(
        form_id=form.id,
        object_id=object.id,
        params=data.get("params", {}),
        fields=data.get("fields", {}),
        showoff_attributes=data.get("showoff_attributes", {}),
        creator_id=user.id,
        form_name=form.name,
        form_category_name=form.category.name,
        is_approved=user.role != 'student'
    )
    db.session.add(new_submission)

    if not new_submission.is_approved:
        object.has_unapproved_submissions = True
        print("set unapproved")

    return new_submission


@transaction
def update_submission(submission, data):
    submission.params = data.get("params", submission.params)
    submission.fields = data.get("fields", submission.fields)
    submission.showoff_attributes = data.get("showoff_attributes", submission.showoff_attributes)
    return submission


def check_changes_in_submission(submission, data):
    if submission.params != data.get("params"):
        return True
    if submission.fields != data.get("fields"):
        return True
    if submission.showoff_attributes != data.get("showoff_attributes"):
        return True
    return False


@transaction
def deapprove_submission(submission):
    from application.presenters.presenters import present_submission

    if submission.is_approved:
        submission.backup = present_submission(submission)

    submission.is_approved = False
    submission.object.has_unapproved_submissions = True


@transaction
def delete_submission(user, submission):
    submission.deleted_at = db.func.now()
    submission.deleter_id = user.id

    if all(submission.is_approved for submission in submission.object.submissions if not submission.deleted_at):
        submission.object.has_unapproved_submissions = False


@transaction
def approve_submission(user, submission):
    submission.is_approved = True
    submission.approved_by = user

    if all(submission.is_approved for submission in submission.object.submissions if not submission.deleted_at):
        submission.object.has_unapproved_submissions = False

    return submission


@transaction
def restore_submission(submission):
    if submission.backup:
        submission.fields = submission.backup["fields"]
        submission.params = submission.backup["params"]
        submission.showoff_attributes = submission.backup["showoff_attributes"]
        submission.is_approved = True
        submission.deleted_at = None
        submission.deleter_id = None

    return submission
