from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import Branch
from .branch_serializers import BranchSerializer

class BranchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Branches.
    """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BranchSerializer

    def get_queryset(self):
        return Branch.objects.all()

    def edit(self, request, pk=None):
        """
        Handle editing a branch.
        """
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({"error": "Branch not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BranchSerializer(branch, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Handle deletion of a branch.
        """
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({"error": "Branch not found."}, status=status.HTTP_404_NOT_FOUND)

        branch.delete()
        return Response({"message": "Branch deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a single branch with error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Branch.DoesNotExist:
            raise NotFound("The requested Branch does not exist.")
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a branch with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete Branch: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
