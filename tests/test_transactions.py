from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.models import Base
from app.db.session import get_db
from app.db.models import Account


DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create fresh tables in memory
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_transaction_flow():
    acc1 = client.post("/v1/accounts/", json={"currency": "INR"}).json()   # Creates Account 1 
    acc2 = client.post("/v1/accounts/", json={"currency": "INR"}).json()   # Creates Account 2

    db = TestingSessionLocal()   # Creates a manual DB session
    sender = db.query(Account).get(acc1["id"])
    sender.balance = 1000
    db.commit()
    db.close()

    tx = client.post("/v1/transactions", json={
        "idempotency_key": "abc-123",
        "sender_account": acc1["id"],
        "receiver_account": acc2["id"],
        "amount": "500.00",
        "currency": "INR"
    }).json()

    assert tx["status"] == "SUCCESS"
