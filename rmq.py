"""
This module provides classes for interacting with RabbitMQ.
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple
import requests
import pika

HTTP_API_HOST = os.getenv("RABBITMQ_HTTP_API_HOST", "localhost")
HTTP_API_PORT = int(os.getenv("RABBITMQ_HTTP_API_PORT", 15672))
HTTP_API_TLS_PORT = int(os.getenv("RABBITMQ_HTTP_API_TLS_PORT", 15671))
HTTP_API_PROTOCOL = (
    "https"
    if os.getenv("RABBITMQ_HTTP_API_USE_TLS", "false").lower() == "true"
    else "http"
)
HTTP_API_BASE_URL = f"{HTTP_API_PROTOCOL}://{HTTP_API_HOST}:{HTTP_API_PORT}/api"

AMQP_HOST = os.getenv("RABBITMQ_AMQP_HOST", "localhost")
AMQP_PORT = int(os.getenv("RABBITMQ_AMQP_PORT", 5672))
AMQP_TLS_PORT = int(os.getenv("RABBITMQ_AMQP_TLS_PORT", 5671))
AMQP_USE_TLS = os.getenv("RABBITMQ_AMQP_USE_TLS", "false").lower() == "true"
AMQP_DEFAULT_VHOST = os.getenv("RABBITMQ_AMQP_DEFAULT_VHOST", "%2F")

SUPERADMIN_USER = os.getenv("RABBITMQ_SUPERADMIN_USERNAME", "guest")
SUPERADMIN_PASS = os.getenv("RABBITMQ_SUPERADMIN_PASSWORD", "guest")


class RabbitMQ(ABC):
    """
    Abstract base class for RabbitMQ components.
    Defines CRUD methods that must be implemented by subclasses.
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

    def create(self, name: str, timeout: int = 10) -> Tuple[int, Optional[dict]]:
        """
        Create a virtual host.
        """
        response = requests.put(
            f"{HTTP_API_BASE_URL}/vhosts/{name}",
            auth=self.get_auth(),
            timeout=timeout,
        )
        return response.status_code, response.json() if response.content else None

    def read(self, name: str, timeout: int = 10) -> Tuple[int, Optional[dict]]:
        """
        Read details of a virtual host.
        """
        response = requests.get(
            f"{HTTP_API_BASE_URL}/vhosts/{name}",
            auth=self.get_auth(),
            timeout=timeout,
        )
        return response.status_code, response.json() if response.content else None

    def update(self, name: str, new_name: str) -> None:
        """
        Update a virtual host (not supported in RabbitMQ).
        """
        raise NotImplementedError("Updating vhost name is not supported in RabbitMQ.")

    def delete(self, name: str, timeout: int = 10) -> Tuple[int, Optional[dict]]:
        """
        Delete a virtual host.
        """
        response = requests.delete(
            f"{HTTP_API_BASE_URL}/vhosts/{name}",
            auth=self.get_auth(),
            timeout=timeout,
        )
        return response.status_code, response.json() if response.content else None


class Exchange(RabbitMQ):
    def __init__(self, vhost: str = AMQP_DEFAULT_VHOST):
        """
        Initialize the Exchange with a specific virtual host.
        """
        self.vhost = vhost

    def create(
        self, name: str, type: str, vhost: str, durable: bool = True, timeout: int = 10
    ) -> Tuple[int, Optional[dict]]:
        """
        Create an exchange.
        """
        data = {"type": type, "durable": durable}
        response = requests.put(
            f"{HTTP_API_BASE_URL}/exchanges/{vhost}/{name}",
            json=data,
            auth=self.get_auth(),
            timeout=timeout,
        )
        return response.status_code, response.json() if response.content else None

    def read(
        self, name: str, vhost: str, timeout: int = 10
    ) -> Tuple[int, Optional[dict]]:
        """
        Read details of an exchange.
        """
        response = requests.get(
            f"{HTTP_API_BASE_URL}/exchanges/{vhost}/{name}",
            auth=self.get_auth(),
            timeout=timeout,
        )
        return response.status_code, response.json() if response.content else None

    def update(self, name: str, new_name: str, new_type: Optional[str] = None) -> None:
        """
        Update an exchange (not supported in RabbitMQ).
        """
        raise NotImplementedError(
            "Updating exchange name or type is not supported in RabbitMQ."
        )

    def delete(
        self, name: str, vhost: str, timeout: int = 10
    ) -> Tuple[int, Optional[dict]]:
        """
        Delete an exchange.
        """
        response = requests.delete(
            f"{HTTP_API_BASE_URL}/exchanges/{vhost}/{name}",
            auth=self.get_auth(),
            timeout=timeout,
        )
        return response.status_code, response.json() if response.content else None


class Queue(RabbitMQ):
    def __init__(self, vhost: str = AMQP_DEFAULT_VHOST):
        """
        Initialize the Queue with a specific virtual host.
        """
        self.vhost = vhost

    def create(
        self, name: str, vhost: str, durable: bool = True, timeout: int = 10
    ) -> Tuple[int, Optional[dict]]:
        """
        Create a queue.
        """
        data = {"durable": durable}
        response = requests.put(
            f"{HTTP_API_BASE_URL}/queues/{vhost}/{name}",
            json=data,
            auth=self.get_auth(),
            timeout=timeout,
        )
        return response.status_code, response.json() if response.content else None

    def read(
        self, name: str, vhost: str, timeout: int = 10
    ) -> Tuple[int, Optional[dict]]:
        """
        Read details of a queue.
        """
        response = requests.get(
            f"{HTTP_API_BASE_URL}/queues/{vhost}/{name}",
            auth=self.get_auth(),
            timeout=timeout,
        )
        return response.status_code, response.json() if response.content else None

    def update(self, name: str, new_name: str) -> None:
        """
        Update a queue (not supported in RabbitMQ).
        """
        raise NotImplementedError("Updating queue name is not supported in RabbitMQ.")

    def delete(
        self, name: str, vhost: str, timeout: int = 10
    ) -> Tuple[int, Optional[dict]]:
        """
        Delete a queue.
        """
        response = requests.delete(
            f"{HTTP_API_BASE_URL}/queues/{vhost}/{name}",
            auth=self.get_auth(),
            timeout=timeout,
        )
        return response.status_code, response.json() if response.content else None


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

    def publish(self, exchange_name: str, routing_key: str, message: str) -> dict:
        """
        Publish a message to a specific exchange with a routing key.
        """
        self.channel.basic_publish(
            exchange=exchange_name, routing_key=routing_key, body=message
        )
        return {"status": "success", "message": "Message published"}

    def close(self) -> None:
        """
        Close the connection to RabbitMQ.
        """
        self.connection.close()

    def __del__(self):
        """
        Ensure the connection is closed when the object is deleted.
        """
        if self.connection.is_open:
            self.close()
