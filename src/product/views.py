from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer

from .serializers import ProductSerializer
from .models import Product


class ProductListView(ListAPIView):

    renderer_classes = (JSONRenderer,)

    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer

