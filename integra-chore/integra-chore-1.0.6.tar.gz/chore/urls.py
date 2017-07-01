# Author : Partha
"""
    Relative Imports helps us to integrate in any app
"""
from django.conf.urls import url

from .views import TestAPI, ListTables, ListFields, ListTableData, ListFieldsData, ListQueryData
from .views import ChoreTablesView, ChoreFeildsView, ChoreTableDataView, ChoreQueryView

urlpatterns = [
    # Exposing API
    url(r'^api/core/test/$', TestAPI.as_view(), name='test'),
    url(r'^api/core/tables/$', ListTables.as_view(), name='list-tables'),
    url(r'^api/core/fields/(?P<table_name>[\w-]+)/$', ListFields.as_view(), name='list-fields'),
    url(r'^api/core/table/(?P<table_name>[\w-]+)/$', ListTableData.as_view(), name='list-table-data'),
    url(r'^api/core/table/(?P<table_name>[\w-]+)/fields/$', ListFieldsData.as_view(), name='list-field-data'),
    url(r'^api/core/query/(?P<query_name>[\w-]+)/$', ListQueryData.as_view(), name='list-query-data'),    
    # Query Manager URLS
    url(r'^chore/tables/$', ChoreTablesView.as_view(), name='table-view'),    
    url(r'^chore/(?P<table_name>[\w-]+)/fields/$', ChoreFeildsView.as_view(), name='fields-view'),    
    url(r'^chore/(?P<table_name>[\w-]+)/data/$', ChoreTableDataView.as_view(), name='data-view'),    
    url(r'^chore/(?P<query_name>[\w-]+)/query/$', ChoreQueryView.as_view(), name='query-view'),    
]
