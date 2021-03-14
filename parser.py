import xmltodict
import csv
import json
import xml.etree.ElementTree as ET
import sys
import os
BASE_DIR = os.path.dirname(__file__)
# List of file types
FILE_TYPES = ["xml", "csv"]


def dict_to_lower(data):
    result = {}
    if not isinstance(data, str):
        for k, v in data.items():
            if "@" in k:
                k = k.replace("@", "")
            if isinstance(v, dict):
                result[str(k).lower()] = dict_to_lower(v)
            else:
                result[str(k).lower()] = v
    return result


class Parsing():
    def xml_to_json(self, f):
        tree = ET.parse(f)
        root = tree.getroot()
        data = {"file_name": str(f)}
        data.update(dict_to_lower(xmltodict.parse(ET.tostring(root))))
        l = []
        vehicle = data['transaction']['customer']['units']['vehicle']
        if isinstance(vehicle, dict):
            l.append(vehicle)
        else:
            for item in vehicle:
                l.append(item)

        print(l)
        data['transaction'].update({'vehicles': l})

        del data['transaction']['customer']['units']
        with open(BASE_DIR + "/parsing_result/" + f.split("/")[-1].replace("xml", "json"), "w",
                  encoding="utf-8") as out_file:
            json.dump(data, out_file, ensure_ascii=False)

    def csv_to_json(self, f1, f2):
        files = [f1, f2]
        for f in files:
            jsonArray = []
            result = {"file_name": str(f)}
            # read csv file
            with open(BASE_DIR + "/" + f, encoding='utf-8') as csvf:
                # load csv file data using csv library's dictionary reader
                csvReader = csv.DictReader(csvf)
                # convert each csv row into python dict
                jsonArray.append(result)
                for row in csvReader:
                    # add this python dict to json array
                    jsonArray.append(row)

                # convert python jsonArray to JSON String and write to file
                with open(BASE_DIR + "/parsing_result/" + f.split("/")[-1].replace("csv", "json"), "w",
                          encoding="utf-8") as out_file:
                    json.dump(jsonArray, out_file, ensure_ascii=False)


def main():
    type = str(sys.argv[1])
    parser = Parsing()
    if type in FILE_TYPES:
        if type == "xml":
            try:
                f1 = str(sys.argv[2])
            except:
                raise exec('Please Enter "One" File')
            parser.xml_to_json(f1)
        elif type == "csv":
            try:
                f1 = str(sys.argv[2])
                f2 = str(sys.argv[3])
            except:
                raise exec('Please Enter "Two" Files')
            parser.csv_to_json(f1, f2)
        else:
            raise exec("Not Implemented Yet")
    else:
        raise exec("Please insert valid file ")


if __name__ == "__main__":
    main()
