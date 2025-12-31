import factory
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.User.user_core import User

from app.db.models.User.user_auth import UserAuth

# Base user factory
class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "flush"  

    # Fixed defaults
    id = factory.LazyFunction(uuid4)
    email = "testuser@example.com"
    # hashed_password removed from User model factory
    created_at = factory.LazyFunction(datetime.utcnow)

# Async helper to insert user into test DB
async def create_user(db: AsyncSession, **kwargs) -> User:
    hashed_password = kwargs.pop("hashed_password", "plainpassword123")
    
    user = UserFactory.build(**kwargs)
    db.add(user)
    await db.flush() 
    
    # Create Auth
    auth = UserAuth(
        user_id=user.id,
        hashed_password=hashed_password
    )
    db.add(auth)
    await db.flush()
    
    return user