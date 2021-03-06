#from mysite.mysite.polls.models import Servers
from ..models import *
from rest_framework import serializers
#from rest_framework.serializers import ModelSerializer
class ServerSerializer(serializers.ModelSerializer):
    status=serializers.StringRelatedField(
        #many=True,
        #read_only=True,
        #slug_field='status'
    )
    class Meta:
        model= Servers
        fields=('id','status','assert_number')


class StaffSerializer(serializers.ModelSerializer):
    # status=serializers.StringRelatedField(
    #     #many=True,
    #     #read_only=True,
    #     #slug_field='status'
    # )
    department=serializers.StringRelatedField(
        read_only=True
    )
    class Meta:
        model= Staff
        fields=('id','email','name','ipaddress','department')