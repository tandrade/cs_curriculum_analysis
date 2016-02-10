import re
import requests 
import os 

import tag_utils


# copypasta from website -- TODO: parse into nice endpoint + params 
coursera_endpoint = "https://www.coursera.org/api/catalogResults.v2?q=subdomainByDomain&languages=en&domainId=computer-science&limit=8&debug=false&fields=domains.v1(description,name),subdomains.v1(id,name),courses.v1(name,description),onDemandSpecializations.v1(name,description),specializations.v1(name,description),partners.v1(name)&includes=courseId,domainId,onDemandSpecializationId,specializationId,subdomainId,courses.v1(partnerIds),onDemandSpecializations.v1(partnerIds),specializations.v1(partnerIds)"

udacity_endpoint = "https://www.udacity.com/public-api/v0/courses"

# FIXME: DRY this logic up between this file and course_catalog.py 
data_dir = "data"

coursera_filename = os.path.join(data_dir, "coursera_tags")
udacity_filename = os.path.join(data_dir, "udacity_tags")


# TODO: DRY this up
def clean_text(text): 
		remove_html = re.sub("<[^>]*>", " ", text)
		return re.sub("[ ]+", " ", remove_html).strip()

def get_coursera_tags(filename): 
	r = requests.get(coursera_endpoint, verify=False)
	if 'linked' not in r.json(): 
		return [] 
	courses = r.json()['linked']['courses.v1']
	total_tags = [] 
	for course in courses:
		full_description = "{}. {}".format(course['name'].encode("utf-8"), 
									clean_text(course['description']).encode("utf-8"))
		total_tags += tag_utils.tag_text_data(full_description)
	tag_utils.write_to_document(total_tags, filename)


def get_udacity_tags(filename):
	r = requests.get(udacity_endpoint)
	courses = r.json()['courses']
	total_tags = [] 
	for course in courses: 
		if 'Non-Tech' in course['tracks']:
			continue
		full_description = "{}. {}".format(course['title'].encode("utf-8"), 
										clean_text(course['summary']).encode("utf-8"))
		total_tags += tag_utils.tag_text_data(full_description)
	tag_utils.write_to_document(total_tags, filename)


if __name__ == "__main__":
	if not os.path.exists(coursera_filename):
		get_coursera_tags(coursera_filename)
	if not os.path.exists(udacity_filename):
		get_udacity_tags(udacity_filename)
