from django.db.models import Q
from django.http import JsonResponse
from rest_framework.response import Response

from .models import Match
from .serializer import MatchSerializer

def match_list(request):
    matches = Match.objects.all()
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)

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

def match_list_id(request, pk):
    matches = Match.objects.filter(
        (Q(player1_id=pk) | Q(player2_id=pk)))
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)
