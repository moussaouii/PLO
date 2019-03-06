from rasa_nlu.model import Interpreter

class NluParser(object):

    def __init__(self, path_model):
        """"
        create an Interpreter object from the model that can parse messages
        :param path to the folder of model
        """
        self._interpreter = Interpreter.load(path_model)

    def parse_msg(self, msg):
        """"
        parse a message using Interpreter object
        :param the message
        :return parse result
        """
        return self._interpreter.parse(msg)






