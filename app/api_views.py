from rest_framework import viewsets
from .viroonga.collections import CollectionsList
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer


@api_view(['GET'])
def api_status(request):
    if request.user.is_staff:
        colls_obj = CollectionsList(load_as_dict=True)
        return Response(colls_obj.__dict__)
    else:
        return unauthoirzed()



def unauthoirzed():
    resp = Response({"Unauthorized"})
    resp.status_code = 401
    return resp