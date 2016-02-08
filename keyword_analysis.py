import itertools 


filenames = ["berkeley_tags", "cmu_tags", "stanford_tags", "washington_tags"]


def read_tags(filename): 
	all_tags = []
	with open(filename, "r") as f:
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
			for i in xrange(n - 1): 
				tags = combination[0].intersection(combination[i + 1])
				for tag in tags:
					all_in_common.add(tag)
		return all_in_common

	all_tag_list = [set(read_tags("washington_tags")),
					set(read_tags("stanford_tags")),
					set(read_tags("cmu_tags")),
					set(read_tags("berkeley_tags"))]

	write_to_file(get_common_elements(all_tag_list, 4),
		"intersection_four_files")
	write_to_file(get_common_elements(all_tag_list, 3),
		"intersection_three_files")
	write_to_file(get_common_elements(all_tag_list, 2),
		"intersection_two_files")


'''
Look at what is the most common overall.
'''
def count_analysis():
	pass 


if __name__ == "__main__":
	set_analysis()