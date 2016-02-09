from bs4 import BeautifulSoup
from collections import Counter
import operator
import os 
import re
import requests

import tag_utils


cmu_url = "http://coursecatalog.web.cmu.edu/schoolofcomputerscience/courses/"
berkeley_url = "http://guide.berkeley.edu/courses/compsci/"
stanford_url = "http://exploredegrees.stanford.edu/schoolofengineering/computerscience/#courseinventory"
uw_url = "https://www.cs.washington.edu/education/courses"

data_dir = "data"

cmu_filename = os.path.join(data_dir, "cmu_tags")
berkeley_filename = os.path.join(data_dir, "berkeley_tags")
stanford_filename = os.path.join(data_dir, "stanford_tags")
uw_filename = os.path.join(data_dir, "washington_tags")


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
		total_tags += tag_utils.tag_text_data(cleaned)
	tag_utils.write_to_document(total_tags, filename)


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
		total_tags += tag_utils.tag_text_data(cleaned)
	tag_utils.write_to_document(total_tags, filename)


def parse_stanford_data(filename):
	def clean_text(text):
		remove_html = re.sub("<[^>]*>", " ", text)
		return re.sub("[ ]+", " ", remove_html).strip()

	total_tags = []
	soup = BeautifulSoup(requests.get(stanford_url).text)
	for course_desc in enumerate(soup.find_all("p", class_ ="courseblockdesc")):
		cleaned = clean_text(str(course_desc))
		total_tags += tag_utils.tag_text_data(cleaned)
	tag_utils.write_to_document(total_tags, filename)


def parse_washington_data(filename):
	def clean_text(text): 
		remove_html = re.sub("<[^>]*>", " ", text)
		return re.sub("[ ]+", " ", remove_html).strip()

	total_tags = [] 
	soup = BeautifulSoup(requests.get(uw_url).text)

	'''
	Due to parsing failures for the html on this page (seems to be missing a </div> for one course 
	listing), the logic for this site is a little stranger. Course titles and course descriptions
	are both marked by a trailing </a></span> tag. Splitting the text of the page by this substring produces a 
	list of titles and descriptions. Could send these to be tagged independently, but to reduce the number of 
	calls for tagging, appending 2 chunks of text at a time and sending that to be tagged. In most cases,
	this will be "title and description pairing" as we would like. However, it is not guaranteed, since
	not all courses have descriptions. 

	For now, this is fine, because sending unrelated chunks of text as one piece of text will not 
	affect tagging. However, if in the future, you want to do some kind of analysis where the unit is a 
	cohesive course (with title+description), this will not work. 

	Hopefully by that time UW will have fixed its website.  

	''' 

	course_content = str(soup.find_all("div", class_="view-content")[0])
	# get rid of a header that sneaks in this way 
	course_content = course_content[course_content.index("</h3>") + 5:]


	total_tags = []
	course_desc = "" 
	for index, course_bloc in enumerate(course_content.split("</a></span>")):
		course_desc += clean_text(course_bloc)

		# tagger likely sensitive to punctuation -- titles do not have punctuation. 
		# If there's no punctation at the end of the substring, add it. 
		if course_desc[-1:] not in [".", "?", "!"]:
			course_desc += ". "
		if index % 2 == 1: 
			total_tags += tag_utils.tag_text_data(course_desc)
			course_desc = ""

	tag_utils.write_to_document(total_tags, filename)


def count_most_popular_tags(filename, count):
	tag_count = Counter() 
	with open(filename) as f:
		for line in f: 
			tag_count[line.lower().replace("\n", "")] += 1
	print sorted(tag_count.items(), key=operator.itemgetter(1), reverse=True)[:count]


if __name__ == "__main__":
	if not os.path.exists(cmu_filename):
		parse_cmu_data(cmu_filename)
	if not os.path.exists(berkeley_filename):
		parse_berkeley_data(berkeley_filename)
	if not os.path.exists(stanford_filename):
		parse_stanford_data(stanford_filename)
	if not os.path.exists(uw_filename):
		parse_washington_data(uw_filename)
