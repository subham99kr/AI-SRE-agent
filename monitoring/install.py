from pathlib import Path

from kubectl import Kubectl
from installer import MonitoringInstaller
from register_cluster import ClusterRegistry
from ports import PortManager
from diagnostics import Diagnostics
from cleanup import Cleanup



ROOT = Path(__file__).parent

CLUSTERS_DIR = ROOT.parent / "clusters"


def select_context():

    contexts = Kubectl.get_contexts()

    if not contexts:

        raise RuntimeError(
            "No Kubernetes contexts found."
        )

    if len(contexts) == 1:

        print(
            f"Using context: {contexts[0]}"
        )

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


def export_kubeconfig(
    kubectl: Kubectl,
    cluster_name: str
):

    CLUSTERS_DIR.mkdir(
        exist_ok=True
    )

    destination = (

        CLUSTERS_DIR /

        f"{cluster_name}.yaml"

    )

    kubectl.export_kubeconfig(
        destination
    )

    return destination


def main():

    print()

    print("=" * 60)
    print("AI-SRE Monitoring Installer")
    print("=" * 60)

    context = select_context()

    print()

    cluster_name = input(
        "Cluster Name: "
    ).strip()

    if not cluster_name:

        print(
            "Cluster name cannot be empty."
        )

        return

    kubectl = Kubectl(
        context
    )

    print()

    print(
        "Exporting kubeconfig..."
    )

    kubeconfig = export_kubeconfig(

        kubectl,

        cluster_name

    )

    print(
        "✓ Done"
    )

    installer = MonitoringInstaller(
        context
    )



    try:

        installer.install()

    except Exception as e:

        print()

        print("=" * 60)
        print("INSTALLATION FAILED")
        print("=" * 60)

        print()

        print(e)

        print()

        Diagnostics(

            context

        ).collect()

        print()

        answer = input(

            "Rollback installation? (Y/N): "

        ).strip().lower()

        if answer == "y":

            Cleanup(

                context

            ).rollback()

        return

    print()




    host_port = PortManager.next_free_port()

    prometheus_url = (

        f"http://localhost:{host_port}"

    )

    print()

    print(

        f"Assigned Host Port : {host_port}"

    )

    print(

        f"Prometheus URL     : {prometheus_url}"

    )

    ClusterRegistry().register(

        cluster_id=cluster_name,

        kubeconfig_path=kubeconfig,

        prometheus_url=prometheus_url,

        host_port=host_port

    )

    print()

    print("=" * 60)
    print("INSTALLATION SUCCESSFUL")
    print("=" * 60)

    print()

    print(f"Cluster      : {cluster_name}")

    print(f"Context      : {context}")

    print(f"Kubeconfig   : {kubeconfig}")

    print(f"Prometheus   : {prometheus_url}")

    print()

    print("You can now start the AI-SRE backend.")


if __name__ == "__main__":

    main()