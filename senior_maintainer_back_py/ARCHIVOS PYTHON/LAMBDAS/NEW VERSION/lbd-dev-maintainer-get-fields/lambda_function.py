import json
import logging
import sys
import mysql.connector
from precia_utils import get_enviroment_variable, get_secret

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def execute_query(entry_query):
    try:
        response = []
        sql_connection = mysql.connector.connect(
            user=get_secret(get_enviroment_variable(
                "MAINTAINER_CONNECTION"))["username"],
            password=get_secret(get_enviroment_variable(
                "MAINTAINER_CONNECTION"))["password"],
            host=get_secret(get_enviroment_variable(
                "MAINTAINER_CONNECTION"))["host"],
            port=int(get_secret(get_enviroment_variable(
                "MAINTAINER_CONNECTION"))["port"]),
            database=get_secret(get_enviroment_variable(
                "MAINTAINER_CONNECTION"))["dbname"]
        )
        if sql_connection.is_connected():
            sql_connection.get_warnings = True
            sql_cursor = sql_connection.cursor(dictionary=True)
            try:
                sql_cursor.execute(entry_query)
                response = sql_cursor.fetchall()
                logger.info(str(response))
            except mysql.connector.Error as err:
                exception_line = sys.exc_info()[2].tb_lineno
                current_error = err
                logger.error(current_error.__class__.__name__ +
                             "[" + str(exception_line) + "] " + str(current_error))
            sql_cursor.close()
            sql_connection.close()
        else:
            logger.info("No se ha podido conectar a la base de datos. Conexión erronea o cerrada.")
    except Exception as execute_query_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = execute_query_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))
    return response


# HTTP/GET
def lambda_handler(event, context):
    try:
        get_approve_users_query = "SELECT * FROM APPROVE_USER"
        get_database_name_query = "SELECT * FROM DATABASE_MAINTAINER"
        fields = {}
        logger.info("Cargando lista de usuarios...")
        approve_user_list = execute_query(get_approve_users_query)
        if not approve_user_list:
            logger.info("No se pudieron cargar los usuarios.")
        logger.info("Cargando lista de esquemas disponibles...")
        database_list = execute_query(get_database_name_query)
        if not approve_user_list:
            logger.info("No se pudieron cargar las bases de datos.")
        fields["database_list"] = database_list
        fields["approve_user_list"] = approve_user_list
    except Exception as lambda_handler_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = lambda_handler_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))
    return {
        'statusCode': 200,
        'body': json.dumps(fields)
    }