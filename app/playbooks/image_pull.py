class ImagePullPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling an ImagePullBackOff incident.

Focus on:

1. Invalid image names
2. Invalid image tags
3. Missing imagePullSecrets
4. Private registry authentication failures
5. Registry connectivity issues

Suggest Kubernetes-specific remediation steps.

Do not suggest application debugging because the container never started.
"""