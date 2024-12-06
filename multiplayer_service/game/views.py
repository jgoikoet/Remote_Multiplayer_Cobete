from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication 

from . import views_match_history

@api_view(['GET'])
@authentication_classes([JWTStatelessUserAuthentication])
def match_list(request):
    try:
        return views_match_history.match_list(request)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([JWTStatelessUserAuthentication])
def stats_view(request, user_id):
    try:
        return views_match_history.stats_view(request, user_id)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([JWTStatelessUserAuthentication])
def match_list_id(request, pk):
    try:
        return views_match_history.match_list_id(request, pk)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
