import logging
from django.contrib.auth.hashers import make_password, check_password

from core.models import User

logger = logging.getLogger(__name__)


def update_password(user, raw_password):
    hashed = make_password(raw_password)
    User.objects.update(
        password=hashed,
    )
    logger.info(f"Credential updated for {user.id=}")


def verify_password(user, raw_password):
    try:
        hashed = user.password
        return check_password(raw_password, hashed)
    except User.DoesNotExist:
        logger.info("Varification Failed: user doesnt exist")
