# |--------------------------------------------------------------------------------------------|
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * |
# |                                                                                            |
# | Module Name: db.py                                                                         |
# | Author: Noah Shields                                                                       |
# | Date: 05/15/2023                                                                           |
# |                                                                                            |
# | Description: This is a subclass of the mySQLConnection class that allows for simple MySQL  |
# |              inserts, deletes, updates, selects, and custom queries                        |
# |                                                                                            |
# | Dependencies: mysql.connector for python, can be downloaded with pip                       |
# |                                                                                            |
# |~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ * ~ *~|
# |--------------------------------------------------------------------------------------------|

from mysql.connector import MySQLConnection

class connection(MySQLConnection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    #takes in a dictionary with three keys: table, columns, and data
    #data represents the WHERE clause (dictionary), and columns represent the projection of the SELECT statement(list)
    def select(self, parameters):    
        table = parameters["table"]
        data = parameters['data']
        columns = ','.join(parameters['columns'])
        condition = ''
        projection = ''

        for key, value in data.items():
            if isinstance(value, str):
                condition += f"{key} = \"{value}\"  AND "
            else:
                condition += f"{key} = {value}  AND "
        condition += " 1=1"

        query = ("SELECT %s FROM %s WHERE %s" % (columns, table, condition))
        print(query)
        #execute query using a cursor
        cursor = self.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    #takes in a dictionary with two keys, data and table, data represents the WHERE clause in the SELECT
    def insert(self, parameters):

        table = parameters["table"]
        data = parameters["data"]
        values = ''


        #gets a comma separated strings of keys (the table columns)
        columns = ','.join(data.keys())
        #vals = ",".join(data.value())

        #parses the data in a way that fits the structure of a sql query
        for item in data.values():
            if isinstance(item, str):
                values += f"\"{item}\","
            else:
                values += str(item) + ','

        #strip the last comma off, two ways to do this
        values = values[:-1]
        #vals = vals.rstrip(vals[-1])

        #creates the query
        query = "INSERT INTO %s(%s) VALUES (%s)" % (table,columns,values,)
        print(query)

        #commit new raw data to the rawData table, runs the query
        cursor = self.cursor()
        cursor.execute(query)
        self.commit()
        
        #store PK of the record and return it
        recent_primary_key = cursor.lastrowid
        return recent_primary_key

    #takes in a single dictionary, that has 3 elements, a dict of updates, a table, and a dictionary of column-value pairs
    # that constructs the WHERE clause 
    def update(self, parameters): 
        data = parameters['data']
        updates = parameters['updates']  
        table = parameters["table"]
        adjustment = ''
        condition = ''

        #puts key value pairs in a query like string for the SET clause
        for key, value in updates.items():
            print(key, value)
            if isinstance(value, str):
                adjustment += f"{key} = \"{value}\","
            else:
                adjustment += f"{key} = {value},"
            
        adjustment = adjustment[:-1]
    

        #puts key value pairs in a query like string for the WHERE clause
        for key, value in data.items():
            if isinstance(value, str):
                condition += f"{key} = \"{value}\"  AND "
            else:
                condition += f"{key} = {value}  AND "
        condition += " 1=1"

        query = ("UPDATE %s SET %s WHERE %s" % (table, adjustment, condition))
        print(query)
        #execute query, commit, and return success
        cursor = self.cursor()
        cursor.execute(query)
        self.commit()
        result = "Success"
        return result




    #takes in a dictionary with two keys, table and data. data represents the WHERE clause in the DELETE query
    def delete(self, parameters):
        table = parameters['table']
        delete = parameters['data']
        condition = ''

        for key, value in delete.items():
            if isinstance(value, str):
                condition += f"{key} = \"{value}\"  AND "
            else:
                condition += f"{key} = {value}  AND "
        condition += " 1=1"

        query = ("DELETE FROM %s WHERE %s" % (table, condition,))

        #execute query, commit, and return success
        cursor = self.cursor()
        cursor.execute(query)
        self.commit()
        result = "Success"
        return result

    def reset(self):
        query = ("CALL reset_all_tables()")

        #execute query, commit, and return success
        cursor = self.cursor()
        cursor.execute(query)
        self.commit()
        result = "Database reset successful"
        return result
    
    #used for a general query, takes in a dict {"query":desired_query}
    def query(self, parameters):
        query = parameters["query"]
        cursor = self.cursor()
        cursor.execute(query)
        print(query)
        result = cursor.fetchall()
        return result
        



        


