from rest_framework import generics, status
from rest_framework import permissions

from django.contrib.auth.models import User
from loadtest.models import Product
from loadtest.serializers import ProductSerializer, UserSerializer


# Create your views here.
class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)
