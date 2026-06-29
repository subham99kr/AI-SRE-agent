from pathlib import Path

from kubectl import Kubectl
from register_cluster import ClusterRegistry


ROOT = Path(__file__).parent

CLUSTERS_DIR = ROOT.parent / "clusters"


def select_context():

    contexts = Kubectl.get_contexts()

    if not contexts:

        raise RuntimeError(
            "No Kubernetes contexts found."
        )

    if len(contexts) == 1:

        return contexts[0]

    print()

    print("=" * 60)

    print("Available Kubernetes Contexts")

    print("=" * 60)

    print()

    for i, context in enumerate(

        contexts,

        start=1

    ):

        print(

            f"{i}. {context}"

        )

    print()

    while True:

        try:

            choice = int(

                input(
                    "Select Context: "
                )

            )

            if 1 <= choice <= len(contexts):

                return contexts[
                    choice - 1
                ]

        except Exception:

            pass

        print(
            "Invalid selection."
        )


def main():

    print()

    print("=" * 60)

    print(
        "AI-SRE Monitoring Uninstaller"
    )

    print("=" * 60)

    context = select_context()

    cluster_name = input(

        "\nCluster Name: "

    ).strip()

    kubectl = Kubectl(
        context
    )

    print()

    print(
        "Deleting monitoring namespace..."
    )

    kubectl.run(

        "delete",

        "namespace",

        "monitoring",

        check=False

    )

    print()

    print("Monitoring namespace removed.")

    print()

    print("Registry cleaned.")

    print()

    print("Kubeconfig removed.")

    answer = input(

        "\nRemove cluster from registry? (Y/N): "

    ).strip().lower()

    if answer == "y":

        ClusterRegistry().unregister(

            cluster_name

        )

        kubeconfig = (

            CLUSTERS_DIR /

            f"{cluster_name}.yaml"

        )

        if kubeconfig.exists():

            kubeconfig.unlink()

        print(
            "✓ Cluster removed."
        )

    print()

    print("=" * 60)

    print(
        "Finished"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()