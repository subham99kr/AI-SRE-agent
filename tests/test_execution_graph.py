import asyncio

from app.workflows.execution_graph import (
    ExecutionGraph
)


async def main():

    graph = (
        ExecutionGraph()
        .build()
    )

    result = await graph.ainvoke(

        {
            "incident_id":
            "3a8aa87a-856d-4ceb-865c-e6b29d827cc8"
        }

    )

    print(result)


asyncio.run(main())