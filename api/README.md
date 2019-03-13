# REST API of Semantic analyzer 
 The goal of this Api is to receives Json request that contains text from external server and use 
 Rasa NLU to analyze semantically the text and send the result back to server.


## Project architecture
The API receives Json request that contains the user message from external server.
It uses Rasa nlu model to extract the aim or target of the user message (Intent) 
and the useful information from the user message that can be extracted (Entities).
After it stors the results (user message, the intent of the user message, the entities extracted and other information about the request ..)
and sends the intent and the entities extracted to the external server.

![API schema](img_readme/api_schema.png)

## Getting Started
### Prerequisites
- You need Python3 or later and pip to run this project on unix machine.
Python3 and pip can be installed using the following pip command
```
sudo apt-get install python3
sudo apt-get install python3-pip
```
you should  install the duckling pipeline using the following command :

```
sudo docker pull rasa/duckling
```
(Duckling is shipped with modules that parse temporal expressions in English, Spanish, French, Italian and Chinese . It recognizes dates and times described in many ways )

- You need also a mongoDB (in our case we use  MongoDB Atlas a cloud databases)

- You need also a rasa nlu traind model (in this project you find rasa nlu traind model for flight search in **./models/current/nlu**)
but this is generic API and it can work with any rasa nlu model

### Requirements
To install the dependencies of this project (Flask, the dependencies of rasa nlu and spacy ...)
```
pip install -r requirements.txt
```
### Configuration
Before run the code, you should specify some parameters in the file **config.py**  as follows
```
class Config(object):
    """Parent configuration class."""
    DEBUG = False
    TESTING = False
    DB_URI = 'mongodb+srv://user123:user123@cluster0-ph6ze.mongodb.net/test?retryWrites=true'
    PATH_MODEL = './models/current/nlu'
    TOKENS = {
        'hwvTzW7FJTwEA4XTVNxkWRApa0srOQYu':'app1',
        'hq9Nl0W0FhkObivMA8m8WphUjTlacTfG':'app2'
    }


class ProductionConfig(Config):
    """Configurations for production."""
    DB_NAME = 'nlu_results'

class DevelopmentConfig(Config):
    """Configurations for Development, with a separate development database"""
    DEBUG = True
    DB_NAME = 'nlu_dev'


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DB_NAME = 'nlu_test'
```

- **DB_URI** : MongoDB URI (in our case  URI connection string for connecting to the Atlas cluster )
- **PATH_MODEL** : Path to the folder of rasa model 
- **TOKENS** : python dictionary has as key=token and has as value=App identifiant 
  we use the App identifiant when we store result in database
  to differentiate the requests of each application if we have 
  multiple applications that interac with our API
- **DB_NAME** : the name of database we use different name for development, production and test

We use more than one configuration. We have separate configurations 
for the production server and the one used during development and test. We use a default configuration that is always loaded and part of the version control, 
and a separate configuration that overrides the values as necessary  using classes 
and inheritance  as mentioned in the example above


### Running project

you should run this command to launch the duckling container (when you want to use your model):

```
docker run -p 8000:8000 rasa/duckling
```
(In our case we launch duckling in container docker in the port 8000. this is specify in config file 
before model training. So you can change this in the config file)

```
  - name: "ner_duckling_http"
  # url of the running duckling server
  url: "http://0.0.0.0:8000"
```

then you can run this project as follows
```
python app.py
```

**output:**
```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 153-261-373
```


Now you can interact with the API by sending get or post request to the url **adresse_server:port/api/parse**
(in our case http://127.0.0.1:5000/api/prase)
whit content type of **application/json**
and data that contains :
- attribute **message** : the text to prase
- attribute **token** it should be valid token(exists in config file)
- attribute **request_info** (it's not mandatory) it contains info about
        the request of user for example user_id or any other attribute.
 as follows:
```
{
	"message": "Bsr Je veux aller à Auch depuis Nice",
	"token" : "hwvTzW7FJTwEA4XTVNxkWRApa0srOQYu",
	"request_info" : { "user_id" : "1234" }
}
```

If all goes well you should receive a Json response like that:
(the result of the application of the parser of nlu_rasa on the message.)
```
{
    "entities": [
        {
            "confidence": 0.9978343065866314,
            "end": 24,
            "entity": "destination",
            "extractor": "ner_crf",
            "start": 20,
            "value": "auch"
        },
        {
            "confidence": 0.8663632792494916,
            "end": 36,
            "entity": "origin",
            "extractor": "ner_crf",
            "start": 32,
            "value": "nice"
        }
    ],
    "intent": {
        "confidence": 0.9999942840943996,
        "name": "flight_search"
    }
}
```
The API stores in MongoDB Atlas
     -the result  of Semantic analysis
     -the request_info
     -the message
     -app name(each token is associated with an application)
     -the date 
```
{  
   "_id":{  
      "$oid":"5c7efa3642f44b1e74bdfdd9"
   },
   "message":"Bsr Je veux aller à Auch depuis Nice 2019",
   "app_name":"app1",
   "request_info":{  
      "user_id":"1234"
   },
   "date":{  
      "$date":{  
         "$numberLong":"1551825462323"
      }
   },
   "result":{  
      "intent":{  
         "name":"flight_search",
         "confidence":{  
            "$numberDouble":"0.9999942840943996"
         }
      },
      "entities":[  
         {  
            "start":{  
               "$numberInt":"20"
            },
            "end":{  
               "$numberInt":"24"
            },
            "value":"auch",
            "entity":"destination",
            "confidence":{  
               "$numberDouble":"0.9978343065866314"
            },
            "extractor":"ner_crf"
         },
         {  
            "start":{  
               "$numberInt":"32"
            },
            "end":{  
               "$numberInt":"36"
            },
            "value":"nice",
            "entity":"origin",
            "confidence":{  
               "$numberDouble":"0.8663632792494916"
            },
            "extractor":"ner_crf"
         }
      ]
   }
}
```     
     
If someting goes wrong you should receive a Json response that describe the error.
for example :
 
 - If the token isn't valid:
 ``` 
 {
    "error": "invalid token"
 }
 ``` 
 - If the request dosn't contains attribut **message** or **token**
  ```
 {
    "error": "invalid request (request should have attribut message and token)"
 }
  ```

### Test the API with Postman
You can test the api with Postman using this configuration :
![postman test](img_readme/postman_req.png)
### Test the API with Curl
You can test the api with Curl using command as follows :
  ```
curl -d '{"message": "Bsr Je veux aller à Auch depuis Nice 2019",
"token" : "hwvTzW7FJTwEA4XTVNxkWRApa0srOQYu",
"request_info" : { "user_id" : "1234" }
}' -H 'Content-Type: application/json'   http://localhost:5000/api/parse
  ```
### Deployement Herocku 
If you use mongoDB Atlas this project should be deployed in Heroku (Cloud Application Platform)
without problems but not in the free version because the loading of rasa nlu model in the ram requires more than 512 Mb 
while the free version has only 512 Mb of ram

### Autors

- Ismail Moussaoui
- Amine Charifi
- Othmane El Fetnassi
- Youssef Bendagha
- M'hand Glilah
- Marouane Labyad 
