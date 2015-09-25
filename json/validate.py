import json
import jsonschema
import argparse

parser = argparse.ArgumentParser(description='Target json file to be validated.')
parser.add_argument("inputFile", help="Input file to validate")
args = parser.parse_args()

schema = open("schema.json").read()

data = open(args.inputFile).read()

json_schema = json.loads(schema)
json_data = json.loads(data)


print json_schema
print json_data
jsonschema.validate(json_data, json_schema)
