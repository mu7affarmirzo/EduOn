from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.orders.serializers import CartSerializer
from orders.models import CartModel, CartItemModel
from orders.models.cart import CartModel


class CartListView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CartModel.objects.get(pk=pk)
        except CartModel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(tags=['cart'])
    def get(self, request, format=None):
        snippets = CartModel.objects.all()
        serializer = CartSerializer(snippets, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['cart'], request_body=CartSerializer)
    def post(self, request, format=None):
        account = request.user
        course = CartModel(owner=account)
        serializer = CartSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CartModel.objects.get(pk=pk)
        except CartModel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(tags=['cart'])
    def delete(self, request, pk, format=None):
        try:
            course = CartModel.objects.get(id=pk)
        except CartModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if course.owner.id != user.id:
            return Response({'response': "You don't have the permission to delete that."})
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

