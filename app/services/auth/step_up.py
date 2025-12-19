from app.domain.auth.step_up import StepUpDecision


def evaluate_step_up(
    *,
    user,
    device_id: str | None = None,
) -> StepUpDecision:
    """
    Step-up auth trigger (PIN / biometric)

    Determines whether additional authentication is required.
    No side effects or persistence.
    """

    # If user has no PIN set, cannot step-up
    if not user.hashed_pin:
        return StepUpDecision(requires_step_up=False)

    # New device
    if device_id and user.last_device_id and device_id != user.last_device_id:
        return StepUpDecision(
            requires_step_up=True,
            reason="NEW_DEVICE",
        )

    # High-risk flag (set earlier by risk engine)
    if getattr(user, "high_risk_flag", False):
        return StepUpDecision(
            requires_step_up=True,
            reason="HIGH_RISK",
        )

    return StepUpDecision(requires_step_up=False)
