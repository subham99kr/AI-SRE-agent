# import json

# from app.providers.provider_factory import (
#     ProviderFactory
# )


# class FixPlannerAgent:

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
# You are a Kubernetes remediation expert.

# Root Cause:
# {root_cause}

# Evidence:
# {evidence_json}

# Generate ONLY valid JSON:

# {{
#     "fix_plan": [
#         "step1",
#         "step2",
#         "step3"
#     ]
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
#                 "fix_plan": [
#                     "Manual investigation required"
#                 ]
#             }