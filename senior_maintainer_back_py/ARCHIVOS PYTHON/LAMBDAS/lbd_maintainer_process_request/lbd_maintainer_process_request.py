import os
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        client = boto3.client('glue')
        glue_job_name = os.environ['JOB_NAME']
        logger.info(str(event))
        url_data_entry = event['queryStringParameters']
        if url_data_entry==None or ("hash_key" not in url_data_entry.keys()) or ("approved" not in url_data_entry.keys()):
            return {
                'statusCode': 200,
                'body': json.dumps('URL invalida.')
            }
        response = client.start_job_run(JobName = glue_job_name, Arguments = {'--HASH_KEY': url_data_entry['hash_key'],'--APPROVED':url_data_entry['approved']})
        job_run_id = response["JobRunId"]
        logger.info(f"Se lanzó el Glue para el procesamiento de solicitudes del mantenedor con el id {job_run_id}.")
        return {
            'statusCode': 200,
            'body': json.dumps('Procesando solicitud...')
        }
    except Exception:
        logger.error("Error iniciando el Glue para procesar las solicitudes del mantenedor.")
        raise