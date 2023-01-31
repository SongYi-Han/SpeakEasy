import json
import rdflib
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDFS, SKOS


wd = Namespace('http://www.wikidata.org/entity/')
wdt = Namespace('http://www.wikidata.org/prop/direct/')
wikibase = Namespace('http://wikiba.se/ontology#')
bd =Namespace('http://www.bigdata.com/rdf#')


def answer(keyword, graph, lbl2ent):
	print("looking for answer with image.json")
	f = open('data/images.json')
	img = json.load(f)

	s = lbl2ent[keyword] 

	query_template = "SELECT ?item WHERE {{ <{}> <http://www.wikidata.org/prop/direct/P345> ?item . }}".format(s)
	qres = graph.query(query_template)
	for row in qres:
		img_id = str(row.item)

	for i in img:
		if img_id in i["cast"]:
			url = i["img"]
			break
	url = url.rstrip(".jpg")

	answer = "Here you go :) image:"+url

	return answer
