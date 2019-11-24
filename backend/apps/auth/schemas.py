from marshmallow import fields
from marshmallow import validate as validators

from ..extensions import schemas


class AuthLoginSchema(schemas.Schema):
    email = fields.Email(
        required=True,
        validate=[validators.Length(min=3, max=255)],
    )
    password = fields.String(
        required=True,
        validate=[validators.Length(min=3, max=255)],
    )

    class Meta:
        fields = ('email', 'password')
        load_only = fields
