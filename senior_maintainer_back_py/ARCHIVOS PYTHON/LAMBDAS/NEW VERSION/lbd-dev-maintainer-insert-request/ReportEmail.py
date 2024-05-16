from email.message import EmailMessage
import logging
import smtplib
import sys
logger = logging.getLogger()

class ReportEmail:
    """
    Clase que representa los correos que reportan las variaciones del día

    Attributes:
    ----------
    subject: str
        Asunto del correo
    body: str
        Cuerpo del correo
    data_file: dict
        Información para el archivo adjunto del correo

    Methods:
    --------
    connect_to_smtp(secret)
        Conecta al servicio SMTP de precia

    create_mail_base
        Crea el objeto EmailMessage con los datos básicos para enviar el correo

    attach_file_to_message(message, df_file)
        Adjunta el archivo al mensaje para enviar por el correo

    send_email(smtp_connection, message)
        Envia el objeto EmailMessage construido a los destinatarios establecidos

    run()
        Orquesta los métodos de la clase

    """

    def __init__(self, subject, body, data_file = None) -> None:
        self.subject = subject
        self.body = body
        self.data_file = data_file
        

    def connect_to_smtp(self, secret):
        """Conecta al servicio SMTP de precia con las credenciales que vienen en secret
        Parameters:
        -----------
        secret: dict, required
            Contiene las credenciales de conexión al servicio SMTP

        Returns:
        --------
        Object SMTP
            Contiene la conexión al servicio SMTP
        """
        error_msg = "No fue posible conectarse al relay de correos de Precia"
        try:
            logger.info("Conectandose al SMTP ...")
            connection = smtplib.SMTP(host=secret["server"], port=secret["port"])
            connection.starttls()
            connection.login(secret["user"], secret["password"])
            logger.info("Conexión exitosa.")
            return connection
        except (Exception,) as connect_to_smtp_error:
            exception_line = sys.exc_info()[2].tb_lineno
            current_error = connect_to_smtp_error
            logger.error(current_error.__class__.__name__ + "[" + str(exception_line) + "] " + str(current_error))

    def create_mail_base(self, mail_from, mails_to,mail_to_cc=""):
        """Crea el objeto EmailMessage que contiene todos los datos del email a enviar
        Parameters:
        -------
        mail_from: str, required
            Dirección de correo que envía el mensaje
        mails_to: str, required
            Direcciones de correo destinatario

        Returns:
        Object EmailMessage
            Contiene el mensaje base (objeto) del correo

        Raises:
        ------
        PlataformError
            Si no se pudo crear el objeto EmailMessage

        """
        error_msg = "No se crear el correo para el SMTP"
        try:
            logger.info('Creando objeto "EmailMessage()" con los datos básicos...')
            message = EmailMessage()
            message["Subject"] = self.subject
            message["From"] = mail_from
            message["To"] = mails_to
            if mail_to_cc!="":
                message["Cc"] = mail_to_cc
            message.set_content(self.body)
            logger.info("Mensaje creado correctamente")
            return message
        except Exception as create_mail_base_error:
            exception_line = sys.exc_info()[2].tb_lineno
            current_error = create_mail_base_error
            logger.error(current_error.__class__.__name__ + "[" + str(exception_line) + "] " + str(current_error))


    def send_email(self, smtp_connection, message):
        """Envia el objeto EmailMessage construido a los destinatarios establecidos
        Parameters:
        -----------
        smtp_connection: Object SMTP, required
            Contiene la conexión con el servicio SMTP
        message: Object EmailMessage
            Mensaje para enviar por correo

        Raises:
        -------
        PlataformError
            Si no pudo enviar el correo
            Si no pudo cerrar la conexión SMTP
        """
        logger.info("Enviando Mensaje...")
        try:
            smtp_connection.send_message(message)
        except Exception as send_email_error:
            exception_line = sys.exc_info()[2].tb_lineno
            current_error = send_email_error
            logger.error(current_error.__class__.__name__ + "[" + str(exception_line) + "] " + str(current_error))
        finally:
            try:
                smtp_connection.quit()
                logger.info("Conexión cerrada: SMTP")
            except Exception as send_email_error:
                exception_line = sys.exc_info()[2].tb_lineno
                current_error = send_email_error
                logger.error(current_error.__class__.__name__ + "[" + str(exception_line) + "] " + str(current_error))

