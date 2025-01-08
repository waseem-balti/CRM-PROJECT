from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import LeadSummary
from .lead_summary_serializer import LeadSummarySerializer

class LeadSummaryViewSet(viewsets.ModelViewSet):
    queryset = LeadSummary.objects.all()
    serializer_class = LeadSummarySerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except LeadSummary.DoesNotExist:
            raise NotFound("The requested LeadSummary does not exist.")

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete LeadSummary: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
