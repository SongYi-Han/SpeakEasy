import rdflib
from extract import extract_keywords
import sparql 
import embedding 
import multimedia


def answer(message, graph, lbl2ent,ent2lbl, lbl2rel, entity_emb, relation_emb, ent2id, id2ent):
	print("recieved question:", message)
	task, predicate, keyword = extract_keywords(message, lbl2ent, lbl2rel)

	if task == "fact":
		answer = sparql.answer(predicate, keyword, graph, lbl2ent, lbl2rel)
	elif task == "recommend":
		answer = embedding.answer(keyword, lbl2ent, ent2lbl, ent2id, id2ent, entity_emb)
	elif task == "multimedia":
		answer = multimedia.answer(keyword, graph, lbl2ent)

	print(answer)
	return answer


