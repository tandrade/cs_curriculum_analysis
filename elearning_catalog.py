import pprint 
import requests 
import os 

import tag_utils


# copypasta from website -- TODO: parse into nice endpoint + params 
coursera_endpoint = "https://www.coursera.org/api/catalogResults.v2?q=subdomainByDomain&languages=en&domainId=computer-science&limit=8&debug=false&fields=domains.v1(description,name),subdomains.v1(id,name),courses.v1(name,description),onDemandSpecializations.v1(name,description),specializations.v1(name,description),partners.v1(name)&includes=courseId,domainId,onDemandSpecializationId,specializationId,subdomainId,courses.v1(partnerIds),onDemandSpecializations.v1(partnerIds),specializations.v1(partnerIds)"


def get_coursera_tags(): 
	r = requests.get(coursera_endpoint, verify=False)
	if 'linked' not in r.json(): 
		return [] 
	courses = r.json()['linked']['courses.v1']
	max_n = 3 
	for index, course in enumerate(courses):
		if index > max_n:
			break 
		pprint.pprint(course)


if __name__ == "__main__":
	get_coursera_tags()
