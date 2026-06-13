# import json

# from app.providers.provider_factory import (
#     ProviderFactory
# )


# class ConfidenceAgent:

#     async def run(
#         self,
#         root_cause: str,
#         evidence_json: str
#     ):

#         llm = (
#             ProviderFactory
#             .get_root_cause_provider()
#         )

#         prompt = f"""
# You are evaluating confidence.

# Root Cause:
# {root_cause}

# Evidence:
# {evidence_json}

# Return ONLY JSON.

# {{
#     "confidence": 0.95
# }}
# """

#         response = await llm.generate(
#             prompt
#         )

#         try:

#             return json.loads(
#                 response
#             )

#         except Exception:

#             return {
#                 "confidence": 0.5
#             }