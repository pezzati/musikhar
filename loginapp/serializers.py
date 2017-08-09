from rest_framework import serializers

class User_Profile_Serializer (serializers.Serializer):
    username = serializers.CharField(max_length= 100)
    # password ?
    email = serializers.CharField(max_length= 50)
    age = serializers.IntegerField(default=0)
    mobile = serializers.CharField(max_length=20)
    gender = serializers.IntegerField(default=0)
