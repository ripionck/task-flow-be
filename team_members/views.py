from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from boards.models import Board
from .models import TeamMember
from .serializers import TeamMemberSerializer


class TeamMemberListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve team members for boards owned by the authenticated user.
        """
        # Filter boards owned by the authenticated user
        user_boards = Board.objects.filter(created_by=request.user)
        # Filter team members for these boards
        team_members = TeamMember.objects.filter(board__in=user_boards)
        serializer = TeamMemberSerializer(team_members, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new team member for a board owned by the authenticated user.
        """
        serializer = TeamMemberSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # Save the team member
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamMemberDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get a team member by its primary key.
        Ensure the team member belongs to a board owned by the authenticated user.
        """
        try:
            team_member = TeamMember.objects.get(pk=pk)
            if team_member.board.created_by != self.request.user:
                raise TeamMember.DoesNotExist  # Prevent unauthorized access
            return team_member
        except TeamMember.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a specific team member.
        """
        team_member = self.get_object(pk)
        if not team_member:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TeamMemberSerializer(team_member)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific team member.
        """
        team_member = self.get_object(pk)
        if not team_member:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TeamMemberSerializer(
            team_member, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific team member.
        """
        team_member = self.get_object(pk)
        if not team_member:
            return Response(status=status.HTTP_404_NOT_FOUND)
        team_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
