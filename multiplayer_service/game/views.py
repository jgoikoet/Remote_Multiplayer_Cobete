from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Match
from .serializer import MatchSerializer

@api_view(['GET'])
def match_list(request):
    matches = Match.objects.all()
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)
