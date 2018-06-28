import pickle
import nltk
import spacy
from math import ceil

VOCAB   = 'data/obj/vocab.pkl'
LEMMA   = 'data/obj/lemma.pkl'
PENN    = 'data/obj/penn_tagset.pkl'
HEDGES  = 'data/obj/hedges.pkl'
FACT    = 'data/obj/factives.pkl'
ASSERT  = 'data/obj/assertives.pkl'
IMPLS   = 'data/obj/implicatives.pkl'
RPRTS   = 'data/obj/reports.pkl'
ENTAIL  = 'data/obj/entailments.pkl'
SUBJ    = 'data/obj/subjectives.pkl'
POLAR   = 'data/obj/polarity.pkl'

OUT_VEC = 'data/obj/vectors.pkl'

def load_obj(loc):
    with open(loc, 'rb') as inp:
        return(pickle.load(inp))


hyland_hedges = load_obj(HEDGES)
assertives = load_obj(ASSERT)
entailments= load_obj(ENTAIL)
factives=load_obj(FACT)
karttunen_implicatives=load_obj(IMPLS)
report_set=load_obj(RPRTS)  
polarity=load_obj(POLAR)
penn_tagset = load_obj(PENN)
factives = load_obj(FACT)
subjectives = load_obj(SUBJ)



P = {'positive':0, 'negative':1, 'both':2, 'neutral':3}


vectors = []
with open('dst.tsv', 'r') as out:
	count = 0
	for line in out:
		line = line.split('\t')
		if(count ==30):
			break
		count += 1
		str_before_bias = line[8].strip().split()
		myWord = line[6].strip().lower()
		if(len(myWord.split())>1):
			continue
		if len(str_before_bias)<1:
			continue
		if len(str_before_bias)>5 or 'http' in str_before_bias:
			continue
		toks = nltk.word_tokenize(line[8])
		for token in toks:
			token = token
			vector = []

#			 1.  * Word
			vector.append(token)
				
#			 2.	Lemma
			lemma = nltk.stem.WordNetLemmatizer().lemmatize(token).lower()
			vector.append(lemma)
		
			# 3.  * POS

			# 4.  * POS-1
			index = toks.index(token)
			tags = nltk.pos_tag(toks)
			pos = tags[index][1]
			vector.append(pos) #pos

			try:
				pos = tags[index-1][1]
				vector.append(pos) #pos-1
			except:
				vector.append(0) #unknown 

			try:
				pos = tags[index-2][1]
				vector.append(pos) #pos-2
			except:
				vector.append(0) #unknown 
			
			try:
				pos = tags[index+1][1]
				vector.append(pos) #pos+1
			except:
				vector.append(0) #unknown 

			try:
				pos = tags[index+2][1]
				vector.append(pos) #pos+2
			except:
				vector.append(0) #unknown 

			# 8.	Position in sentence {start:0, mid:1, end:2}
			segment = ceil(len(toks)/3)
			position = 0
			try:
				if index > segment and index <= segment*2:
					position = 1
				elif index > segment*2:
					position = 2
				vector.append(position)
			except:
				vector.append(0) #unknown

			# 9.	Hedge {true:1, false:0}
	
			if token in hyland_hedges:
				vector.append(1)
			else:
				vector.append(0)

			# 10. * Hedge in context
			context = [] # 2 words before and after index
			try:
				context.append(toks[index-2].strip().lower())
			except:
				context.append(0) #None

			try:
				context.append(toks[index-1].strip().lower())
			except:
				context.append(0) #None

			try:
				context.append(toks[index+1].strip().lower())
			except:
				context.append(0) #None

			try:
				context.append(toks[index+2].strip().lower())
			except:
				context.append(0) #None
	
			value = 0
			for text in context:
				if text in hyland_hedges:
					value = 1
					break
			vector.append(value)

			# 11. * Factive verb
			if token in factives:
				vector.append(1)
			else:
				vector.append(0)

			# 12. * Factive verb in context
			value = 0
			for text in context:
				if text!=None and text in factives:
					value = 1
					break
			vector.append(value)

			# 13. * Assertive verb

			if token in assertives:
				vector.append(1)
			else:
				vector.append(0)

			# 14. * Assertive verb in context
			value = 0
			for text in context:
				if text!=None and text in assertives:
					value = 1
					break
			vector.append(value)

			# 15.   Implicative verb
			karttunen_implicatives = load_obj(IMPLS)

			if token in karttunen_implicatives:
				vector.append(1)
			else:
				vector.append(0)

			# 16. * Implicative verb in context
			value = 0
			for text in context:
				if text!=None and text in karttunen_implicatives:
					value = 1
					break
			vector.append(value)

			# 17. * Report verb
			report_set = load_obj(RPRTS)

			if token in report_set:
				vector.append(1)
			else:
				vector.append(0)

			# 18.   Report verb in context
			value = 0
			for text in context:
				if text!=None and text in report_set:
					value = 1
					break
			vector.append(value)

			# 19. * Entailment
			entailments = load_obj(ENTAIL)

			if token in entailments:
				vector.append(1)
			else:
				vector.append(0)

			# 20. * Entailment in context
			value = 0
			for text in context:
				if text!=None and text in entailments:
					value = 1
					break
			vector.append(value)

			# 21. * Strong subjective
			subjectives = load_obj(SUBJ)

			try:
				if subjectives[token]['type'] == 'strongsubj':
					vector.append(1)
				else:
					vector.append(0)
			except:
				vector.append(0)

			# 22.   Strong subjective in context
			value = 0
			for text in context:
				try:
					if text!=None and subjectives[text]['type'] == 'strongsubj':
						value=1
						break
				except:
					pass
			vector.append(value)

			# 23. * Weak subjective
			try:
				if subjectives[token]['type'] == 'weaksubj':
					vector.append(1)
				else:
					vector.append(0)
			except:
				vector.append(0)

			# 24. * Weak subjective in context
			value = 0
			for text in context:
				try:
					if text!=None and subjectives[text]['type'] == 'weaksubj':
						value=1
						break
				except:
					pass
			vector.append(value)

			# 25.   Polarity 
			P = {'positive':0, 'negative':1, 'both':2, 'neutral':3}
			try:
				vector.append(P[subjectives[text]['pol']])
			except:
				vector.append(P['both'])

			# 26. * Positive word
			polarity = load_obj(POLAR)

			try:
				if polarity[token]=='positive':
					vector.append(1)
				else:
					vector.append(0)
			except:
				vector.append(0)

			# 27. * Positive word in context
			value = 0
			for text in context:
				try:
					if text!=None and polarity[token]=='positive':
						value=1
						break
				except:
					pass
			vector.append(value)

			# 28. * Negative word
			try:
				if polarity[token]=='negative':
					vector.append(1)
				else:
					vector.append(0)
			except:
				vector.append(0)

			# 29. * Negative word in context
			value = 0
			for text in context:
				try:
					if text!=None and polarity[token]=='negative':
						value=1
						break
				except:
					pass
			vector.append(value)

			# 30. * Grammatical relation
			nlp = spacy.load('en_core_web_sm')

	
			# 31.   Bias lexicon
			# 32. * Collaborative feature
		
	#			bias_value
			if(token.lower()==myWord):
				vector.append(1)
			else:
				vector.append(0)
			vectors.append(vector)
with open('vectors.tsv','w') as vect:
	for vector in vectors:
		line='\t'.join(str(col) for col in vector)
		vect.write(line+"\n")
