import os
import requests

ALCHEMY_API_KEY = os.environ["ALCHEMY_API_KEY"] # will fail if environmental variable not set 

alchemy_endpoint = "http://gateway-a.watsonplatform.net/calls/text/TextGetRankedKeywords"


def tag_text_data(txt):
	parameters = {
		"apikey": ALCHEMY_API_KEY,
		"text": txt,
		"outputMode": "json"
	}

	r = requests.get(alchemy_endpoint, params=parameters)
	if "keywords" in r.json():
		return [tag_obj["text"] for tag_obj in r.json()["keywords"]]
	# for debugging purposes 
	print r.json() 
	return []


def write_to_document(tag_list, filename):
	with open(filename, "w") as f:
		for tag in tag_list:
			f.write(tag.encode("utf-8") + "\n")
