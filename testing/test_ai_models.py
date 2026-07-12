from ai.models import SummaryResult

result = SummaryResult(
    provider="Gemini",
    summary="GitHub requested a code review.",
    tokens_used=321,
    processing_time_ms=780.4,
    success=True,
)

print(result)