import rdflib
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDFS, SKOS
import random

wd = Namespace('http://www.wikidata.org/entity/')
wdt = Namespace('http://www.wikidata.org/prop/direct/')
wikibase = Namespace('http://wikiba.se/ontology#')
bd =Namespace('http://www.bigdata.com/rdf#')


def answer(predicate, keyword, graph, lbl2ent, lbl2rel):
	print("looking for answer by sparql")
	answer_auto = ["Hey, the {} of {} is {} !", "Hey hey, the {} of {} is {} ❤", "It's not easy to answer, but I think the {} of {} is {} :D", "I found the {} of {} is {}! interesting 8)"]
	answer_auto_fail = ["Sorry I haven't learned about the {} of {} yet (T_T) .. seems its not existing in my database" , "I'm sorry I couldn't find the answer, I think there is no information about the {} of {} in wikidata yet ..", "hmmm it's difficult question... and I cant answer the {} of {} ... sorry", "Could you ask me another question ?the {} of {} is a bit hard question to me.. "]

	if predicate and keyword:
		print(predicate)
		print(keyword)

		p = lbl2rel[predicate]
		s = lbl2ent[keyword]

		query_template = "SELECT DISTINCT ?answer ?label WHERE {{ <{}> <{}> ?answer. ?answer rdfs:label ?label. }}".format(s, p)
		qres = graph.query(query_template)
		for row in qres:
			answer = row.label


		try : 
			answer_template = random.sample(answer_auto,1)[0].format(predicate, keyword, answer)
		
		except UnboundLocalError :
			answer_template = random.sample(answer_auto_fail,1)[0].format(predicate, keyword)	
		'''
		if answer == "":
			answer_template = random.sample(answer_auto_fail,1)[0]

		answer_template = random.sample(answer_auto,1)[0].format(predicate, keyword, answer)
		'''
	else :
		answer_template = "Sorry I couldn't find the result "
	
	
	return answer_template
