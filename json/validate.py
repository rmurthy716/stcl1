import json
import jsonschema

schema = open("schema.json").read()

data = open("colossus.json").read()

json_schema = json.loads(schema)
json_data = json.loads(data)


print json_schema
print json_data
jsonschema.validate(json_data, json_schema)
