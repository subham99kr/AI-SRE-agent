from app.tools.kubernetes_tool import KubernetesTool

tool = KubernetesTool()

print(tool.get_pods())

print(tool.get_events())