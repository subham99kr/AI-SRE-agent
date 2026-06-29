import socket


START_PORT = 9091

END_PORT = 9999


class PortManager:

    @staticmethod
    def is_free(
        port: int
    ) -> bool:

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:

            sock.bind(
                (
                    "127.0.0.1",
                    port
                )
            )

            return True

        except OSError:

            return False

        finally:

            sock.close()

    @classmethod
    def next_free_port(
        cls
    ) -> int:

        for port in range(

            START_PORT,

            END_PORT + 1

        ):

            if cls.is_free(
                port
            ):

                return port

        raise RuntimeError(

            "No free ports available."

        )