from pymongo import MongoClient


class Mongo(object):

    def __init__(self, db_uri, db_name):
        """
        initiate connection to database MongoDB(In our case MongoDB Atlas)
        and access to database
        :param db_uri: MongoDB URI (in our case  URI connection string for connecting to the Atlas cluster )
        :param db_name: database name
        """
        self._client = MongoClient(db_uri)
        self._db = self._client[db_name]

    def insert_result(self, result):
        """
        insert the result in database
        :param parse result
        :return (inserted_id, acknowledged)
          -acknowledged the result of an acknowledged write operation .
          -inserted_id The inserted document’s _id.
        """
        return self._db.results.insert_one(result)

