from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'
    org_name = 'acme'
    solr_url = 'http://localhost:8983/solr'
    solr_collections = [
        '_item_train',
        '_items',
        '_logs',
        '_events',
        '_event_aggregations',
    ]
