from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from products_app.models import ProductModel
from products_app.serializers import ProductSerializer

class ProductView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request):
        products = ProductModel.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post (self, request):

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            instance = serializer.save()
            print(instance)
            return Response(serializer.data)
        return Response('Not valid data')

