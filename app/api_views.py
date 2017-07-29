from rest_framework import viewsets
from .lib.collections import CollectionsList
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer
from .lib.query_processing import QueryProcessor, AddParamStep, SolrQueryProcessor
from .apps import AppConfig


@api_view(['GET'])
def api_status(request):
    if request.user.is_staff:
        colls_obj = CollectionsList(load_as_dict=True)
        return Response(colls_obj.__dict__)
    else:
        return unauthoirzed()

@api_view(['GET'])
def api_query(request):
    if request.user.has_perm("app.query_user"):
        params = request.GET.copy()
        s1 = AddParamStep("1", "step", "1")
        s2 = AddParamStep("2", "step", "2")
        steps = [s1, s2]
        q = SolrQueryProcessor(steps, params, AppConfig.solr_url, AppConfig.org_name + AppConfig.solr_collections[0], '/select')
        resp = q.execute()
        print(params)
        return(Response(resp))
    else:
        return(unauthoirzed())


def unauthoirzed():
    resp = Response({"Unauthorized"})
    resp.status_code = 401
    return resp