from app.core.security.hashing.issued_secrets import hash_secret
from app.db.models.User.user_auth import UserAuth


async def store_refresh_token(
    *,
    db,
    user_id: str,
    refresh_token: str,
) -> None:
    hashed = hash_secret(refresh_token)

    auth = await db.get(UserAuth, user_id)
    auth.refresh_token_hash = hashed

    await db.commit()
