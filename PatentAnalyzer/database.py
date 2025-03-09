
import pandas as pd
#create a class for representing a database. The database is going to be a set of key value pairs stored in a pandas dataframe

class DataBase():
    def __init__(self):
        # initialize a database object with the data represented as a pandas dataframe.
        self._data = pd.DataFrame()

    def get(self, key):
        # get the value for a specific key in the database.
        return self._data[key]

    def put(self, key, value):
        self._data[key] = value
        # add a record to the database by supplying the key.
        return self._data[key]

    def all(self):
        # return all the records in the database. Replace the Null/NaN values with an empty string so that it doesn't error on the frontend.
        return self._data.fillna("")
    
    def delete(self, key):
        self._data.pop(key)
        # delete a specific record in the database by providing a key.
        return self._data.fillna("")

    def clear_all(self):
        # delete all records in the database and replace with an empty pandas dataframe.
        self._data = pd.DataFrame()
        return self._data