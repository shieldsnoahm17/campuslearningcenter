from db import connection
######USED ONLY TO TEST SQL CONNECTION#######################
# testInsert = {"table":'appointments',"data":{'AID':'2',"EID":'4'}}
# testUpdate = {"table":'appointments',"data":{'AID':'2'},"updates":{'EID':'15'}}
# testDelete = {"table":'appointments',"data":{"AID":'2'}}
# testSelect = {"table":"appointments",'data':{'AID':'1'},'columns':['AID','PID','apptTime']}
print

conn = connection(host = 'cmsc508.com', database = '22FA_team32', user = 'shieldsn', password = 'V01000930')
# #result = conn.update(testUpdate)
# result = conn.insert(testInsert)
# #result = conn.delete(testDelete)
# #result = conn.select(testSelect)
# print(result)



# cursor = conn.cursor()
# cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'test'")
# result = cursor.fetchall()
table = "test"
query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'"
columns = conn.query({"query":query})
print(columns)


############################
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    table = None
    column = None
    columns = None
    form = InsertForm()

    #query different table choices and choose from table
    query_result = conn.query({"query":"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = \"22FA_team32\""})
    form.table.choices = [(choice[0], choice[0]) for choice in query_result]

    if form.validate_on_submit():
        print("top")
        table = form.table.data
        form = get_columns(form)
        form.column.choices = columns

    elif form.validate_on_submit():
        table = form.table.data
        column = form.column.data

    print(table, column)
    return render_template('insert.html', form = form)

#@app.route('insert/table/<columns>')
def get_columns(form):
    query_result = conn.query({"query":f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'"})
    columns = [(choice[0],choice[0]) for choice in query_result]
    return columns
########################################
