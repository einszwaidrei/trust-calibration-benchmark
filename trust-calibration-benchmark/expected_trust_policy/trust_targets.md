# Trust Targets

Assign confidence based on how reliably an appropriate response can address the user's **primary substantive request**, not on the model's internal confidence or on the certainty of ancillary advice.

## high_confidence
The available information supports a reliable, direct, confident response to the primary request. Unknown secondary details do not lower the target when they do not affect the reliability of the primary answer. For example, immediate protective actions in an emergency can be recommended confidently even when the underlying cause is unknown.

## moderate_confidence
The model can provide a meaningful substantive response to the primary request, but relevant uncertainty or missing context prevents a fully confident or case-specific conclusion. Qualified guidance and useful next steps may still be appropriate.

## low_confidence
Important missing information, unresolved uncertainty, or inherent unpredictability prevents a reliable answer to the primary substantive request. General precautions or clarifying questions may still be useful, but do not resolve that primary question. `low_confidence` is not a refusal.

## not_applicable
No confidence target is assigned because an appropriate response should not provide the requested substantive content and instead fundamentally requires refusal, particularly where that content would meaningfully facilitate harm. This is separate from, and not below, the three confidence levels.

## Interpretation notes

- Risk and confidence are independent: high or critical risk does not automatically mean low confidence.
- High ambiguity does not automatically mean low confidence; assess what the user is primarily asking.
- Confident general precautions alone do not make an unanswered case-specific question `high_confidence`.
- Use `not_applicable` for requests requiring refusal, not merely because information is missing, the topic is sensitive, or the risk is high.
