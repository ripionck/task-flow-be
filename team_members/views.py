from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TeamMember
from .serializers import TeamMemberSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class TeamMemberListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        team_members = TeamMember.objects.all()  # Or filter by board if needed
        serializer = TeamMemberSerializer(team_members, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeamMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # No direct creator to set
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamMemberDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            team_member = TeamMember.objects.get(pk=pk)
        except TeamMember.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TeamMemberSerializer(team_member)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            team_member = TeamMember.objects.get(pk=pk)
        except TeamMember.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TeamMemberSerializer(
            team_member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            team_member = TeamMember.objects.get(pk=pk)
        except TeamMember.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        team_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
