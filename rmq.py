"""
This module provides classes for interacting with RabbitMQ.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple
import requests
import pika

from logutils import get_logger
from utils import get_env_var

logger = get_logger(__name__)

HTTP_API_HOST = get_env_var("RABBITMQ_HTTP_API_HOST", "localhost")
HTTP_API_PORT = int(get_env_var("RABBITMQ_HTTP_API_PORT", 15672))
HTTP_API_TLS_PORT = int(get_env_var("RABBITMQ_HTTP_API_TLS_PORT", 15671))
HTTP_API_PROTOCOL = (
    "https"
    if get_env_var("RABBITMQ_HTTP_API_USE_TLS", "false").lower() == "true"
    else "http"
)
HTTP_API_BASE_URL = f"{HTTP_API_PROTOCOL}://{HTTP_API_HOST}:{HTTP_API_PORT}/api"

AMQP_HOST = get_env_var("RABBITMQ_AMQP_HOST", "localhost")
AMQP_PORT = int(get_env_var("RABBITMQ_AMQP_PORT", 5672))
AMQP_TLS_PORT = int(get_env_var("RABBITMQ_AMQP_TLS_PORT", 5671))
AMQP_USE_TLS = get_env_var("RABBITMQ_AMQP_USE_TLS", "false").lower() == "true"
AMQP_DEFAULT_VHOST = get_env_var("RABBITMQ_AMQP_DEFAULT_VHOST", "%2F")

SUPERADMIN_USER = get_env_var("RABBITMQ_SUPERADMIN_USERNAME", "guest")
SUPERADMIN_PASS = get_env_var("RABBITMQ_SUPERADMIN_PASSWORD", "guest")


class RabbitMQ(ABC):
    """
    Abstract base class for RabbitMQ components.
    """

    _auth: Tuple[str, str] = (SUPERADMIN_USER, SUPERADMIN_PASS)

    @classmethod
    def get_auth(cls) -> Tuple[str, str]:
        """
        Return the private authentication credentials.
        """
        return cls._auth

    @abstractmethod
    def create(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def read(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def update(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def delete(self, *args, **kwargs) -> Any:
        pass


class VHost(RabbitMQ):
    def __init__(self, vhost: str = AMQP_DEFAULT_VHOST):
        """
        Initialize the VHost with a specific virtual host.
        """
        self.vhost = vhost

    def create(
        self, name: str, timeout: int = 10
    ) -> Tuple[Optional[Tuple[int, dict]], Optional[str]]:
        """
        Create a virtual host.
        """
        try:
            logger.debug(
                "Attempting to create a virtual host with name: %s, timeout: %s",
                name,
                timeout,
            )
            response = requests.put(
                f"{HTTP_API_BASE_URL}/vhosts/{name}",
                auth=self.get_auth(),
                timeout=timeout,
            )
            response.raise_for_status()
            logger.info(
                "Virtual host created successfully with status code: %s",
                response.status_code,
            )
            return (
                response.status_code,
                response.json() if response.content else None,
            ), None
        except requests.exceptions.RequestException as e:
            logger.error("Failed to create virtual host '%s': %s", name, e)
            return None, str(e)

    def read(
        self, name: str, timeout: int = 10
    ) -> Tuple[Optional[Tuple[int, dict]], Optional[str]]:
        """
        Read details of a virtual host.
        """
        try:
            logger.debug(
                "Attempting to read details of virtual host with name: %s, timeout: %s",
                name,
                timeout,
            )
            response = requests.get(
                f"{HTTP_API_BASE_URL}/vhosts/{name}",
                auth=self.get_auth(),
                timeout=timeout,
            )
            response.raise_for_status()
            logger.info(
                "Details of virtual host retrieved successfully with status code: %s",
                response.status_code,
            )
            return (
                response.status_code,
                response.json() if response.content else None,
            ), None
        except requests.exceptions.RequestException as e:
            logger.error("Failed to read details of virtual host '%s': %s", name, e)
            return None, str(e)

    def update(self, name: str, new_name: str) -> Tuple[None, str]:
        """
        Update a virtual host (not supported in RabbitMQ).
        """
        logger.error(
            "Updating virtual host name is not supported in RabbitMQ. Current name: %s, New name: %s",
            name,
            new_name,
        )
        return None, "Updating vhost name is not supported in RabbitMQ."

    def delete(
        self, name: str, timeout: int = 10
    ) -> Tuple[Optional[Tuple[int, dict]], Optional[str]]:
        """
        Delete a virtual host.
        """
        try:
            logger.debug(
                "Attempting to delete virtual host with name: %s, timeout: %s",
                name,
                timeout,
            )
            response = requests.delete(
                f"{HTTP_API_BASE_URL}/vhosts/{name}",
                auth=self.get_auth(),
                timeout=timeout,
            )
            response.raise_for_status()
            logger.info(
                "Virtual host deleted successfully with status code: %s",
                response.status_code,
            )
            return (
                response.status_code,
                response.json() if response.content else None,
            ), None
        except requests.exceptions.RequestException as e:
            logger.error("Failed to delete virtual host '%s': %s", name, e)
            return None, str(e)


class Exchange(RabbitMQ):
    def __init__(self, vhost: str = AMQP_DEFAULT_VHOST):
        """
        Initialize the Exchange with a specific virtual host.
        """
        self.vhost = vhost

    def create(
        self, name: str, type: str, vhost: str, durable: bool = True, timeout: int = 10
    ) -> Tuple[Optional[Tuple[int, dict]], Optional[str]]:
        """
        Create an exchange.
        """
        try:
            logger.debug(
                "Attempting to create an exchange with name: %s, type: %s, vhost: %s, durable: %s, timeout: %s",
                name,
                type,
                vhost,
                durable,
                timeout,
            )
            data = {"type": type, "durable": durable}
            response = requests.put(
                f"{HTTP_API_BASE_URL}/exchanges/{vhost}/{name}",
                json=data,
                auth=self.get_auth(),
                timeout=timeout,
            )
            response.raise_for_status()
            logger.info(
                "Exchange created successfully with status code: %s",
                response.status_code,
            )
            return (
                response.status_code,
                response.json() if response.content else None,
            ), None
        except requests.exceptions.RequestException as e:
            logger.error("Failed to create exchange '%s': %s", name, e)
            return None, str(e)

    def read(
        self, name: str, vhost: str, timeout: int = 10
    ) -> Tuple[Optional[Tuple[int, dict]], Optional[str]]:
        """
        Read details of an exchange.
        """
        try:
            logger.debug(
                "Attempting to read details of exchange with name: %s, vhost: %s, timeout: %s",
                name,
                vhost,
                timeout,
            )
            response = requests.get(
                f"{HTTP_API_BASE_URL}/exchanges/{vhost}/{name}",
                auth=self.get_auth(),
                timeout=timeout,
            )
            response.raise_for_status()
            logger.info(
                "Details of exchange retrieved successfully with status code: %s",
                response.status_code,
            )
            return (
                response.status_code,
                response.json() if response.content else None,
            ), None
        except requests.exceptions.RequestException as e:
            logger.error("Failed to read details of exchange '%s': %s", name, e)
            return None, str(e)

    def update(
        self, name: str, new_name: str, new_type: Optional[str] = None
    ) -> Tuple[None, str]:
        """
        Update an exchange (not supported in RabbitMQ).
        """
        logger.error(
            "Updating exchange is not supported in RabbitMQ. Current name: %s, New name: %s, New type: %s",
            name,
            new_name,
            new_type,
        )
        return None, "Updating exchange name or type is not supported in RabbitMQ."

    def delete(
        self, name: str, vhost: str, timeout: int = 10
    ) -> Tuple[Optional[Tuple[int, dict]], Optional[str]]:
        """
        Delete an exchange.
        """
        try:
            logger.debug(
                "Attempting to delete exchange with name: %s, vhost: %s, timeout: %s",
                name,
                vhost,
                timeout,
            )
            response = requests.delete(
                f"{HTTP_API_BASE_URL}/exchanges/{vhost}/{name}",
                auth=self.get_auth(),
                timeout=timeout,
            )
            response.raise_for_status()
            logger.info(
                "Exchange deleted successfully with status code: %s",
                response.status_code,
            )
            return (
                response.status_code,
                response.json() if response.content else None,
            ), None
        except requests.exceptions.RequestException as e:
            logger.error("Failed to delete exchange '%s': %s", name, e)
            return None, str(e)


class Queue(RabbitMQ):
    def __init__(self, vhost: str = AMQP_DEFAULT_VHOST):
        """
        Initialize the Queue with a specific virtual host.
        """
        self.vhost = vhost

    def create(
        self, name: str, vhost: str, durable: bool = True, timeout: int = 10
    ) -> Tuple[Optional[Tuple[int, dict]], Optional[str]]:
        """
        Create a queue.
        """
        try:
            logger.debug(
                "Attempting to create a queue with name: %s, vhost: %s, durable: %s, timeout: %s",
                name,
                vhost,
                durable,
                timeout,
            )
            data = {"durable": durable}
            response = requests.put(
                f"{HTTP_API_BASE_URL}/queues/{vhost}/{name}",
                json=data,
                auth=self.get_auth(),
                timeout=timeout,
            )
            response.raise_for_status()
            logger.info(
                "Queue created successfully with status code: %s", response.status_code
            )
            return (
                response.status_code,
                response.json() if response.content else None,
            ), None
        except requests.exceptions.RequestException as e:
            logger.error("Failed to create queue '%s': %s", name, e)
            return None, str(e)

    def read(
        self, name: str, vhost: str, timeout: int = 10
    ) -> Tuple[Optional[Tuple[int, dict]], Optional[str]]:
        """
        Read details of a queue.
        """
        try:
            logger.debug(
                "Attempting to read details of queue with name: %s, vhost: %s, timeout: %s",
                name,
                vhost,
                timeout,
            )
            response = requests.get(
                f"{HTTP_API_BASE_URL}/queues/{vhost}/{name}",
                auth=self.get_auth(),
                timeout=timeout,
            )
            response.raise_for_status()
            logger.info(
                "Details of queue retrieved successfully with status code: %s",
                response.status_code,
            )
            return (
                response.status_code,
                response.json() if response.content else None,
            ), None
        except requests.exceptions.RequestException as e:
            logger.error("Failed to read details of queue '%s': %s", name, e)
            return None, str(e)

    def update(self, name: str, new_name: str) -> Tuple[None, str]:
        """
        Update a queue (not supported in RabbitMQ).
        """
        logger.error(
            "Updating queue is not supported in RabbitMQ. Current name: %s, New name: %s",
            name,
            new_name,
        )
        return None, "Updating queue name is not supported in RabbitMQ."

    def delete(
        self, name: str, vhost: str, timeout: int = 10
    ) -> Tuple[Optional[Tuple[int, dict]], Optional[str]]:
        """
        Delete a queue.
        """
        try:
            logger.debug(
                "Attempting to delete queue with name: %s, vhost: %s, timeout: %s",
                name,
                vhost,
                timeout,
            )
            response = requests.delete(
                f"{HTTP_API_BASE_URL}/queues/{vhost}/{name}",
                auth=self.get_auth(),
                timeout=timeout,
            )
            response.raise_for_status()
            logger.info(
                "Queue deleted successfully with status code: %s", response.status_code
            )
            return (
                response.status_code,
                response.json() if response.content else None,
            ), None
        except requests.exceptions.RequestException as e:
            logger.error("Failed to delete queue '%s': %s", name, e)
            return None, str(e)


class Producer(RabbitMQ):
    """
    Component for publishing messages to an exchange using AMQP.
    """

    def __init__(
        self,
        host: str = AMQP_HOST,
        port: int = AMQP_TLS_PORT if AMQP_USE_TLS else AMQP_PORT,
        vhost: str = AMQP_DEFAULT_VHOST,
    ):
        """
        Initialize the Producer with a connection to RabbitMQ.
        """
        self.vhost = vhost
        logger.debug(
            "Initializing Producer with host: %s, port: %s, vhost: %s",
            host,
            port,
            vhost,
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                virtual_host=vhost,
                credentials=pika.PlainCredentials(*self.get_auth()),
                ssl_options=pika.SSLOptions() if AMQP_USE_TLS else None,
            )
        )
        self.channel = self.connection.channel()
        logger.info("Producer initialized successfully.")

    def publish(self, exchange_name: str, routing_key: str, message: str) -> dict:
        """
        Publish a message to a specific exchange with a routing key.
        """
        try:
            logger.debug(
                "Publishing message to exchange: %s, routing_key: %s",
                exchange_name,
                routing_key,
            )
            self.channel.basic_publish(
                exchange=exchange_name, routing_key=routing_key, body=message
            )
            logger.info("Message published successfully to exchange: %s", exchange_name)
            return {"status": "success", "message": "Message published"}
        except Exception as e:
            logger.error(
                "Failed to publish message to exchange '%s': %s", exchange_name, e
            )
            return {"status": "error", "message": str(e)}

    def close(self) -> None:
        """
        Close the connection to RabbitMQ.
        """
        logger.debug("Closing Producer connection.")
        self.connection.close()
        logger.info("Producer connection closed successfully.")

    def __del__(self):
        """
        Ensure the connection is closed when the object is deleted.
        """
        if self.connection.is_open:
            self.close()
