"""
"""
import datetime

from django.db.models import IntegerField, F
from django.db.models.functions import Cast, ExtractDay, TruncDate
from django.db.models import DurationField, F, ExpressionWrapper

from cityapl.apps.token_pool.models import TokenPool


def delete_tokens():
	"""
	1. cron script to unblocked token after 60s of use if not keep alived
	2. delete erpired keep-lived token if not get keep-live hit after 5 min  
	"""
	current_time = datetime.datetime.now()
	print(current_time)
	# Case-1
	qs = TokenPool.objects.filter(
		is_assigned  = True,
		expire_at__lte = current_time
	).annotate(
		diff=ExpressionWrapper(F('expire_at') - F('updated_at'), output_field=DurationField())
	).filter(
		diff__lte = datetime.timedelta(minutes=2),
	).update(is_assigned=False, expire_at=None)

	#Case-2
	qs = TokenPool.objects.filter(
		is_assigned  = True,
		expire_at__lte = current_time
	).annotate(
		diff=ExpressionWrapper(F('expire_at') - F('updated_at'), output_field=DurationField())
	).filter(
		diff__gte = datetime.timedelta(minutes=5),
	).delete()