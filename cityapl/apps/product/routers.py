"""
"""
from django.urls import path, include 
from rest_framework.routers import SimpleRouter

# from .views import (
#     TokenAPIView,TokenAssignAPIView
# )

router = SimpleRouter()

# router.register(r'token', TokenViewSet, basename='token')

urlpatterns = [
	# path('token/create/', TokenAPIView.as_view(), name='token-create'),
	# path('token/unblock/', TokenAPIView.as_view(), name='token-unblock'),
	# path('token/<str:token>/delete/', TokenAssignAPIView.as_view(), name='token-delete'),
	# path('token/assign-token/', TokenAssignAPIView.as_view(), name='assign-token'),
	# path('token/keep-alive/', TokenAssignAPIView.as_view(), name='keep-alive-token'),
]

urlpatterns += router.urls
