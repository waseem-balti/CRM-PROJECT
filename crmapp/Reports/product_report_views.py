from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import Product
from .product_report_serializers import ProductReportSerializer

class ProductReportViewSet(viewsets.ViewSet):
    """
    ViewSet for generating Product reports.
    """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Generate a product report for all products.
        """
        try:
            products = Product.objects.all()
            serializer = ProductReportSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to generate product report: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        """
        Generate a product report for a specific product.
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductReportSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            raise NotFound("The requested Product does not exist.")
        except Exception as e:
            return Response(
                {"error": f"Failed to generate product report: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
