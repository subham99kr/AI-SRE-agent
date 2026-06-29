from pathlib import Path

import subprocess


class Kubectl:

    def __init__(
        self,
        context: str
    ):

        self.context = context

    def run(
        self,
        *args,
        check=True
    ):

        command = [

            "kubectl",

            "--context",

            self.context,

            *args

        ]

        print()

        print(
            " ".join(command)
        )

        result = subprocess.run(

            command,

            capture_output=True,

            text=True

        )

        if check and result.returncode != 0:

            raise RuntimeError(

                "\n"

                f"Command Failed\n\n"

                f"{' '.join(command)}\n\n"

                f"{result.stderr}"

            )

        return result

    def apply(
        self,
        file: Path
    ):

        print(
            f"Applying {file.name}"
        )

        return self.run(

            "apply",

            "-f",

            str(file)

        )

    def delete(
        self,
        file: Path
    ):

        print(
            f"Deleting {file.name}"
        )

        return self.run(

            "delete",

            "-f",

            str(file),

            check=False

        )

    def exists(

        self,

        resource: str,

        name: str,

        namespace: str | None = None

    ) -> bool:

        command = [

            "get",

            resource,

            name

        ]

        if namespace:

            command.extend(

                [

                    "-n",

                    namespace

                ]

            )

        result = self.run(

            *command,

            check=False

        )

        return result.returncode == 0

    def rollout(

        self,

        deployment: str,

        namespace: str

    ):

        return self.run(

            "rollout",

            "status",

            f"deployment/{deployment}",

            "-n",

            namespace

        )

    def wait_for_pod(

        self,

        namespace: str,

        label: str

    ):

        return self.run(

            "wait",

            "--for=condition=Ready",

            "pod",

            "-l",

            label,

            "-n",

            namespace,

            "--timeout=180s"

        )

    def export_kubeconfig(

        self,

        output: Path

    ):

        with open(

            output,

            "w"

        ) as file:

            subprocess.run(

                [

                    "kubectl",

                    "config",

                    "view",

                    "--context",

                    self.context,

                    "--minify",

                    "--flatten"

                ],

                stdout=file,

                check=True

            )

    @staticmethod
    def get_contexts():

        result = subprocess.run(

            [

                "kubectl",

                "config",

                "get-contexts",

                "-o",

                "name"

            ],

            capture_output=True,

            text=True,

            check=True

        )

        return [

            x.strip()

            for x in result.stdout.splitlines()

            if x.strip()

        ]

    def namespace_exists(

        self,

        namespace: str

    ):

        return self.exists(

            "namespace",

            namespace

        )

    def deployment_exists(

        self,

        deployment: str,

        namespace: str

    ):

        return self.exists(

            "deployment",

            deployment,

            namespace

        )

    def service_exists(

        self,

        service: str,

        namespace: str

    ):

        return self.exists(

            "service",

            service,

            namespace

        )

    def configmap_exists(

        self,

        name: str,

        namespace: str

    ):

        return self.exists(

            "configmap",

            name,

            namespace

        )

    def pvc_exists(

        self,

        name: str,

        namespace: str

    ):

        return self.exists(

            "pvc",

            name,

            namespace

        )

    def serviceaccount_exists(

        self,

        name: str,

        namespace: str

    ):

        return self.exists(

            "serviceaccount",

            name,

            namespace

        )
    def get_namespace(

        self,

        namespace: str

    ):

        return self.run(

            "get",

            "namespace",

            namespace,

            check=False

        )


    def get_pods(

        self,

        namespace: str

    ):

        return self.run(

            "get",

            "pods",

            "-n",

            namespace

        )


    def logs(

        self,

        pod: str,

        namespace: str

    ):

        return self.run(

            "logs",

            pod,

            "-n",

            namespace

        )


    def describe(

        self,

        resource: str,

        name: str,

        namespace: str

    ):

        return self.run(

            "describe",

            resource,

            name,

            "-n",

            namespace

        )
    

    def get_events(
        self,
        namespace: str
    ):

        return self.run(

            "get",

            "events",

            "-n",

            namespace,

            "--sort-by=.metadata.creationTimestamp"

        )


    def get_pod_names(
        self,
        namespace: str,
        label: str
    ):

        result = self.run(

            "get",

            "pods",

            "-n",

            namespace,

            "-l",

            label,

            "-o",

            "jsonpath={.items[*].metadata.name}"

        )

        return result.stdout.split()


    def describe_pod(
        self,
        pod: str,
        namespace: str
    ):

        return self.run(

            "describe",

            "pod",

            pod,

            "-n",

            namespace

        )


    def pod_logs(
        self,
        pod: str,
        namespace: str
    ):

        return self.run(

            "logs",

            pod,

            "-n",

            namespace,

            check=False

        )


    def deployment_yaml(
        self,
        deployment: str,
        namespace: str
    ):

        return self.run(

            "get",

            "deployment",

            deployment,

            "-n",

            namespace,

            "-o",

            "yaml"

        )