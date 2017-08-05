from rest_framework import viewsets
from .lib.collections import CollectionsList
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer
from .lib.query_processing import QueryProcessor, AddParamStep, SolrQueryProcessor, SolrItemRecommendationBoostStep, SetParamsStep
from django.http import HttpResponse
import json
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
        step1 = SetParamsStep("set-params", AppConfig.default_item_search_params)
        q = '/select?rows=100&defType=edismax&q=%s&pf=query_txt_en&qf=query_txt_en&fl=score,*,countBoost:product(0.01,log(event_count_i)),recencyBoost:product(0.01,sqrt(log(avg_ts_i))),summed:sum(product(0.01,log(event_count_i)),product(0.01,sqrt(log(avg_ts_i))))&debug=true&boost=sum(product(0.01,log(event_count_i)),product(0.01,sqrt(log(avg_ts_i))))&wt=json&indent=true'
        step2 = SolrItemRecommendationBoostStep("3", AppConfig.solr_url, AppConfig.aggregations_collection, q, 'sku_s', 'summed', 'sku_s', multiplier=10)
        steps = [step1, step2]
        q = SolrQueryProcessor(steps, params, AppConfig.solr_url, AppConfig.items_collection, '/select')
        resp = q.execute()
        r = HttpResponse(resp, content_type="application/json")
        return(r)
    else:
        return(unauthoirzed())


def unauthoirzed():
    resp = Response({"Unauthorized"})
    resp.status_code = 401
    return resp