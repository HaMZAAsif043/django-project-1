from rest_framework import generics
from products_app.models import ProductModel
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view ,permission_classes
from products_app.serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
class ProductCreateAPIView(generics.CreateAPIView):
    queryset =ProductModel.objects.all()
    serializer_class =ProductSerializer
    permission_classes =[AllowAny]
    def perform_create(self,serializer):
        # serializer.save(user=self.request.user)
        print(serializer.validated_data)
        serializer.save()

product_create_view = ProductCreateAPIView.as_view()
class ProductDetailsAPIView(generics.RetrieveAPIView):
    queryset =ProductModel.objects.all()
    serializer_class =ProductSerializer
product_details_view = ProductDetailsAPIView.as_view()

class ProductListAPIView(generics.ListCreateAPIView):
    queryset =ProductModel.objects.all()
    serializer_class =ProductSerializer
    permission_classes =[AllowAny]

product_List_view = ProductListAPIView.as_view()

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def product_alt_view(request,pk=None,*args ,**kwargs,):
    if request.method == 'GET':
        if pk is not None:
            obj = get_object_or_404(Product,pk=pk)
            data =ProductSerializer(obj,many=False)

            return Response(data)
        queryset =ProductModel.objects.all()
        data = ProductSerializer(queryset,many=True).data
        return Response(data)
    if request.method == 'POST':
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.data)
            return Response(serializer.data)