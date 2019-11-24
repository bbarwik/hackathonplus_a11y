from flask import current_app

from sqlalchemy import (
    Boolean,
    Column,
    String,
)
from sqlalchemy_utils import (
    EmailType,
    PasswordType,
)

from apps.common.models import (
    Timestampable,
    UUIDable,
)


class User(Timestampable, UUIDable):
    email = Column(EmailType, nullable=False, unique=True)
    first_name = Column(String(length=255), nullable=False)
    last_name = Column(String(length=255), nullable=False)
    username = Column(String(length=255), nullable=False)
    password = Column(
        PasswordType(
            max_length=255,
            onload=(
                lambda **kwargs: {
                    **kwargs,
                    'schemes': current_app.config['PASSWORD_SCHEMES'],
                }
            ),
        ),
        nullable=False,
        unique=False,
    )
    is_active = Column(Boolean, default=True)
