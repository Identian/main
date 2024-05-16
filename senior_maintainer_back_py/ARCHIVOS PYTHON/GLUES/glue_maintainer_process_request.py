import sys
import boto3
from dateutil import tz
import datetime as dt
import logging
import pymysql.cursors
from email_utils.email_utils import *
from awsglue.utils import getResolvedOptions
from precia_utils.precia_logs import setup_logging
from precia_utils.sql_client import getSecret

logger = setup_logging()
logger.setLevel(logging.INFO)


def get_enviroment_variable(variable):
    variable_value = getResolvedOptions(sys.argv, [variable])
    return variable_value[variable]


def get_bogota_current_time():
    try:
        logger.info('Configurando la hora Colombia.')
        bog_time_today = dt.datetime.now(
            tz=tz.gettz('America/Bogota')).replace(tzinfo=None)
        logger.info('La fecha y hora actual de bogotá es -> ' +
                    bog_time_today.strftime("%Y-%m-%d %H:%M:%S"))
        return bog_time_today
    except Exception as set_diff_time_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = set_diff_time_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))
        pass


def send_final_mail(request_information, response_status):
    try:
        logger.info("Iniciando envío de mensaje.")
        report_date = get_bogota_current_time()
        subject = "[MAINTAINER REQUEST] {} Respuesta de solicitud - Mantenedor Precia".format(request_information["REQUEST_ID"])
        body = f"Se ha procesado la solicitud con el siguiente resultado:\n\n\
            DESCRIPCIÓN DE SOLICITUD:{request_information['REQUEST_DESCRIPTION']}\n\
            ESTADO:{request_information['REQUEST_STATUS']}\n\
            MENSAJE DE RESPUESTA:{request_information['REQUEST_MESSAGE']}\n\
            REGISTROS AFECTADOS:{response_status['rowcount']}\n\
            REGISTROS ESPERADOS A AFECTAR:{request_information['RECORDS_TO_AFFECT']}\n\
            SOLICITADO POR:{request_information['REQUESTER_EMAIL']}\n\
            APROBADO POR:{request_information['APPROVER_EMAIL']}\n\n\n\
            Mensaje enviado por servicio Mantenedor Precia a la fecha y hora {report_date.strftime('%Y-%m-%d %H:%M:%S')}"
        email = ReportEmail(subject, body)
        smtp_connection = email.connect_to_smtp(getSecret(get_enviroment_variable("SMTP_CREDENTIALS")))
        message = email.create_mail_base(get_enviroment_variable('MAINTAINER_MAIL'),request_information['REQUESTER_EMAIL'])
        email.send_email(smtp_connection, message)
    except Exception as send_final_mail_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = send_final_mail_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))
    


def process_request(request_information, request_decision, process_datetime):
    max_minutes = int(get_enviroment_variable('RESQUEST_TIMEOUT'))
    process_request_info = {
        "new_request_process_datetime": "",
        "new_request_status": "",
        "new_request_message": "",
        "request_hash_key": request_information["REQUEST_HASH_KEY"],
        "request_intdate": request_information["REQUEST_INTDATE"]
    }
    response_status={"rowcount": 0, "msg": ""}
    update_query = "UPDATE MAINTAINER_REQUEST SET REQUEST_PROCESS_DATETIME='{new_request_process_datetime}', REQUEST_STATUS='{new_request_status}', REQUEST_MESSAGE='{new_request_message}' WHERE REQUEST_HASH_KEY='{request_hash_key}' AND REQUEST_INTDATE={request_intdate}"
    try:
        if request_information['REQUEST_STATUS'] == str('SOLICITADO'):
            process_request_info["new_request_process_datetime"] = process_datetime.strftime(
                "%Y-%m-%d %H:%M:%S")
            process_request_info["new_request_status"] = "RECHAZADO"
            if (process_datetime >= request_information["REQUEST_DATETIME"]+dt.timedelta(minutes=max_minutes)):
                reject_by_hash_expired_msg = "La solicitud ha sido rechazada: El tiempo de la solicitud se venció."
                logger.info(f"{reject_by_hash_expired_msg}")
                process_request_info["new_request_message"] = reject_by_hash_expired_msg
            else:
                if str.lower(request_decision) == "true":
                    request_list = list(filter(None,list(map(lambda item: item[1:] if item.startswith('\n') else item,str(request_information["REQUEST_QUERY"]).split(';')))))
                    response_status = execute_request_query(
                        request_list, request_information["DATABASE_NAME"], int(request_information["RECORDS_TO_AFFECT"]))
                    if response_status["msg"] == "succeed":
                        process_request_info["new_request_status"] = "APROBADO"
                        approved_request_msg = "La solicitud ha sido aprobada: Se aprobó la solictud y se proceso correctamente."
                        process_request_info["new_request_message"] = approved_request_msg
                        logger.info(f"{approved_request_msg}")
                    elif response_status["rowcount"] > 0 and response_status["msg"] != "":
                        error_request_msg = "La solicitud ha generado un error al procesar: El numero de registros a afectar y el numero de registros en la solicitud no coincide. rowcount:" + \
                            str(response_status["rowcount"])
                        logger.info(f"{error_request_msg}")
                        process_request_info["new_request_message"] = error_request_msg
                        process_request_info["new_request_status"] = "ERROR"
                    else:
                        error_request_msg = "La solicitud ha generado un error al procesar: Se ha generado un error al intentar ejecutar el query de la solicitud."
                        logger.info(f"{error_request_msg}")
                        process_request_info["new_request_message"] = error_request_msg + str(
                            " -> {:3000}...".format(response_status["msg"]))
                        process_request_info["new_request_status"] = "ERROR"
                elif str.lower(request_decision) == "false":
                    reject_request_msg = "La solicitud ha sido rechazada: El autorizador denegó la solicutd. No se realiza la acción en base de datos."
                    logger.info(f"{reject_request_msg}")
                    process_request_info["new_request_message"] = reject_request_msg
                else:
                    error_request_msg = "La solicitud ha generado un error al procesar: Se ha intentado acceder sin informar la acción correctamente (approved debe ser 'true' o 'false')."
                    logger.info(f"{error_request_msg}")
                    process_request_info["new_request_message"] = error_request_msg
                    process_request_info["new_request_status"] = "ERROR"
            update_query = update_query.format(**process_request_info)
            execute_maintainer_query(update_query)
            request_information["REQUEST_STATUS"] = process_request_info["new_request_status"]
            request_information["REQUEST_MESSAGE"] = process_request_info["new_request_message"]
            request_information["REQUEST_PROCESS_DATETIME"] = process_datetime
            send_final_mail(request_information, response_status)
        else:
            logger.info(
                f"La solicitud ya ha sido procesada y su estado actual es: {request_information['REQUEST_STATUS']}.")
    except Exception as process_request_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = process_request_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))


