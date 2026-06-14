import asyncio

from app.agents.execution_agent import (
    ExecutionAgent
)


async def main():

    steps = [
        {
            "description": "Get Pods",
            "kubectl_command": "kubectl get pods -n default"
        },
        {
            "description": "Describe Deployment",
            "kubectl_command": "kubectl describe deployment broken-app -n default"
        },
        {
            "description": "Get Deployment",
            "kubectl_command": "kubectl get deployment broken-app -n default"
        }
    ]

    agent = ExecutionAgent()

    results = await agent.run(

        remediation_steps=steps,

        approved=True

    )

    print()

    print("=" * 80)
    print("EXECUTION RESULTS")
    print("=" * 80)

    for result in results:

        print(result)
        print()


if __name__ == "__main__":

    asyncio.run(main())