from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'
    org_name = 'acme'
    solr_url = 'http://localhost:8983/solr'
    items_collection = org_name + '_items'
    aggregations_collection = org_name + '_event_aggregations'

    solr_collections = [
        '_item_train',
        '_items',
        '_logs',
        '_events',
        '_event_aggregations',
    ]

    default_item_search_params = {
        'defType' : 'edismax',
        'qf' : 'keywords_txt_en',
        'pf' : 'keywords_txt_en',
        'mm' : '50%',
        'wt' : 'json',
        'indent' : 'true',
    }
