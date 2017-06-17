
import sys, pprint
from pymongo import MongoClient
import constrains_spidy.contrain_checker as constrains
import pymongo

"""
Dependencies of the Library: 

pip3.5 install pymongo 

Metadata of Library 

Mandatory 
---------
mongo_host = DB hostname 
mongo_port = DB Port 
mongo_user = Username for DB access 
mongo_user_pass = Password for DB access 
mongo_db_name = Mongo Collection Name 
mongo_uri = URI format of mongo 

Optional 
---------
mongo_collection = DB Collection Name. 

"""
class mongo_functions:

      def __init__(self,baseline={}):
          self.__baseline__ = baseline

          #### Constrain Checks
          metadata_headers = ["mongo_host", "mongo_user","mongo_user_pass", \
                             "mongo_port", "mongo_db_name" ]
          constrain_check = constrains.constrain_check()
          constrain_check.metadata_checks(self.__baseline__, metadata_headers)

          ###### Connectivity checks
          constrain_check.check_network(self.__baseline__['mongo_host'],self.__baseline__['mongo_port'])

          ###### mongo Connectivity Code.
          try:
                if  self.__baseline__.__contains__("mongo_uri"):
                    self.__client = MongoClient(self.__baseline__['mongo_uri'])
                else:
                    if self.__baseline__["mongo_user"] == "":
                       self.__client = MongoClient(self.__baseline__['mongo_host'],int(self.__baseline__['mongo_port']))
                    else:
                       mongo_uri = "mongodb://" + self.__baseline__["mongo_user"] + ":" + self.__baseline__["mongo_user_pass"] + "@" + self.__baseline__["mongo_host"]
                       self.__client =  MongoClient(mongo_uri)
          except TypeError:
              print("Connectivity Issues with MongoDB, Kindly check and validated the DB connectivity settings Manually")
              sys.exit(1)
          except Exception as e:
              print("Connectivity Issues with MongoDB, Kindly check and validated the DB connectivity settings Manually")
              print(e)
              sys.exit(1)

          try:
                self.__db = self.__client[self.__baseline__['mongo_db_name']]
          except ValueError:
                print ("Problems with DB name or DB name does not Exists Check with MongoDB Administrator")
          except Exception as e:
                print("Connectivity Issues with MongoDB, Kindly check and validated the DB connectivity settings Manually")
                print(e)
                sys.exit(1)



      def mongo_writes(self):
          pass

      def mongo_get_info(self):
          ### Gather Database information
          list_data = {}
          list_data["collections"] = self.__db.collection_names(include_system_collections=True)
          list_data["profiling_info"] = self.__db.profiling_info()
          list_data["last_status"] = self.__db.last_status()
          list_data["sizeof"] = self.__db.__sizeof__()
          list_data["connectivity_details"] = self.__db.__str__()

          return list_data

      def mongo_get_db(self):
          ### Dump all DB Collections.
          list_data = {}
          list_documents = self.__db.collection_names()
          for docs in list_documents:
              list_data[docs] = []
              cursor  = self.__db.get_collection(name=docs).find({})
              for items in cursor:
                  list_data[docs].append(items)
              cursor.close()
          return list_data

      def mongo_get_collection(self,collection_name,search_filter=None):

          ### Dump given Collection Documents.
          list_data = []
          if search_filter == None:
             cursor = self.__db.get_collection(name=collection_name).find({},{'_id': False})
          else:
             cursor = self.__db.get_collection(name=collection_name).find(search_filter)

          for items in cursor:
              list_data.append(items)

          cursor.close()
          return list_data

      def mongo_new_collection(self,collection_name,data):

          ### Data Quality Check
          constrain_check = constrains.constrain_check()
          constrain_check.mongo_collection_creation_constrain(data)

          ### Check if Collection Exists
          check_collection  = self.mongo_get_info()
          if check_collection["collections"].__contains__(collection_name):
             print("Collection already Exists, Kindly use the mongo_append_collection function")
             sys.exit(1)

          ### Create new collection.
          self.__db.create_collection(name=collection_name).insert_many(data)
          return "Success"

      def mongo_append_collection(self,collection_name,data):

          ### Data Quality Check
          constrain_check = constrains.constrain_check()
          constrain_check.mongo_collection_creation_constrain(data)

          ### Check if Collection Exists
          """
          check_collection  = self.mongo_get_info()
          if not check_collection["collections"].__contains__(collection_name):
             print("Collection/Database Does not Exists, Kindly use the mongo_new_collection function")
             sys.exit(1)
          """

          ### Append to Collection
          self.__db.get_collection(collection_name).insert(data)
          return "Success"

      def mongo_remove_collection(self,collection_name):

          ### Remove collection
          self.__db.drop_collection(collection_name)
