import json
import logging
import sys
import mysql.connector
from precia_utils import get_enviroment_variable, get_secret


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def validate_query(query_list, entry_database, consult_verification):
    try:
        sql_connection = mysql.connector.connect(
            user=get_secret(get_enviroment_variable("FLASH_CONNECTION"))["username"],
            password=get_secret(get_enviroment_variable("FLASH_CONNECTION"))["password"],
            host=get_secret(get_enviroment_variable("FLASH_CONNECTION"))["host"],
            port=int(get_secret(get_enviroment_variable("FLASH_CONNECTION"))["port"]),
            database=entry_database
        )
        logger.info(f'[validate_query] Esta conectado a bd')
        if sql_connection.is_connected():
            sql_connection.get_warnings = True
            sql_cursor = sql_connection.cursor(dictionary=True)
            try:
                for entry_query in query_list:
                    sql_cursor.execute(entry_query)
                    consult_verification["rowcount"] += sql_cursor.rowcount
                logger.info(f'[validate_query] Termina correctamente el conteo de lineas afectadas.')
            except mysql.connector.Error as err:
                logger.error(f'[validate_query] Except de mysql.connector.Error, motivo: {str(err)}')
                if err.errno == 1064:
                    consult_verification["msg_error"] = err.msg
                else:
                    raise
        else:
            logger.info("No se ha podido conectar a la base de datos. Conexión erronea o cerrada.")
            consult_verification["msg_error"] = "No se ha podido conectar a la base de datos. Conexión erronea o cerrada."
    except Exception as lambda_handler_error:
        logger.error(f'[validate_query] Except de metodo, motivo: {str(lambda_handler_error)}')
        exception_line = sys.exc_info()[2].tb_lineno
        consult_verification["msg_error"] = str(lambda_handler_error)
        current_error = lambda_handler_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))
    finally:
        sql_connection.rollback()
        sql_cursor.close()
        sql_connection.close()
    return consult_verification


def format_query_as_list(entry_query):
    return list(map(lambda item: item[1:] if item.startwith('\n') else item,entry_query.split(';')))
    

#HTTP/POST
def lambda_handler(event, context):
    logger.info(f"[lambda_handler] event de llegada: \n{event}")
    try:
        #data_entry = json.loads(event["body"])
        data_entry = event
        entry_query = format_query_as_list(str(data_entry["query"]))
        entry_database = data_entry["database"]
        consult_verification = {
            "rowcount":0,
            "msg_error":""
        }
        consult_verification=validate_query(entry_query, entry_database, consult_verification)
    except Exception as lambda_handler_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = lambda_handler_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))
    return {
        'statusCode': 200,
        'body': json.dumps(consult_verification)
    }