from app.providers.gemini_flash_provider import GeminiFlashProvider


class ProviderFactory:

    @staticmethod
    def get_root_cause_provider():

        return GeminiFlashProvider()