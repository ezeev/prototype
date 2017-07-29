
import requests
from ..apps import AppConfig


solr_url = AppConfig.solr_url
create_command = solr_url + '/admin/collections?action=CREATE&name=%s&numShards=1&replicationFactor=1&collection.configName=default'
exists_url = solr_url + '/%s/select?indent=on&q=*:*&wt=json&rows=0'

class CollectionsList:
    collections = []
    messages = []

    def __init__(self, load_as_dict=False):
        self.load_collections(load_as_dict)


    def load_collections(self, as_dict):
        self.collections = []
        self.messages = []
        for coll in AppConfig.solr_collections:
            coll_obj = Collection()
            coll_obj.name = AppConfig.org_name + coll
            # check if the collection exists
            exists = exists_url % (AppConfig.org_name + coll)
            r = requests.get(exists)
            if r.status_code == 404:
                self.messages.append("Collection %s does not exist... Creating. \n" % (AppConfig.org_name + coll))
                cmd = create_command % (AppConfig.org_name + coll)
                r = requests.get(cmd)
                self.messages.append("Collection create command has returned status code: %d" % (r.status_code))

            if as_dict:
                self.collections.append(coll_obj.__dict__)
            else:
                self.collections.append(coll_obj)



class Collection:
    name = ""
    status = ""
    num_docs = 0



