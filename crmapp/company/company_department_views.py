from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import Department, DpartmentalGoal
from .company_department_serializer import CompanyDepartmentSerializer, CompanyDpartmentalGoalSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Department data.
    """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = CompanyDepartmentSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a single department with error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Department.DoesNotExist:
            raise NotFound("The requested Department does not exist.")
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a department with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete Department: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CompanyDpartmentalGoalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Departmental Goals.
    """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = DpartmentalGoal.objects.all()
    serializer_class = CompanyDpartmentalGoalSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a single departmental goal with error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except DpartmentalGoal.DoesNotExist:
            raise NotFound("The requested Departmental Goal does not exist.")
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a departmental goal with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete Departmental Goal: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
