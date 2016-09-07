import csv
import math

class Group:

	def __init__(self, name):
		self.name = name
		self.article_ids = []

	def add_article(self, article_id):
		self.article_ids.append(article_id)

class Article:

	def __init__(self, id):
		self.id = id
		self.words = {}

	def add_word(self, word_id, count):
		self.words[word_id] = count

def parse_groups(groups_file):
	groups = []
	with open(groups_file, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for name in reader:
			groups.append(Group(name))
	return groups

def parse_labels(label_file, groups):
	articles = {}
	with open(label_file, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			article_id = row[0]
			group_id = row[1]
			articles[article_id] = Article(article_id)
			groups[group_id - 1].add_article(article_id)
	return articles
	
def parse_data(data_file, articles):
	with open(data_file, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			article_id = row[0]
			word_id = row[1]
			count = row[2]
			articles[article_id].add_word(word_id, count)

def init():
	data_file = 'p2_data/data50.csv'
	label_file = 'p2_data/label.csv'
	groups_file = 'p2_data/groups.csv'
	groups = parse_groups(groups_file)
	articles = parse_labels(label_file, groups)
	parse_data(data_file, articles)
	return groups, articles

def jaccard_sim(article1, article2):
	words1 = set(article1.words.keys())
	words2 = set(article2.words.keys())
	common_words = words1 & words2
	num = 0.0
	for word in common_words:
		num += min(article1.words[word], article2.words[word])
	union_words = words1 | words2
	denom = 0.0
	for word in union_words:
		c1 = 0
		if word in words1:
			c1 = article1.words[word]
		c2 = 0
		if word in words2:
			c2 = article2.words[word]
		denom += max(c1, c2)
	return num/denom

def l2_sim(article1, article2):
	words1 = set(article1.words.keys())
	words2 = set(article2.words.keys())
	union_words = words1 | words2
	sum = 0
	for word in union_words:
		c1 = 0
		if word in words1:
			c1 = article1.words[word]
		c2 = 0
		if word in words2:
			c2 = article2.words[word]
		sum += (c1 - c2) * (c1 - c2)
	return math.sqrt(sum)

def cosine_sim(article1, article2):
	words1 = set(article1.words.keys())
	words2 = set(article2.words.keys())
	common_words = words1 & words2
	num = 0.0
	for word in common_words:
		num += article1.words[word] * article2.words[word]
	den1 = 0.0
	for word in words1:
		c1 = article1.words[word]
		den1 += c1 * c1
	den2 = 0.0
	for word in words2:
		c2 = article2.words[word]
		den2 += c2 * c2	
	denom = math.sqrt(den1) * math.sqrt(den2)
	return num/denom

def main():
	groups, articles = init()
	n = 20
    group_sim_jac = [[0 for i in range(n)] for j in range(n)] 
    group_sim_l2 = [[0 for i in range(n)] for j in range(n)] 
    group_sim_cos = [[0 for i in range(n)] for j in range(n)] 

	for i in range(n):
		group_i = groups[i]
		for j in range(i, n):
			group_j = groups[j]
			sum_jac = sum_l2 = sum_cos = 0
			int num = len(group_i.article_ids) * len(group_j.article_ids)
			for ai in group_i.article_ids:
				for aj in group_j.article_ids:
					sum_jac += jaccard_sim(ai, aj)
					sum_l2 += l2_sim(ai, aj)
					sum_cos += cosine_sim(ai, aj)
			group_sim_jac[i][j] = group_sim_jac[j][i] = sum_jac/num
			group_sim_l2[i][j] = group_sim_l2[j][i] = sum_l2/num
			group_sim_cos[i][j] = group_sim_cos[j][i] = sum_cos/num

if __name__ == '__main__':
	main()
