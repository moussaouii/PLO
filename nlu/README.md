# Flybot - Tourism Chatbot

The goal here is to make you familiar with the technicalities regarding the chatbot, so it can extract the right entities and the right intent.

## Getting Started

Start by getting a local copy of the project for development and testing purposes.

### Prerequisites

First, you have to install python 3 or later, and Docker

### Installing

We are using in this projects, among other python libraries, the rasa_nlu library (wich is responsible of training our entity/intent recognition model). To install those libraries, open a shell and tape the following:


```
$ pip install -r requirements.txt
```
here we use the spacy model `fr_core_news_md`  is a statistical model in french, trained on the French Sequoia and WikiNER corpus. Assigns context-specific token vectors, POS tags, dependency parse and named entities. Supports indentification of PER, LOC, ORG and MISC entities. It contains 579k keys, 20k unique vectors (300 dimensions).

in order to let our chatbot recognize the spacy model `fr_core_news_md` as the shortcut `fr`:

```
python -m spacy link fr_core_news_md fr
```

Then install the duckling pipeline using the following command :

```
sudo docker pull rasa/duckling
```
Then run this command to launch the duckling container (when you want to use your model):

```
docker run -p 8000:8000 rasa/duckling
```


## Presenting the rasa_nlu library

Rasa NLU is an open-source tool for intent classification and entity extraction. For example, taking a sentence like

```
"Je veux aller de toulouse à paris ce weekend"
```
and returning structured data like

```
{
  "intent": {
    "confidence": 0.9998878932233402,
    "name": "flight_search"
  },
  "intent_ranking": [
    {
      "confidence": 0.9998878932233402,
      "name": "flight_search"
    },
    {
      "confidence": 0.00010302332102096702,
      "name": "negative"
    },
    {
      "confidence": 8.601318306999593e-06,
      "name": "greet"
    },
    {
      "confidence": 3.149591201931632e-07,
      "name": "bye"
    },
    {
      "confidence": 1.6717821163472018e-07,
      "name": "affirmative"
    }
  ],
  "entities": [
    {
      "confidence": 0.9992337253580568,
      "extractor": "ner_crf",
      "end": 25,
      "start": 17,
      "value": "toulouse",
      "entity": "origin"
    },
    {
      "confidence": 0.9920121427732627,
      "extractor": "ner_crf",
      "end": 33,
      "start": 28,
      "value": "paris",
      "entity": "destination"
    },
    {
      "extractor": "ner_duckling_http",
      "text": "ce weekend",
      "start": 34,
      "value": {
        "from": "2019-03-08T18:00:00.000+01:00",
        "to": "2019-03-11T00:00:00.000+01:00"
      },
      "additional_info": {
        "values": [
          {
            "from": {
              "value": "2019-03-08T18:00:00.000+01:00",
              "grain": "hour"
            },
            "type": "interval",
            "to": {
              "value": "2019-03-11T00:00:00.000+01:00",
              "grain": "hour"
            }
          }
        ],
        "from": {
          "value": "2019-03-08T18:00:00.000+01:00",
          "grain": "hour"
        },
        "to": {
          "value": "2019-03-11T00:00:00.000+01:00",
          "grain": "hour"
        },
        "type": "interval"
      },
      "end": 44,
      "entity": "time",
      "confidence": 1.0
    }
  ],
  "text": "Je veux aller de toulouse à paris ce weekend"
}
```
Here we have trained our chatbot model to recognize, in this example, the intent "flight_search" and its entities ("time", "nb_passengers", "origin", "destination", "discover_category", "one_way", "round_trip", "flexibility")

## Training the model

In order to train our chatbot model to recognize the right itents and the right entities, we just have to launch the following line on a shell

```
$ python nlu_model.py
```
the nlu_model.py uses the "config_spacy.yml" file and a "train_data_res_final.json".
The "nlu_model.py" script contains 3 parts : first part is for training the model based on a data set (in this case "train_data_res_final.json"); the second is for running our model, testing it with some examples; the last one ask the user in the shell to tape a request, then returns a structured data like shown before. At the beginning, only the first part is uncommented, in order to train the model.

The "train_data_res_final.json" is - in our case - the data set in which is based the training; its format is as follow :

```
{
    "rasa_nlu_data": {
        "common_examples": [],
        "regex_features" : [],
        "lookup_tables"  : [],
        "entity_synonyms": []
    }
}
```
Regex features are a tool to help the classifier detect entities or intents and improve the performance.
Synonyms will map extracted entities to the same name, for example mapping “with my wife” to simply "romantic" (arguably).
The common_examples are used to train your model. You should put all of your training examples in the common_examples array. These examples are in the following format:

```
      {
        "entities": [
          {
            "end": 35,
            "entity": "origin",
            "start": 29,
            "value": "Ramsar"
          },
          {
            "end": 55,
            "entity": "destination",
            "start": 48,
            "value": "Guanaja"
          },
          {
            "end": 65,
            "entity": "nb_passengers",
            "start": 56,
            "value": "1"
          },
          {
            "end": 78,
            "entity": "round_trip",
            "start": 66,
            "value": "aller retour"
          }
        ],
        "intent": "flight_search",
        "text": "bonjour J'souhaite un vol de Ramsar destination Guanaja tout seul aller retour"
      },
```

As for the "config_spacy.yml", it specifies the pipelines and the language used to train the model.
In this project, we use the "nlp_spacy" pipeline for recognizing the destinations and origins, the "intent_entity_featurizer_regex" pipeline to create a list of regular expressions defined in the training data format, the "ner_crf" pipeline to implement conditional random fields to do named entity recognition. The "ner_spacy" extract the locations. Finally, the "ner_duckling_http" extract the date time wanted.
