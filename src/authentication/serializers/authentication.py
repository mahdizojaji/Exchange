from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


# class LoginSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("username", "password")
#         extra_kwargs = {"phone_number": {"validators": [User.phone_number_validator]}}
#
#
# class LoginUserDetailsSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("uuid", "phone_number")
#         read_only_fields = ("uuid", "phone_number")