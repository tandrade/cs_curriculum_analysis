import itertools 
import os


def read_tags(filename): 
	all_tags = []
	# TODO: get a better way of organizing the data filenames 
	with open(os.path.join("data", filename), "r") as f:
		all_tags = f.readlines() 
	return [tag.replace("\n", "").lower().strip() for tag in all_tags]


'''
Look at what is common across different sites. 
''' 
def set_analysis():
	def write_to_file(set_results, filename):
		with open(filename, "w") as f:
			for tag in set_results:
				f.write(tag + "\n")

	def get_common_elements(set_results, n):
		all_in_common = set() 
		for combination in itertools.combinations(set_results, n):
			# get everything after the first entry, but don't exceed the array
			combination_in_common = set()
			combination_in_common = combination[0] 
			for i in xrange(n - 1):
				combination_in_common = combination_in_common.intersection(combination[i + 1])
			for tag in combination_in_common:
				all_in_common.add(tag)
		return all_in_common

	washington_tags = set(read_tags("washington_tags"))
	stanford_tags = set(read_tags("stanford_tags"))
	cmu_tags = set(read_tags("cmu_tags"))
	berkeley_tags = set(read_tags("berkeley_tags"))

	all_tag_list = [	
						washington_tags,
						stanford_tags,
						cmu_tags,
						berkeley_tags
					]

	all_in_common = get_common_elements(all_tag_list, 4)
	three_in_common = get_common_elements(all_tag_list, 3)
	two_in_common = get_common_elements(all_tag_list, 2)


'''
Look at what is the most common overall.
'''
def count_analysis():
	pass 


if __name__ == "__main__":
	set_analysis()