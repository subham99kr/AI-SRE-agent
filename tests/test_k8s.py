from app.tools.kubernetes_reader import KubernetesTool

tool = KubernetesTool()

print(tool.get_pods())

print(tool.get_events())