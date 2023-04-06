import sys
from typing import Optional

import redis


class Redis:

    @staticmethod
    def connect() -> Optional[redis.client.Redis]:
        try:
            client = redis.Redis(
                host="localhost",
                port=6379,
                db=0,
                socket_timeout=5,
            )
            ping = client.ping()
            if ping is True:
                return redis.Redis(
                    host="localhost",
                    port=6379,
                    db=0,
                    socket_timeout=5,
                )
        except redis.AuthenticationError as e:
            print(e)
            sys.exit(1)
