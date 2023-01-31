import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from fuzzywuzzy import process
import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')
stopwords = ['a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an', 'and', 'any', 'are', 'aren', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'couldn', "couldn't", 'd', 'did', 'didn', "didn't", 'do', 'does', 'doesn', "doesn't", 'doing', 'don', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn', "hadn't", 'has', 'hasn', "hasn't", 'have', 'haven', "haven't", 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'isn', "isn't", 'it', "it's", 'its', 'itself', 'just', 'll', 'm', 'ma', 'me', 'mightn', "mightn't", 'more', 'most', 'mustn', "mustn't", 'my', 'myself', 'needn', "needn't", 'no', 'nor', 'not', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 're', 's', 'same', 'shan', "shan't", 'she', "she's", 'should', "should've", 'shouldn', "shouldn't", 'so', 'some', 'such', 't', 'than', 'that', "that'll", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was', 'wasn', "wasn't", 'we', 'were', 'weren', "weren't", 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'won', "won't", 'wouldn', "wouldn't", 'y', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']

def extract_keywords(question, lbl2ent, lbl2rel):
	# remove question mark 
	print("extacting questions ... ")
	if question[-1] == '?':
		question = question[:-1]

	# define question type 
	if 'recommend' in question.lower():
		task = 'recommend'
		predicate = None
		keywords = recommend_question(question,lbl2ent)
	elif 'show me' in question.lower() or 'looks like' in question.lower() or 'look like' in question.lower():
		task = 'multimedia'
		predicate = None
		keywords = multimedia_question(question,lbl2ent)
	else:
		task = 'fact'
		predicate, keywords = fact_question(question,lbl2ent, lbl2rel)

	return task, predicate, keywords


def fact_question(question, lbl2ent, lbl2rel):
	print("factual algorithm is running ...")
	q_tokens = question.split()

	if len(q_tokens) <= 1 :
		return None, None 
	#stop_words = set(stopwords.words('english'))
	q_tokens = [t for t in q_tokens if not t.lower() in stopwords]

	q = " ".join(q_tokens)
	nlp = en_core_web_sm.load()
	pos = [(x.orth_,x.pos_, x.lemma_) for x in [y for y in nlp(question) if not y.is_stop and y.pos_ != 'PUNCT']]
	if pos[0][1] == 'VERB':
		predicate = pos[0][0]
		keywords = []
		for r in pos[1:] :
			keywords.append(r[0])
		keywords = " ".join(keywords)

	else: 
		tokens = question.split("of ")
		predicate = [t for t in tokens[0].split() if not t.lower() in stopwords]
		predicate = " ".join(predicate)
		keywords = tokens[1]

	print("--original predicate and keywords is :", predicate, keywords)

	print("fuzzy matching for predicate =33")
	predicates = list(lbl2rel.keys())
	fuzzy_matching = process.extractOne(predicate, predicates)

	if fuzzy_matching[1] > 60 : 
		predicate = fuzzy_matching[0]
	else: 
		predicate = None
	
	print("fuzzy matching for entity =33")
	entities = list(lbl2ent.keys())
	fuzzy_matching = process.extractOne(keywords, entities)

	if fuzzy_matching[1] > 50 : 
		keywords = fuzzy_matching[0]
	else: 
		keywords = None
	print("--converted to :", predicate, keywords)
	return predicate, keywords


def recommend_question(question,lbl2ent):
	print("recoomendation algorithm is running ...")
	if 'similar' in question :
		tokens = question.split("similar")
		if "," in tokens[1] :
			keywords = tokens[1].split(",")
		else: 
			keywords = token[1]
	else:
		tokens = question.split("like")
		if "," in tokens[1] :
			keywords = tokens[1].split(",")
		else: 
			keywords = token[1]

	if type(keywords) == list:
		print(keywords)
		keywords = keywords[0]

	print("fuzzy matching for entity =33")
	entities = list(lbl2ent.keys())
	fuzzy_matching = process.extractOne(keywords, entities)
	keywords = fuzzy_matching[0]

	return keywords


def multimedia_question(question,lbl2ent):
	print("multimedia algorithm is running ...")
	nlp = en_core_web_sm.load()
	keyword = [x.orth_ for x in [y for y in nlp(question) if not y.is_stop and y.pos_ != 'PUNCT'] if x.pos_ == 'PROPN']
	keyword = " ".join(keyword)
	print(keyword)

	print("fuzzy matching for entity =33")
	entities = list(lbl2ent.keys())
	fuzzy_matching = process.extractOne(keyword, entities)
	keyword = fuzzy_matching[0]

	print(keyword)

	return keyword





