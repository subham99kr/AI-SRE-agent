from kubernetes import config


def load_cluster_config():

    try:
        config.load_kube_config()
        print("Loaded local kubeconfig")

    except Exception:

        config.load_incluster_config()
        print("Loaded in-cluster config")