import datetime

from django.core.management.base import BaseCommand

from spark_18 import pylogging
from spark_18.apps.token_pool.utils import delete_tokens


class Command(BaseCommand):
    """
    Cron task to send attendance miss alert
    """
    def handle(self, *args, **options):
        todays_datetime = datetime.datetime.now()
        try:
            delete_tokens()
            msg = "Token deleted successfully"
            pylogging.logger.info(
                "__CRON__: {0} on {1}".format(
                    msg, datetime.datetime.now()))
        except Exception as e:
            msg = "Something went wrong.\n {}".format(e)
            pylogging.logger.error(
                "__CRON__: Error in delete: {0} on {1}".format(
                    str(e), datetime.datetime.now())
            )

        self.stdout.write(msg)