from rest_framework import serializers
from django.contrib.auth.models import User
from loadtest.models import Product, SoloPiFile


class UserSerializer(serializers.ModelSerializer):
    # products = serializers.HyperlinkedModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username']


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Product
        fields = ['url', 'id', 'user', 'name', 'desc', 'producter', 'created_time']
