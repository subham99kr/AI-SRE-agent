from app.models.evidence import Evidence


class MetricsClassifier:

    @staticmethod
    def classify(
        evidence: Evidence
    ) -> str:

        metrics = evidence.metrics

        #
        # CPU
        #

        cpu = metrics.get("cpu", {})

        if cpu:

            highest = max(cpu.values())

            if highest > 0.90:

                return "HIGH_CPU"

        #
        # Error Rate
        #

        errors = metrics.get(
            "error_rate",
            {}
        )

        if any(v > 0.1 for v in errors.values()):

            return "HIGH_ERROR_RATE"

        #
        # Latency
        #

        latency = metrics.get(
            "latency_p95"
        )

        if latency and latency > 1.5:

            return "HIGH_LATENCY"

        return "HEALTHY"