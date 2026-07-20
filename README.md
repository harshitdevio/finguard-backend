# FinGuard

FinGuard is a **ledger-backed, state-machine driven financial backend API** built using **FastAPI**, **SQLAlchemy (Async PostgreSQL)**, and **Redis**. The project focuses on correctness, consistency, and security by applying backend engineering principles commonly used in financial systems.

## Core Features

### 1. Explicit State Machine

User onboarding is driven by a strict **10-state finite state machine**, preventing invalid state transitions and partially registered accounts. Every operation validates its required preconditions before execution.

```text
┌─────────────────────────────────────────┐
│ 01. PHONE_SUBMITTED                     │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│ 02. OTP_SENT                            │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│ 03. OTP_VERIFIED                        │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│ 04. PREUSER_CREATED                     │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│ 05. CREDENTIALS_SET                     │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│ 06. PROFILE_COMPLETED                   │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│ 07. RISK_PASSED                         │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│ 08. LIMITED_ACCOUNT                     │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│ 09. KYC_SUBMITTED                       │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│ 10. KYC_VERIFIED / FULL_ACCESS          │
└─────────────────────────────────────────┘
```

### 2. Double-Entry Ledger Accounting

Account balances are **never modified directly** with simple `UPDATE` statements. Every transfer generates balanced **DEBIT** and **CREDIT** ledger entries within the same database transaction, providing a complete, auditable history of every financial operation.

### 3. ACID Transactions

All financial operations execute within a single atomic database transaction. Balance updates, transaction creation, and ledger entries either **all succeed or all roll back**, ensuring the system can never enter a partially completed financial state.

### 4. Idempotent Transaction Processing

Transactional endpoints require a unique **idempotency key**. If a client retries a request due to network failures or timeouts, FinGuard detects the existing transaction and returns the original response instead of executing the business logic again, preventing duplicate transfers.

### 5. Race Condition Protection

To prevent double-spending and stale reads during concurrent transfers, FinGuard uses PostgreSQL's pessimistic row locking (`SELECT ... FOR UPDATE`). Account rows remain locked until the active transaction completes, forcing competing requests to execute sequentially.

### 6. Multi-Layer Cryptography

Different categories of sensitive data are protected using cryptographic primitives appropriate to their purpose and lifetime.

- **Passwords & PINs** — Peppered **Argon2id** hashing
- **OTPs** — **HMAC-SHA256** hashing stored exclusively in Redis with TTL expiration
- **KYC Document References** — **SHA-256** hashing before persistence

This ensures sensitive information is never stored in plaintext while significantly reducing the impact of a database compromise.

> [!NOTE]
> **FinGuard** is primarily a backend architecture project built to demonstrate system design, authentication and onboarding orchestration, state-driven workflows, and financial backend design patterns rather than a production-ready fintech product.
>
> Fintech-specific processes such as KYC verification, fraud detection, AML screening, and regulatory compliance are intentionally simplified or mocked. The focus of the project is on backend architecture, service boundaries, state management, security controls, transactional correctness, and financial system design—not regulatory implementation.|

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.
