import rdflib
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDFS, SKOS
import random
from sklearn.metrics import pairwise_distances


wd = Namespace('http://www.wikidata.org/entity/')
wdt = Namespace('http://www.wikidata.org/prop/direct/')
wikibase = Namespace('http://wikiba.se/ontology#')
bd =Namespace('http://www.bigdata.com/rdf#')


def answer(keywords, lbl2ent, ent2lbl, ent2id, id2ent, entity_emb):
	print("looking for answer with embedding")
	answer_auto = ["I think you will like {}, {} and {} based on your taste :)", "I will recommend you {}, {} and {} for you! you will love it !", "Hmm, how about {}, {} and {}?"]
	
	k_entity= lbl2ent[keywords]
	k_id = ent2id[k_entity]
	distances = pairwise_distances(entity_emb[k_id].reshape(1, -1), entity_emb, metric='cosine').flatten()

	most_likely = distances.argsort()

	recomendations = []
	for rank, idx in enumerate(most_likely[0:5]):
		if distances[idx] > 0.00:
			lbl = ent2lbl[id2ent[idx]] 
			recomendations.append(lbl)

	answer_template = random.sample(answer_auto,1)[0].format(recomendations[-1],recomendations[-2],recomendations[-3])

	#answer_template = "I think you will like {}, {} and {}!".format(recomendations[0],recomendations[1],recomendations[2])

	return answer_template
