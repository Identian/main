import json
import logging
import sys
from dateutil import tz
import datetime as dt
import hashlib
import mysql.connector
from precia_utils import get_enviroment_variable, get_secret
from ReportEmail import ReportEmail


logger = logging.getLogger()
logger.setLevel(logging.INFO)

response_msg = "No se realizó correctamente el envío de la solicitud."
request_is_inserted=False

def get_bogota_current_time():
    try:
        logger.info('Configurando la hora Colombia.')
        bog_time_today = dt.datetime.now(tz=tz.gettz('America/Bogota')).replace(tzinfo=None)
        logger.info('La fecha y hora actual de bogotá es -> '+bog_time_today.strftime("%Y-%m-%d %H:%M:%S"))
        return bog_time_today
    except Exception as set_diff_time_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = set_diff_time_error
        logger.error(current_error.__class__.__name__ + "[" + str(exception_line) + "] " + str(current_error))
        pass


def execute_query(entry_query):
    try:
        sql_connection = mysql.connector.connect(
            user=get_secret(get_enviroment_variable(
                "MAINTAINER_CONNECTION"))["username"],
            password=get_secret(get_enviroment_variable(
                "MAINTAINER_CONNECTION"))["password"],
            host=get_secret(get_enviroment_variable(
                "MAINTAINER_CONNECTION"))["host"],
            port=int(get_secret(get_enviroment_variable(
                "MAINTAINER_CONNECTION"))["port"]),
            database="maintainer"
        )
        if sql_connection.is_connected():
            sql_connection.get_warnings = True
            sql_cursor = sql_connection.cursor(dictionary=True)
            try:
                sql_cursor.execute(entry_query)
            except mysql.connector.Error as err:
                exception_line = sys.exc_info()[2].tb_lineno
                current_error = err
                logger.error(current_error.__class__.__name__ +
                             "[" + str(exception_line) + "] " + str(current_error))
                response_msg = "No se pudo insertar la solicitud. (Error del sistema)"
        else:
            response_msg = "No se pudo establecer la conexión para realizar la solicitud. (Error de conexión)"
    except Exception as execute_query_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = execute_query_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))
        sql_connection.rollback()
        response_msg = "No se pudo insertar la solicitud. (Error del sistema)."
    else:
        sql_connection.commit()
        request_is_inserted=True
        response_msg = "Se agregó la solicitud a la base de datos pero no se envió."
    finally:
        sql_cursor.close()
        sql_connection.close()


def define_transaction_hash(requester_email):
    try:
        logger.info("Inicia proceso de cración de hash unico.")
        date_to_set = get_bogota_current_time()
        data_to_hash = "secret" + requester_email + \
            date_to_set.strftime("%Y%m%y%H%M%S%f")
        transaction_hash = hashlib.sha256(
            data_to_hash.encode('utf-8')).hexdigest()
        transaction_id = "REQUEST_"+date_to_set.strftime("%Y%m%y%H%M%S%f")
        logger.info("Se definió un transaction_id -> "+transaction_id)
        logger.info("Hash y transaction_id generados correctamente.")
        return transaction_hash, transaction_id
    except Exception as define_transaction_hash_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = define_transaction_hash_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))


def insert_transaction(data_entry):
    try:
        logger.info("Inicia proceso de agregar transacción.")
        request_datetime = get_bogota_current_time()
        insert_transaction_query = "INSERT INTO MAINTAINER_REQUEST(REQUEST_QUERY, DATABASE_NAME,RECORDS_TO_AFFECT, REQUESTER_EMAIL, APPROVER_EMAIL, REQUEST_DATETIME, REQUEST_DESCRIPTION, REQUEST_INTDATE, REQUEST_HASH_KEY, REQUEST_ID) VALUES (\"{request_query}\", '{database_name}', {number_of_records}, '{requester_email}', '{approver_email}', '{request_datetime}','{request_description}',{intdate},'{request_hash}','{request_id}')"
        data_entry["number_of_records"] = int(data_entry["number_of_records"])
        data_entry["intdate"] = int(request_datetime.strftime("%Y%m%d"))
        data_entry["request_hash"], data_entry["request_id"] = define_transaction_hash(
            data_entry["requester_email"])
        data_entry["request_datetime"] = request_datetime.strftime("%Y-%m-%d %H:%M:%S")
        insert_transaction_query = insert_transaction_query.format(
            **data_entry)
        logger.info("Insertando nueva solicitud.")
        execute_query(insert_transaction_query)
        if request_is_inserted:
            send_transaction_message(data_entry)
    except Exception as lambda_handler_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = lambda_handler_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))


def send_transaction_message(data_entry):
    logger.info("Enviando correo de aprobación a "+data_entry["approver_email"])
    try:
        data_entry["approve_url"] = str(get_enviroment_variable("APPROVE_URL"))+"?hash_key="+str(data_entry["request_hash"])+"&approved=true"
        data_entry["reject_url"] = str(get_enviroment_variable("APPROVE_URL"))+"?hash_key="+str(data_entry["request_hash"])+"&approved=false"
        subject = "[MAINTAINER REQUEST] {} Solicitud de aprobación - Mantenedor Precia".format(data_entry["request_id"])
        body = "Se ha generado una solicitud de aprobación con las siguientes caracteristicas:\
                Motivo: {request_description}\n\
                Query:{request_query:50}...\n\
                Numero de registros afectados: {number_of_records}\n\
                Base de datos: {database_name}\n\n\n\
                La solicitud la realiza el colaborador {requester_name}. Puede contactarle por medio de un correo electronico a {requester_email}.\n\n\
                Para APROBAR la solicitud, haga ingrese a el siguiente enlace en su navegador: {approve_url}\n\n\
                Este enlace es valido por 20 Minutos desde el envío del correo. Si desea RECHAZAR la solicitud, ignore este mensaje o haga clic en el siguiente enlace:\n\n{reject_url} "
        body = body.format(**data_entry)
        email = ReportEmail(subject, body)
        smtp_connection = email.connect_to_smtp(get_secret(get_enviroment_variable("SMTP_CREDENTIALS")))
        message = email.create_mail_base(get_enviroment_variable("MAINTAINER_EMAIL"), data_entry["approver_email"], data_entry["requester_email"])
        email.send_email(smtp_connection, message)
        response_msg = "Se insertó la solicitud correctamente."
    except Exception as send_new_report_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = send_new_report_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))


def lambda_handler(event, context):
    try:
        logger.info(str(event))
        data_entry = event
        insert_transaction(data_entry)
    except Exception as lambda_handler_error:
        exception_line = sys.exc_info()[2].tb_lineno
        current_error = lambda_handler_error
        logger.error(current_error.__class__.__name__ +
                     "[" + str(exception_line) + "] " + str(current_error))
    return {
        'statusCode': 200,
        'body': json.dumps(response_msg)
    }
