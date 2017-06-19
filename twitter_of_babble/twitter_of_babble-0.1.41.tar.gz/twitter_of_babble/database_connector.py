import psycopg2

def pullQuery(dbn,usr,hst,pswrd,stmnt):
    '''
    connects to a postgres database, executes a statement
    and returns results to dict

      [dbn] <str> : database name
      [usr] <str> : username for database
      [hst] <str> : database host
      [pswrd] <str> : password for database user
      [stmnt] <str> : sql statement to pull data

      returns : dict object of query results
    '''


    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}'password='{}'".format(dbn,usr,hst,pswrd))
        cursor = conn.cursor()
        cursor.execute(stmnt)

        column_names = [desc[0] for desc in cursor.description]

        rows = cursor.fetchall()

        tweet_dict = {}
        for i in list(range(len(column_names))):
            tweet_dict['{}'.format(column_names[i])] = [x[i] for x in rows]

    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

    return tweet_dict
