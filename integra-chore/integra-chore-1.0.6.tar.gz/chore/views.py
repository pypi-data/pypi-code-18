# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .chore_api import ChoreAPI

class TestAPI(APIView):
    
    def get(self, request, format = None):
        """
        Just a Test API.
        """
        return Response({'message':'Success'})

class BaseApi(APIView):

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def post(self, *args, **kwargs):
        raise NotImplementedError

    def initialize(self, **creds):
        """ 
        Used to initialize the ChoreAPI
        """
        return ChoreAPI(**creds)

class ListTables(BaseApi):
    
    def post(self, request, format = None):
        """
        To list the tables
        @creds: {
            'app_type':'',
            'cred_type':'',
            'host':'',
            'db':'',
            'port':''
            'username':'',
            'password':''
        }
        """
        _reset = False
        if 'creds' not in request.data or request.data['creds'] == "" or type(request.data['creds']) is not dict :
            return Response({'message': 'Please provide credentials'}, status = status.HTTP_406_NOT_ACCEPTABLE)
        creds = request.data['creds']
        
        # Provide UUID if not provided
        if 'UUID' not in request.data or request.data['UUID'] == "":
            if request.user is not None and request.user.is_authenticated():
                creds.update({ 'UUID' : request.session.session_key })
            else:
                creds.update({ 'UUID' : request.auth.token })   
        if 'reset' in request.GET and request.GET['reset'] != "" and request.GET['reset'] != 'False':
            _reset = True             
        apiRef = self.initialize(**creds)
        data = apiRef.getTablesList(_format = "json", reset = _reset)
        if data is None:
            return Response({'message': 'Unabled to process the request'}, status = status.HTTP_400_BAD_REQUEST)            
        return Response(data, status = status.HTTP_200_OK)

    def get(self, request, format = None):
        """
        Return error
        """
        return Response({"message": "Not Supported"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

class ListFields(BaseApi):
    
    def post(self, request, table_name = None, format = None):
        """
        To list the Fields
        @creds: {
            'app_type':'',
            'cred_type':'',
            'host':'',
            'db':'',
            'port':''
            'username':'',
            'password':''
        }
        """
        if 'creds' not in request.data or request.data['creds'] == "" or type(request.data['creds']) is not dict :
            return Response({'message': 'Please provide credentials'}, status = status.HTTP_406_NOT_ACCEPTABLE)
        
        if table_name is None:
            return Response({'message': 'Please provide table_name'}, status = status.HTTP_406_NOT_ACCEPTABLE)
            
        creds = request.data['creds']
        
        # Provide UUID if not provided
        if 'UUID' not in request.data or request.data['UUID'] == "":
            if request.user is not None and request.user.is_authenticated():
                creds.update({ 'UUID' : request.session.session_key })
            else:
                creds.update({ 'UUID' : request.auth.token })                
        apiRef = self.initialize(**creds)
        data = apiRef.getTableFieldsList(table_name = table_name, _format = "json")
        if data is None:
            return Response({'message': 'Unabled to process the request'}, status = status.HTTP_400_BAD_REQUEST)            
        return Response(data, status = status.HTTP_200_OK)
        

    def get(self, request, format = None):
        """
        Return error
        """
        return Response({"message": "Not Supported"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

class ListTableData(BaseApi):
    
    def post(self, request, table_name = None, format = None):
        """
        To list the TableData
        @creds: {
            'app_type':'',
            'cred_type':'',
            'host':'',
            'db':'',
            'port':''
            'username':'',
            'password':''
        }
        @page
        @reset
        @page_size
        """
        _reset = False
        _page = 1
        _page_size = 10
        _format = "json"

        if 'creds' not in request.data or request.data['creds'] == "" or type(request.data['creds']) is not dict :
            return Response({'message': 'Please provide credentials'}, status = status.HTTP_406_NOT_ACCEPTABLE)
        
        if table_name is None:
            return Response({'message': 'Please provide table_name'}, status = status.HTTP_406_NOT_ACCEPTABLE)
            
        creds = request.data['creds']
        
        # Provide UUID if not provided
        if 'UUID' not in request.data or request.data['UUID'] == "":
            if request.user is not None and request.user.is_authenticated():
                creds.update({ 'UUID' : request.session.session_key })
            else:
                creds.update({ 'UUID' : request.auth.token })                

        if 'reset' in request.GET and request.GET['reset'] != "" and request.GET['reset'] != 'False':
            _reset = True
        
        if 'page' in request.GET and request.GET['page'] != "":
            _page = int(request.GET['page'])

        if 'page_size' in request.GET and request.GET['page_size'] != "":
            _page_size = int(request.GET['page_size'])

        apiRef = self.initialize(**creds)
        data = apiRef.getTableData(table_name = table_name, _format = _format, page = _page, page_size = _page_size, reset = _reset)
        if data is None:
            return Response({'message': 'Unabled to process the request'}, status = status.HTTP_400_BAD_REQUEST)            
        return Response(data, status = status.HTTP_200_OK)

    def get(self, request, format = None):
        """
        Return error
        """
        return Response({"message": "Not Supported"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

class ListFieldsData(APIView):
    
    def post(self, request, format = None):
        """
        To list the FieldsData
        """
        return Response({}, status = status.HTTP_200_OK)

    def get(self, request, format = None):
        """
        Return error
        """
        return Response({"message": "Not Supported"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

class ListQueryData(BaseApi):
    
    def post(self, request, query_name = None, format = None):
        """
        To list the TableData
        @creds: {
            'app_type':'',
            'cred_type':'',
            'host':'',
            'db':'',
            'port':''
            'username':'',
            'password':''
        }
        @page
        @reset
        @page_size
        """
        _reset = False
        _page = 1
        _page_size = 10
        _format = "json"
        if query_name is None:
            return Response({'message': 'Please provide query_name'}, status = status.HTTP_406_NOT_ACCEPTABLE)
        
        if 'creds' not in request.data or request.data['creds'] == "" or type(request.data['creds']) is not dict :
            return Response({'message': 'Please provide credentials'}, status = status.HTTP_406_NOT_ACCEPTABLE)
        
        if 'query' not in request.data or request.data['query'] == "":
            return Response({'message': 'Please provide query'}, status = status.HTTP_406_NOT_ACCEPTABLE)
        
        creds = request.data['creds']
        query = request.data['query']
        
        # Provide UUID if not provided
        if 'UUID' not in request.data or request.data['UUID'] == "":
            if request.user is not None and request.user.is_authenticated():
                creds.update({ 'UUID' : request.session.session_key })
            else:
                creds.update({ 'UUID' : request.auth.token })                

        if 'reset' in request.GET and request.GET['reset'] != "" and request.GET['reset'] != 'False':
            _reset = True
        
        if 'page' in request.GET and request.GET['page'] != "":
            _page = int(request.GET['page'])

        if 'page_size' in request.GET and request.GET['page_size'] != "":
            _page_size = int(request.GET['page_size'])

        apiRef = self.initialize(**creds)
        data = apiRef.getQueryData(query_name = query_name, query = query, _format = _format, page = _page, page_size = _page_size, reset = _reset)
        if data is None:
            return Response({'message': 'Unabled to process the request'}, status = status.HTTP_400_BAD_REQUEST)            
        return Response(data, status = status.HTTP_200_OK)

    def get(self, request, format = None):
        """
        Return error
        """
        return Response({"message": "Not Supported"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)


class ChoreTablesView(View):
    """
    Used to list the tables
    """

    def get(self, request):
        return render(request, "chore/chore-tables.html", {})
    
    def post(self, request):
        """
        Not a supported method
        """
        raise NotImplementedError

class ChoreFeildsView(View):
    """
    Used to list the fields of specified table
    """

    def get(self, request, table_name = None):
        return render(request, "chore/chore-fields.html", {'table_name':table_name})

    def post(self, request):
        """
        Not a supported method
        """
        raise NotImplementedError
        
class ChoreTableDataView(View):
    """
    Used to list the data of specified table
    """

    def get(self, request, table_name = None):
        return render(request, "chore/chore-data.html", {"table_name":table_name})

    def post(self, request):
        """
        Not a supported method
        """
        raise NotImplementedError

class ChoreQueryView(View):
    """
    Used to list the data of specified Query
    """
    def get(self, request, query_name = None):
        return render(request, "chore/chore-query.html", {"query_name":query_name})

    def post(self, request):
        """
        Not a supported method
        """
        raise NotImplementedError


"""

Listing Tables
Content-Type: application/json
url:
    /api/core/tables/

Listing Fields
Content-Type: application/json
url:
    /api/core/fields/<table_name>/

Listing TableData
Content-Type: application/json
url:
    /api/core/table/<table_name>/

Listing Only ColumnData
Content-Type: application/json
url:
    /api/core/table/<table_name>/fields/?search=<col1>,<col2>

Listing the QueryData
Content-Type:
url:
    /api/core/query/<query_name>/?query=<sql query>

#Sample Data
creds = {
    'app_type':'RDBMS',
    'cred_type': 'POSTGRES',
    'host': 'localhost',
    'db': 'sunrisebilling',
    'port':5432,
    'username':'integra',
    'password':'integra'
}

"""
