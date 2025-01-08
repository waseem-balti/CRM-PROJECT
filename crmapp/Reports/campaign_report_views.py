# campaign_views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import Campaign
from .campaign_report_serializers import CampaignReportSerializer

class CampaignReportViewSet(viewsets.ViewSet):
    """
    ViewSet for generating Campaign reports.
    """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Generate a report for all campaigns.
        """
        try:
            campaigns = Campaign.objects.all()
            serializer = CampaignReportSerializer(campaigns, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to generate campaign report: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        """
        Generate a report for a specific campaign.
        """
        try:
            campaign = Campaign.objects.get(pk=pk)
            serializer = CampaignReportSerializer(campaign)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Campaign.DoesNotExist:
            raise NotFound("The requested Campaign does not exist.")
        except Exception as e:
            return Response(
                {"error": f"Failed to generate campaign report: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
