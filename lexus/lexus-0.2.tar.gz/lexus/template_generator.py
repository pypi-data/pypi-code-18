# -*- coding: utf-8 -*-
import argparse

class GenerateTemplateAction(argparse.Action):
    def __init__(self, **kwargs):
        super(GenerateTemplateAction, self).__init__(**kwargs)
    
    def __call__(self, parser, namespace, values, option_strings):
        file_name = values if values is not None else namespace.file_name
        with open(str(file_name) + ".py", "w") as f:
            text = '''# -*- coding: utf-8 -*-
from lexi import lex

def lambda_handler(request, context=None):
intent_name = request['currentIntent']['name']
req = lex.Request(request).to_dict 
if intent_name in globals():
    return globals()[intent_name](req, context).to_dict()
else:
    return lex.ResponseBuilder.elicit_intent("Can't find intent name's function in lambda.")
            '''
            f.write(text)
        print("success to generate " + file_name + '.py')

parser = argparse.ArgumentParser(prog="lexus", description='Tool to generate Lambda function for AWS Lex')
parser.add_argument('-g', nargs="?", dest='file_name', metavar='Generate', type=str, default="lambda_function",
        action=GenerateTemplateAction, 
        help="Generate Lambda function template for AWS Lex in current directory. Enter file name, default is 'lambda_function'")

args = parser.parse_args()
