import logging
from django.contrib.auth.hashers import make_password, check_password

from core.models import Credential, User

logger = logging.getLogger(__name__)


def set_password(user, raw_password):
    hashed = make_password(raw_password)
    Credential.objects.create(
        user=user,
        provider=Credential.Provider.PASSWORD,
        password=hashed,
    )
    logger.info(f"Credential created for {user.id=}")


def update_password(user, raw_password):
    hashed = make_password(raw_password)
    Credential.objects.update(
        user=user,
        provider=Credential.Provider.PASSWORD,
        password=hashed,
    )
    logger.info(f"Credential updated for {user.id=}")


def verify_password(user, raw_password):
    try:
        cred = user.credentials.get(provider=Credential.Provider.PASSWORD)
        return check_password(raw_password, cred.password)
    except User.DoesNotExist:
        logger.info("Varification Failed: user doesnt exist")
    except Credential.DoesNotExist:
        logger.info("Varification Failed: credential doesnt exist")
