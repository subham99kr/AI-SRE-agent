import requests

from app.config.prometheus_config import (
    PROMETHEUS_URL,
    PROMETHEUS_TIMEOUT
)


class PrometheusTool:

    def __init__(self):

        self.base_url = PROMETHEUS_URL

    ####################################################################
    #
    # Generic Query
    #
    ####################################################################

    def query(
        self,
        promql: str
    ) -> list[dict]:

        response = requests.get(

            f"{self.base_url}/api/v1/query",

            params={
                "query": promql
            },

            timeout=PROMETHEUS_TIMEOUT
        )

        response.raise_for_status()

        result = response.json()

        if result["status"] != "success":

            return []

        return result["data"]["result"]

    ####################################################################
    #
    # CPU Usage
    #
    ####################################################################

    def cpu_usage(
        self,
        namespace: str
    ) -> list[dict]:

        return self.query(
            f"""
sum by (pod)
(
    rate(
        container_cpu_usage_seconds_total{{
            namespace="{namespace}",
            container!="",
            image!=""
        }}[5m]
    )
)
"""
        )

    ####################################################################
    #
    # Memory Usage
    #
    ####################################################################

    def memory_usage(
        self,
        namespace: str
    ) -> list[dict]:

        return self.query(
            f"""
sum by (pod)
(
    container_memory_working_set_bytes{{
        namespace="{namespace}",
        container!="",
        image!=""
    }}
)
"""
        )

    ####################################################################
    #
    # Restart Count
    #
    ####################################################################

    def restart_count(
        self,
        namespace: str
    ) -> list[dict]:

        return self.query(
            f"""
kube_pod_container_status_restarts_total{{
    namespace="{namespace}"
}}
"""
        )

    ####################################################################
    #
    # Request Rate
    #
    ####################################################################

    def request_rate(
        self,
        service: str
    ):

        return self.query(
            f"""
    sum by (handler)
    (
        rate(
            http_requests_total{{
                service="{service}"
            }}[5m]
        )
    )
    """
        )

    ####################################################################
    #
    # P95 Latency
    #
    ####################################################################

    def latency_p95(
        self,
        service: str
    ) -> list[dict]:

        return self.query(
            f"""
histogram_quantile(
    0.95,
    sum by (le)
    (
        rate(
            http_request_duration_seconds_bucket{{
                service="{service}"
            }}[5m]
        )
    )
)
"""
        )

####################################################################
#
# Request Count
#
####################################################################

    def request_count(
        self,
        service: str
    ) -> list[dict]:

        return self.query(
            f"""
    sum by (handler)
    (
        http_requests_total{{
            service="{service}"
        }}
    )
    """
        )
####################################################################
#
# Error Rate
#
####################################################################

    def error_rate(
        self,
        service: str
    ) -> list[dict]:

        return self.query(
            f"""
    sum by (handler)
    (
        rate(
            http_requests_total{{
                service="{service}",
                status=~"5.."
            }}[5m]
        )
    )
    """
        )
    
####################################################################
#
# Average Latency
#
####################################################################

    def latency_average(
        self,
        service: str
    ) -> list[dict]:

        return self.query(
            f"""
    (
    sum by (handler)
    (
        rate(
            http_request_duration_seconds_sum{{
                service="{service}"
            }}[5m]
        )
    )
    )
    /
    (
    sum by (handler)
    (
        rate(
            http_request_duration_seconds_count{{
                service="{service}"
            }}[5m]
        )
    )
    )
    """
        )