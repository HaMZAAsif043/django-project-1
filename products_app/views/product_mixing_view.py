from rest_framework import generics ,mixins
from products_app.models import ProductModel
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view ,permission_classes
from products_app.serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class ProductMixinView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    # mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):
    queryset =ProductModel.objects.all()
    serializer_class =ProductSerializer
    permission_classes =[AllowAny]
    lookup_field = 'pk'
    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get("pk")

        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    def put(self,request,*args,**kwargs):
        return self.update(request, *args, **kwargs)

product_mixin_view = ProductMixinView.as_view()