

import requests


class QueryProcessor:
    steps = []
    params = ""

    def __init__(self, steps, params):
        self.steps = steps
        self.params = params

    def execute(self):
        pass

class SolrQueryProcessor(QueryProcessor):

    def __init__(self, steps, params, solr_url, collection, req_handler):
        QueryProcessor.steps = steps
        QueryProcessor.params = params
        self.solr_url = solr_url
        self.collection = collection
        self.req_handler = req_handler

    def execute(self):
        for step in QueryProcessor.steps:
                step.do_step(QueryProcessor.params)
        return self.solr_url + "/" + self.collection + self.req_handler + "?" + QueryProcessor.params.urlencode()



# Base class for query step
class QueryStepBase:
    # do something with the params and return them back
    def __init__(self, id):
        self.id = id

    def do_step(self, params):
        pass


class AddParamStep(QueryStepBase):
    def __init__(self, id, param_name, param_val):
        QueryStepBase.id = id
        self.param_name = param_name
        self.param_val = param_val

    def do_step(self, params):
        params[self.param_name] = self.param_val


class SolrItemRecommendationBoostStep(QueryStepBase):
    def __init__(self, id, multiplier = 1, num_recs = 100):
        QueryStepBase.id = id
        self.multiplier = multiplier
        self.num_recs = num_recs

    def do_step(self, params):
        # here is where we query solr and get boosts
        q = params['q']
        url = "http://localhost:8983/solr/acme_event_aggregations/select?defType=edismax&q=%s&pf=query_txt_en&qf=query_txt_en&fl=score,*,countBoost:product(0.01,log(event_count_i)),recencyBoost:product(0.01,sqrt(log(avg_ts_i))),summed:sum(product(0.01,log(event_count_i)),product(0.01,sqrt(log(avg_ts_i))))&debug=true&rows=%d&boost=sum(product(0.01,log(event_count_i)),product(0.01,sqrt(log(avg_ts_i))))&wt=json&indent=true" % (q, self.num_recs)
        r = requests.get(url)
        json = r.json()
        # append to existing bq if there is one
        bq = params.get('bq', "")
        if len(bq) > 0:
            bq = bq + " "
        for doc in json['response']['docs']:
            sku = doc['sku_s']
            boost = doc['summed']
            bq = bq + "sku_s:%s^%f " % (sku, boost)
        params['bq'] = bq.strip()




'''
class SolrQueryStep(QueryStepBase):
    def __init__(self, id, req_handler):
        QueryStepBase.__init__(self, id)
        self.req_handler = req_handler

    def do_step(self, params):
        query = "?v=true"
        for k in params.keys():
            query = query + "&" + k + "=" + params[k]
        return self.solr_url + "/" + self.collection + self.req_handler + query
'''

'''
class SolrQueryProcessor(QueryProcessorBase):
    def __init__(self, steps, query, solr_url, collection):
        #QueryProcessorBase.query = query
        #QueryProcessorBase.steps = steps
        QueryProcessorBase.__init__(self, steps, query)
        self.solr_url = solr_url
        self.collection = collection
'''

