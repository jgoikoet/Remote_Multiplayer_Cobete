from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes  # Decorators for API views
from django.db.models import Q
from django.http import JsonResponse
from .models import Match
from .serializer import MatchSerializer
import jwt
from django.contrib.auth import authenticate  # Handles user authentication

# Simple JWT imports
from rest_framework_simplejwt.tokens import RefreshToken  # Handles refresh tokens for JWT
from rest_framework_simplejwt.authentication import JWTAuthentication  # JWT authentication backend
from rest_framework.authentication import TokenAuthentication  # Token-based authentication
from rest_framework.authtoken.models import Token  # Token model for authentication
from rest_framework.permissions import IsAuthenticated  # Permission class to ensure user is authenticated


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def match_list(request):
    matches = Match.objects.all()
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def stats_view(request, user_id):
    individual_matches = Match.objects.filter(
        Q(player1_id=user_id) | Q(player2_id=user_id))
    individual_played = individual_matches.count()
    individual_won = individual_matches.filter(winner_id=user_id).count()

    return JsonResponse({
        "individual_matches": {
            "played": individual_played,
            "won": individual_won
        },
        "total": {
            "played": individual_played,
            "won": individual_won
        }
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def match_list_id(request, pk):
    matches = Match.objects.filter(
        (Q(player1_id=pk) | Q(player2_id=pk)))
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)
