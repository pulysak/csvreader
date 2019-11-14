from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer

from .serializers import ProductSerializer
from .models import Product


class ProductListView(ListAPIView):

    renderer_classes = (JSONRenderer,)

    queryset = Product.objects.active()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        producer = self.request.query_params.get('producer')
        if producer:
            qs = qs.filter(producer=producer)
        return qs
