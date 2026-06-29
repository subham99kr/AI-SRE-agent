from app.tools.kubernetes_reader import KubernetesTool

tool = KubernetesTool(cluster_id)

print(tool.get_pods())

print(tool.get_events())