def execute_request_query(query_list, database_entry, records):
    response_status = {"rowcount": 0, "msg": ""}
    entry_process = database_entry.split(':')[0]
    entry_database = database_entry.split(':')[1]
    environment_configuration_name = entry_process+"_DB_CONNECTION"
    database_connection = getSecret(get_enviroment_variable(environment_configuration_name))
    try:
        connection = pymysql.connect(host=database_connection["host"],
                                     port=int(database_connection["port"]),
                                     user=database_connection["username"],
                                     password=database_connection["password"],
                                     database=entry_database,
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor_connection = connection.cursor()
        query_index = 1
        for query_entry in query_list:
            cursor_connection.execute(query_entry)
            if cursor_connection.rowcount > 0:
                response_status["rowcount"] += cursor_connection.rowcount
            query_index+=1
        if response_status["rowcount"] == records:
            connection.commit()
            response_status["msg"] = "succeed"
        else:
            connection.rollback()
            logger.info(f"Error en el query numero: {query_index}")
            response_status["msg"] = "Solictud erronea: El numero de registros no coincide."
    except Exception as execute_request_query_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = execute_request_query_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))
        connection.rollback()
        response_status["msg"] = current_error.args[1]
    else:
        cursor_connection.close()
        connection.close()
    return response_status


def execute_maintainer_query(query):
    response = {}
    try:
        connection = pymysql.connect(host=getSecret(get_enviroment_variable("MAINTAINER_CREDENTIALS"))["host"],
                                     port=int(getSecret(get_enviroment_variable("MAINTAINER_CREDENTIALS"))["port"]),
                                     user=getSecret(get_enviroment_variable("MAINTAINER_CREDENTIALS"))["username"],
                                     password=getSecret(get_enviroment_variable("MAINTAINER_CREDENTIALS"))["password"],
                                     database="maintainer",
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor_connection = connection.cursor()
        cursor_connection.execute(query)
        logger.info("Solicitudes encontradas: "+str(cursor_connection.rowcount))
        if cursor_connection.rowcount > 0:
            response = cursor_connection.fetchone()
            logger.info("Se encontro: "+str(response))
    except pymysql.Error as execute_maintainer_query_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = execute_maintainer_query_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))
    else:
        connection.commit()
        cursor_connection.close()
        connection.close()
    logger.info("Enviando: "+ str(response))
    return response


def main():
    request_hash_key = get_enviroment_variable('HASH_KEY')
    request_decision = get_enviroment_variable('APPROVED')
    process_datetime = get_bogota_current_time()
    load_request_query = f"SELECT * FROM MAINTAINER_REQUEST WHERE REQUEST_HASH_KEY='{request_hash_key}'"
    request_information = execute_maintainer_query(load_request_query)
    if not request_information:
        logger.info("La solicitud no existe.")
    else:
        process_request(request_information,
                        request_decision, process_datetime)
    logger.info("Finalizando programa")


main()
