import rdflib
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDFS, SKOS
import numpy as np
import csv
import qna

def load():
	graph = rdflib.Graph()
	graph.parse('data/14_graph.nt', format='turtle')

	#load pretrained embedding
	entity_emb = np.load('data/entity_embeds.npy')
	relation_emb = np.load('data/relation_embeds.npy')

	#load entity, releation
	entity_file = 'data/entity_ids.del'
	relation_file = 'data/relation_ids.del'

	with open(entity_file, 'r') as ifile:
		ent2id = {rdflib.term.URIRef(ent): int(idx) for idx, ent in csv.reader(ifile, delimiter='\t')}
		id2ent = {v: k for k, v in ent2id.items()}

	# build entity-label dictionary
	ent2lbl = {ent: str(lbl) for ent, lbl in graph.subject_objects(RDFS.label)}
	lbl2ent = {lbl: ent for ent, lbl in ent2lbl.items()}


	#butild relation-label dictionary
	predicates = set(graph.predicates())
	predicates_url = [str(i.lstrip("rdflib.term.URIRef(")) for i in predicates]
	rel2lbl = {}
	lbl2rel = {}

	for p in predicates_url[4:] :
		query_template = "SELECT ?label WHERE{{<{}> rdfs:label ?label .FILTER(LANG(?label) = 'en'). }}".format(p)
		qres = graph.query(query_template)
		for row in qres:
			lbl = str(row.label)

		rel2lbl[p] = lbl
		lbl2rel[lbl] = p

	return graph, lbl2ent, ent2lbl, lbl2rel, entity_emb, relation_emb, ent2id, id2ent




