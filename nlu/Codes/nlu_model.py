from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer, Metadata, Interpreter
from rasa_nlu import config
import pprint
import spacy
import json
import time

start_time = time.time()

print (spacy.load("fr")("hello"))

# entrainement du modele de chatbot
def train_nlu(data, configs, model_dir):
	training_data = load_data(data)
	trainer = Trainer(config.load(configs))
	interpreter = trainer.train(training_data)
	model_dir = trainer.persist("models/nlu", fixed_model_name="chatter")

# lancement du chatbot
def run_nlu():
	interpreter = Interpreter.load('./models/nlu/default/chatter')
	print(json.dumps(interpreter.parse(u"Je cherche un billet de Paris à Perpignan dans une semaine"), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"moscow"), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"Je veux un billet à partir de El Jadida à oujda dans une semaine"), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"Je cherche un billet de naples vers LA dans une semaine pour une personne"), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"rabat"), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"budapest"), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"vers lyon"), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"à partir de rennes"), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"Salut, je veux aller au japon le mois prochain."), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"Salut, je veux aller au japon le mois prochain. des propositions ?"), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"Salut, je cherche un billet de Toulouse à Paris pour 2, dans une semaine."), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"je veux aller à rio en été"), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"j'aimerais bien m'en aller à Moscou pour les jeux olympiques d'hiver"), indent = 2))
	print('   ')
	print(json.dumps(interpreter.parse(u"y a-t-il un vol pour le maroc ce week end pour moins de 100 euros?"), indent = 2))
	print('   ')

# commentez / decommentez les parties que vous souhaitez executer
if __name__ == '__main__':
	train_nlu('./train_data_res_final.json', './config_spacy.yml', './models/nlu')
	#run_nlu()

	## Partie chatbot interactif - à décommenter
	#print('__________________')
	#print('__________________')
	#oui = 0
	#interpreter = Interpreter.load('./models/nlu/default/chatter')
	#while oui == 0:
	#	text = input('Que voulez-vous faire ? \n')
	#	print(json.dumps(interpreter.parse(text), indent = 2))
	#	print('   ')
	
elapsed_time = time.time() - start_time
print('elapsed time is ',elapsed_time)