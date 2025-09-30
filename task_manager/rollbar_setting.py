import rollbar
import logging
import os
from django.conf import settings
from rollbar.logger import RollbarHandler


ROLLBAR = {
    'access_token': os.getenv(
        "ROLLBAR_TOKEN",
        "ab027f85a51e7eadf2bb36b552d1516",
    ),
    'environment': os.getenv("ROLLBAR_ENV", "development"),
    'root': settings.BASE_DIR,
}

rollbar.init(**ROLLBAR)


logger = logging.getLogger(__name__)
logger.addHandler(RollbarHandler())
