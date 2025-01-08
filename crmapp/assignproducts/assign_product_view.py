from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import AssignProduct
from .assign_product_serializer import AssignProductSerializer

class AssignProductViewSet(viewsets.ModelViewSet):
    queryset = AssignProduct.objects.all()
    serializer_class = AssignProductSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except AssignProduct.DoesNotExist:
            raise NotFound("The requested AssignProduct does not exist.")

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete AssignProduct: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
