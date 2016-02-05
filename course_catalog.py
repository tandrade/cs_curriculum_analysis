from bs4 import BeautifulSoup
from collections import Counter
import operator
import os 
import pprint
import requests
import re

cmu_url = "http://coursecatalog.web.cmu.edu/schoolofcomputerscience/courses/"
berkeley_url = "http://guide.berkeley.edu/courses/compsci/"
stanford_url = "http://exploredegrees.stanford.edu/schoolofengineering/computerscience/#courseinventory"
uw_url = "https://www.cs.washington.edu/education/courses"

cmu_filename = "cmu_tags"
berkeley_filename = "berkeley_tags"


ALCHEMY_API_KEY = os.environ["ALCHEMY_API_KEY"] # will fail if environmental variable not set 

alchemy_endpoint = "http://gateway-a.watsonplatform.net/calls/text/TextGetRankedKeywords"


def tag_text_data(txt):
	parameters = {
		"apikey": ALCHEMY_API_KEY,
		"text": txt,
		"outputMode": "json"
	}

	r = requests.get(alchemy_endpoint, params=parameters)
	return [tag_obj["text"] for tag_obj in r.json()["keywords"]]


def write_to_document(tag_list, filename):
	with open(filename, "w") as f:
		for tag in tag_list:
			f.write(tag.encode("utf-8") + "\n")


def parse_cmu_data(filename):
	def clean_text(text):
		# looking for text between first and second "br/"
		first = text[text.index("<br/>") + 5:]
		text = first[:first.index("<br/>")]
		remove_html = re.sub("<[^>]*>", " ", text)
		return re.sub("[ ]+", " ", remove_html).strip()
	
	total_tags = []
	soup = BeautifulSoup(requests.get(cmu_url).text)
	for course_desc in soup.find_all("dl", class_="courseblock"): 
		main_desc = course_desc.find_all("dd")[0]
		cleaned = clean_text(str(main_desc))
		total_tags += tag_text_data(cleaned)
	write_to_document(total_tags, filename)


def parse_berkeley_data(filename):
	def clean_text(text):
		first = text[text.index("<br/>") + 5:]
		text = first[first.index("<br/>") + 5:]
		text = text[:text.index("</span>")]
		remove_html = re.sub("<[^>]*>", " ", text)
		return re.sub("[ ]+", " ", remove_html).strip()

	total_tags = []
	soup = BeautifulSoup(requests.get(berkeley_url).text)
	for index, course_desc in enumerate(soup.find_all("div", class_="coursebody")):
		main_desc = course_desc.find_all("span")[0]
		cleaned = clean_text(str(main_desc))
		total_tags += tag_text_data(cleaned)
	write_to_document(total_tags, filename)


def count_most_popular_tags(filename, count):
	tag_count = Counter() 
	with open(filename) as f:
		for line in f: 
			tag_count[line.lower().replace("\n", "")] += 1
	print sorted(tag_count.items(), key=operator.itemgetter(1), reverse=True)[:count]


if __name__ == "__main__":
	# if not os.path.exists(cmu_filename):
	# 	parse_cmu_data(cmu_filename)
	if not os.path.exists(berkeley_filename):
		parse_berkeley_data(berkeley_filename)
