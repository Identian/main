import json
import logging
import sys
import mysql.connector
from precia_utils import get_enviroment_variable, get_secret


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def validate_query(entry_query, entry_process, entry_database, consult_verification):
    try:
        database_connection=get_secret(get_enviroment_variable(entry_process+"_DB_CONNECTION"))
        sql_connection = mysql.connector.connect(
            user=database_connection["username"],
            password=database_connection["password"],
            host=database_connection["host"],
            port=int(database_connection["port"]),
            database=entry_database
        )
        if sql_connection.is_connected():
            sql_connection.get_warnings = True
            sql_cursor = sql_connection.cursor(dictionary=True)
            try:
                sql_cursor.execute(entry_query)
                consult_verification["rowcount"] = sql_cursor.rowcount
            except mysql.connector.Error as err:
                if err.errno == 1064:
                    consult_verification["msg_error"] = err.msg
                else:
                    raise
        else:
            logger.info("No se ha podido conectar a la base de datos. Conexión erronea o cerrada.")
            consult_verification["msg_error"] = "No se ha podido conectar a la base de datos. Conexión erronea o cerrada."
    except Exception as lambda_handler_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = lambda_handler_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))
    finally:
        sql_connection.rollback()
        sql_cursor.close()
        sql_connection.close()
    return consult_verification

#HTTP/POST
def lambda_handler(event, context):
    try:
        #data_entry = json.loads(event["body"])
        data_entry = event
        entry_query = data_entry["query"]
        entry_process = data_entry["database"].split(':')[0]
        entry_database = data_entry["database"].split(':')[1]
        consult_verification = {
            "rowcount":0,
            "msg_error":""
        }
        consult_verification=validate_query(entry_query, entry_process,entry_database, consult_verification)
    except Exception as lambda_handler_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = lambda_handler_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))
    return {
        'statusCode': 200,
        'body': json.dumps(consult_verification)
    }