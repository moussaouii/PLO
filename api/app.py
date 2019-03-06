from flask import Flask, request, jsonify
from flask_api import status
from nlu_parser import NluParser
from mongo import Mongo
import datetime
import config


app = Flask(__name__)
#  Load configuration from config.py
app.config.from_object(config.DevelopmentConfig)
#  Load rase nlu model that parse text
run_nul = NluParser(app.config['PATH_MODEL'])
# initialize connection to mongoDB (in our case Atlas MongoDB)
mongo = Mongo(app.config['DB_URI'], app.config['DB_NAME'])


def verfiy_token(token):
    """Verfiy if the token valid or not

        :param  The token from the request(str)

        :return
            bool: return True if the token is valid(exists in key of app.config['TOKENS'])
                  False if not.

    """
    return token in app.config['TOKENS']





@app.route('/api/parse', methods=['GET','POST'])
def prase_msg():
    """
     This function responds to a request get or post for /api/parse
     whit request content type of application/json
     and data that contains :
     - attribute message : the text to prase
     - attribute token it should be valid token(exists in config|"TOKEN"]
     - attribute request_info (it's not mandatory)it contains info about
        the request of user for example user_id or any other attribute.
    :return json reponse that contains the result of the application of
     the parser of nlu_rasa on the message. and save
     -the result
     -the request_info
     -the message
     -app name(each token is associated with an application)
     -the date
    """
    try:
        data = request.json
        if ('message' in data) and ('token' in data):
            message = data["message"]
            token = data["token"]
            request_info = None
            if 'request_info' in data:#if the request info exist
                request_info = data["request_info"]
            if verfiy_token(token) :#if the token valid
                # parse the message
                result = run_nul.parse_msg(message)
                # adapt the format of the results to the API response format
                del result['intent_ranking']
                del result['text']
                # insert the result in MonogoDB
                result_id = mongo.insert_result({
                    "message" : message,
                    "app_name" : app.config['TOKENS'][token],
                    "request_info" : request_info,
                    "date": datetime.datetime.utcnow(),
                    "result": result
                })
                # everything goes well
                return jsonify(result), status.HTTP_200_OK
            else:
                # the token is invalid
                return jsonify({'error' : 'invalid token'}), status.HTTP_401_UNAUTHORIZED
        else:
            #the data of the request dosen't contain : attribute message or attribute token
            return jsonify({'error' : 'invalid request (request should have attribut message and token)'}), status.HTTP_400_BAD_REQUEST
    except Exception as e:
        return jsonify({'error' : str(e)}), status.HTTP_500_INTERNAL_SERVER_ERROR


if __name__ == '__main__':
    app.run()







