# """
# """
# import uuid

# from rest_framework import serializers



# class TokenCreateSerializer(serializers.ModelSerializer):
#     """
#     Serializer to create token
#     """
#     class Meta:
#         model = TokenPool
#         fields = ()

#     def create(self, validated_data):
#     	"""
#     	"""
#     	validated_data['token'] = uuid.uuid4()
#     	return super().create(validated_data)


# class TokenSerializer(serializers.ModelSerializer):
#     """
#     Serializer to create token
#     """
#     token = serializers.CharField()
#     class Meta:
#         model = TokenPool
#         fields = ('token',)