from os import path
import json

class CaseNotesSuggester():
    
    def get_neighbors(self, input_notes,label_col, feature_cols, result_count):
    	result=""
    	for col in feature_cols:
    		result=result + col +" "
    	
    	 result=result + input_notes +" "
    	 return result



	def get_neighbors_simple(self, input_notes,label_col, feature_cols, result_count):
			result=""
        	for col in feature_cols:
           		try:
               		result=result + col +" "
            except KeyError:
            	print (col, "feature column not exits in query data",)
         
        result=result + input_notes +" "
        return result
