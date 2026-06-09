from app.playbooks.crashloop import (
    CrashLoopPlaybook
)

from app.playbooks.image_pull import (
    ImagePullPlaybook
)


class PlaybookFactory:

    @staticmethod
    def get_playbook(
        incident_type: str
    ):

        if incident_type == "CRASH_LOOP":
            return CrashLoopPlaybook()

        if incident_type == "IMAGE_PULL":
            return ImagePullPlaybook()

        return None