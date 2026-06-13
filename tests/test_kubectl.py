from app.tools.kubectl_tool import (
    KubectlTool
)

tool = KubectlTool()

result = tool.get_pods(
    namespace="default"
)

print(result)