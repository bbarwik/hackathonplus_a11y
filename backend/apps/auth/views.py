from http import HTTPStatus

from flask import (
    Response,
    current_app,
    json,
    request,
)

from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy.orm.exc import (
    MultipleResultsFound,
    NoResultFound,
)

from apps.common.views import APIView
from apps.users.models import User

from . import schemas


class AuthJWTTokenCreateView(APIView):
    method_decorators = {
        'delete': [jwt_required],
    }

    def post(self) -> Response:
        data = schemas.AuthLoginSchema().load(request.json)
        invalid_credentials_response = Response(
            json.dumps({'message': 'Invalid credentials'}),
            HTTPStatus.UNAUTHORIZED,
            headers={'Content-Type': 'application/json'},
        )
        try:
            user = User.query.filter_by(email=data['email']).one()
        except (NoResultFound, MultipleResultsFound):
            return invalid_credentials_response
        if user.password != data['password']:
            return invalid_credentials_response
        access_token = create_access_token(identity=user)
        return Response(
            json.dumps({current_app.config['JWT_JSON_KEY']: access_token}),
            HTTPStatus.OK,
            headers={'Content-Type': 'application/json'},
        )

    def delete(self) -> Response:
        # TODO: blacklist token
        return Response(None, HTTPStatus.OK)
