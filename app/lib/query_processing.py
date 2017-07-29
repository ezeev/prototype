


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

        for k in QueryProcessor.params.keys():
            query = query + "&" + k + "=" + QueryProcessor.params[k]
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

