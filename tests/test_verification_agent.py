import asyncio

from app.agents.verification_agent import (
    VerificationAgent
)


async def main():

    agent = VerificationAgent()

    result = await agent.run(

        namespace="default",

        deployment="broken-app"

    )

    print()

    print("=" * 80)
    print("VERIFICATION RESULT")
    print("=" * 80)

    print(result.model_dump())


if __name__ == "__main__":

    asyncio.run(main())