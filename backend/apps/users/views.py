from http import HTTPStatus

from flask import (
    Response,
    request,
    url_for,
)

from flask_jwt_extended import (
    current_user,
    jwt_required,
)
from sqlalchemy.orm.exc import NoResultFound

from apps.common.views import APIView

from ..extensions import db
from . import (
    models,
    schemas,
)


class UserCreateView(APIView):
    def post(self) -> Response:
        user = schemas.UserSchema().load(request.json)
        db.session.add(user)
        db.session.commit()
        return Response(
            schemas.UserSchema(exclude=('password',)).dumps(user),
            HTTPStatus.CREATED,
            headers={
                'Location': url_for('.user-detail', user_id=str(user.id)),
                'Content-Type': 'application/json',
            },
        )


class UserRetrieveView(APIView):
    method_decorators = [jwt_required]

    def get(self, user_id: str) -> Response:
        if user_id == 'self':
            user = current_user
        else:
            try:
                user = models.User.query.get(user_id)
            except NoResultFound:
                raise
        return Response(
            schemas.UserSchema().dumps(user),
            HTTPStatus.OK,
            headers={'Content-Type': 'application/json'},
        )
