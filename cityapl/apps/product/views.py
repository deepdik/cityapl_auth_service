# """
# """
# import datetime

# from django.db.models import F

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .serializers import (TokenCreateSerializer,
# 	TokenSerializer)


# class TokenAPIView(APIView):
# 	"""
# 	"""
# 	serializer_class = TokenCreateSerializer
# 	def post(self, request, *args, **kwargs):
# 		"""
# 		POST method to create new token
# 		"""
# 		serializer = self.serializer_class(data=request.data)
# 		serializer.is_valid(raise_exception=True)
# 		serializer.save()
# 		return Response({
# 			'detail': 'New token created successfully'
# 			}, status=status.HTTP_201_CREATED)

# 	def put(self, request, *args, **kwargs):
# 		"""
# 		To unblock a token
# 		"""
# 		serializer = TokenSerializer(data=request.data)
# 		serializer.is_valid(raise_exception=True)
# 		# search for token in pool. 
# 		qs = TokenPool.objects.filter(
# 			token=serializer.validated_data['token'],
# 		)
# 		if qs.exists():
# 			obj = qs.first()
# 			obj.expire_at  = None
# 			obj.is_assigned  = False
# 			obj.save()
# 			return Response({
# 				'detail': 'Token unblocked successfully',
# 				'token': obj.token
# 				}, status=status.HTTP_201_CREATED)

# 		return Response({
# 				'detail': 'No unblocked token found'
# 				}, status=status.HTTP_404_NOT_FOUND)


# class TokenAssignAPIView(APIView):
# 	"""
# 	"""
# 	def get(self, request, *args, **kwargs):
# 		"""
# 		GET method to assign a token
# 		"""
# 		# search for available tokens in pool
# 		qs = TokenPool.objects.filter(is_assigned=False)
# 		if qs.exists():
# 			obj = qs.first()
# 			obj.expire_at  = datetime.datetime.now()+datetime.timedelta(
# 				minutes=1)
# 			obj.is_assigned = True
# 			obj.save()
# 			return Response({
# 				'detail': 'New token assigned successfully',
# 				'token': obj.token,
# 				'expire_at':obj.expire_at,
# 				}, status=status.HTTP_201_CREATED)

# 		return Response({
# 				'detail': 'No active token found in pool'
# 				}, status=status.HTTP_404_NOT_FOUND)


# 	def delete(self, request, *args, **kwargs):
# 		"""
# 		Post method to delete token
# 		"""
# 		token = kwargs.get('token')
# 		qs = TokenPool.objects.filter(
# 			token=token,
# 		)
# 		if qs.exists():
# 			qs.delete()
# 			return Response({
# 				'detail': 'Token deleted successfully',
# 				}, status=status.HTTP_200_OK)

# 		return Response({
# 				'detail': 'No token found'
# 				}, status=status.HTTP_404_NOT_FOUND)

# 	def put(self, request, *args, **kwargs):
# 		"""
# 		Method to keep token alive for next 5 minute
# 		"""
# 		serializer = TokenSerializer(data=request.data)
# 		serializer.is_valid(raise_exception=True)
# 		current_time = datetime.datetime.now()
# 		qs = TokenPool.objects.filter(
# 			token=serializer.validated_data['token'],
# 			is_assigned=True,
# 		)
# 		if qs.exists():
# 			obj = qs.first()
# 			if obj.expire_at > current_time:
# 				obj.expire_at = obj.expire_at + datetime.timedelta(minutes=5)
# 				obj.save()
# 				return Response({
# 					'detail': 'Alived for next 5 minute',
# 					'expire_at':obj.expire_at
# 					}, status=status.HTTP_200_OK)
# 			else:
# 				return Response({
# 					'detail': 'Token is already expired',
# 					'expire_at':obj.expire_at
# 					}, status=400)

# 		return Response({
# 				'detail': 'No token found'
# 				}, status=status.HTTP_404_NOT_FOUND)

