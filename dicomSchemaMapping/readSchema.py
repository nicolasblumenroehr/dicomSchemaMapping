from jsonschema import validate
import json
import logging
class readSchema():

    def __init__(self, schema, draftDir):
        self.schema=schema
        self.draftDir=draftDir
        try:
            self.definitions=self.schema["definitions"]
        except:
            pass
        self.schemaValidator(schema, draftDir)
        self.searchedSchema=self.searchObject(schema)

    def schemaValidator(self, jsonSchema, draftDir):
        #Validation of the file read in is of proper JSON Format, corresponding to the latest draft supported by this application or earlier
        for i in draftDir:
            j=json.load(open(i))
            try:
                validate(instance=jsonSchema, schema=j)
                logging.info("Schema is valid for draft: %s", str(i))
                break
            except Exception as e:
                logging.warning("Schema is not valid")
                pass

    def searchArray(self, property):
        #print(property)
        if "$ref" in property["items"]:
            if property["items"]["$ref"].startswith("#"):
                keyword=property["items"]["$ref"].split("/")[-1:][0]
                subProperties=self.definitions[keyword]
            else:
                path=property["items"]["$ref"].split("#")[0]
                print(path)
        elif property["items"]["type"] == "array":
            subProperties=[self.searchArray(property["items"])]
        elif property["items"]["type"] == "object":
            subProperties=self.searchObject(property["items"])
        else:
            subProperties=self.searchType(property["items"]["type"])
        return subProperties


    def searchDefinitions(self, definition):
        properties=None
        if "$ref" in definition:
            if definition["$ref"].startswith("#"):
                keyword=definition[1]["$ref"].split("/")[-1:][0]
                subProperties=self.searchDefinitions(self.definitions[keyword])
                properties[definition]=[subProperties]
            else:
                path=definition["$ref"].split("#")[0]
                print(path)
        elif definition["type"] == "array":
            subProperties=self.searchArray(definition)
            properties=subProperties
        elif definition["type"] == "object":
            subProperties=self.searchObject(definition)
            properties=subProperties
        else:
            properties=self.searchType(definition["type"])
        return properties

    def searchObject(self, property):
        properties={}
        for i in property["properties"].items():
            if "$ref" in i[1]:
                if i[1]["$ref"].startswith("#"):
                    keyword=i[1]["$ref"].split("/")[-1:][0]
                    subProperties=self.searchDefinitions(self.definitions[keyword])
                    properties[i[0]]=[subProperties]
                else:
                    path=i[1]["$ref"].split("#")[0]
                    print(path)
            elif i[1]["type"] == "array":
                subProperties=self.searchArray(i[1])
                properties[i[0]]=[subProperties]
            elif i[1]["type"] == "object":
                subProperties=self.searchObject(i[1])
                properties[i[0]]=subProperties
            else:
                properties[i[0]]=self.searchType(i[1]["type"])
        return properties

    def searchType(self, property):
        if property=="integer":
            return "int"
        elif property=="string":
            return "str"
        elif property=="number":
           return "float"
        elif property=="boolean":
           return "bool"
        elif property=="null":
            return None
        elif isinstance(property, list):
            multipleTypes=[]
            for j in property:
                multipleTypes.append(self.searchType(j))
            return tuple(multipleTypes)
        else:
            print(TypeError)