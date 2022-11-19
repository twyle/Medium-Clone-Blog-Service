import logging.config
import os

import boto3
from dotenv import load_dotenv

load_dotenv()


class KinesisFirehoseDeliveryStreamHandler(logging.StreamHandler):
    """This class sends our logs to Amazon Kinesis."""

    def __init__(self):
        """Initialize the firehose stream.."""
        # By default, logging.StreamHandler uses sys.stderr if stream parameter is not specified
        logging.StreamHandler.__init__(self)

        self.__firehose = None
        self.__stream_buffer = []
        self.__aws_key = os.environ["AWS_ACCESS_KEY"]
        self.__aws_secret = os.environ["AWS_ACCESS_SECRET"]
        self.__aws_region = os.environ["AWS_REGION"]

        try:
            self.__firehose = boto3.client(
                "firehose",
                aws_access_key_id=self.__aws_key,
                aws_secret_access_key=self.__aws_secret,
                region_name=self.__aws_region,
            )
        except Exception:
            print("Firehose client initialization failed.")

        self.__delivery_stream_name = os.environ["FIREHOSE_DELIVERY_STREAM"]

    def emit(self, record):
        """Send the formatted log to AWS Firehose."""
        try:
            msg = self.format(record)

            if self.__firehose:
                self.__stream_buffer.append(
                    {"Data": msg.encode(encoding="UTF-8", errors="strict")}
                )
            else:
                stream = self.stream
                stream.write(msg)
                stream.write(self.terminator)

            self.flush()
        except Exception:
            self.handleError(record)

    def flush(self):
        """Flush the log buffer."""
        self.acquire()

        try:
            if self.__firehose and self.__stream_buffer:
                self.__firehose.put_record_batch(
                    DeliveryStreamName=self.__delivery_stream_name,
                    Records=self.__stream_buffer,
                )

                self.__stream_buffer.clear()
        except Exception as e:
            print("An error occurred during flush operation.")
            print(f"Exception: {e}")
            print(f"Stream buffer: {self.__stream_buffer}")
        finally:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()

            self.release()


def create_dev_logger():
    """Create the application logger."""
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
            "json": {
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            },
        },
        "handlers": {
            "standard": {
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
        },
        "loggers": {"": {"handlers": ["standard"], "level": logging.INFO}},
    }

    logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)

    return logger


def create_prod_logger():
    """Create the application logger."""
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
            "json": {
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            },
        },
        "handlers": {
            "standard": {
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
            "kinesis": {
                "class": "api.config.kinesis_config.KinesisFirehoseDeliveryStreamHandler",
                "formatter": "json",
            },
        },
        "loggers": {"": {"handlers": ["kinesis"], "level": logging.INFO}},
    }

    logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)

    return logger


def create_logger(env="development"):
    app_logger = create_dev_logger()
    if env == "production":
        app_logger = create_prod_logger()
    return app_logger


app_logger = create_logger()
