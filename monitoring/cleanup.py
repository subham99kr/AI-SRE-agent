from kubectl import Kubectl


class Cleanup:

    def __init__(
        self,
        context: str
    ):

        self.kubectl = Kubectl(
            context
        )

    def rollback(self):

        print()

        print("=" * 60)
        print("Rolling Back Installation")
        print("=" * 60)

        self.kubectl.run(

            "delete",

            "namespace",

            "monitoring",

            check=False

        )

        print()

        print("✓ Rollback Complete")