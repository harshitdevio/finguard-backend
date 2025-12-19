from dataclasses import dataclass

@dataclass(frozen=True)
class StepUpDecision:
    requires_step_up: bool
    reason: str | None = None
