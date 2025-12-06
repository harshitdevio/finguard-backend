from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, Literal


class KYCStatusOutput(BaseModel):
    kyc_status: Literal["pending", "verified", "rejected"] = Field(
        ..., description="Current KYC state of the user"
    )
    is_kyc_complete: bool = Field(
        ..., description="Boolean flag to simplify frontend checks"
    )
    submitted_at: Optional[datetime] = Field(
        None, description="When user submitted KYC information"
    )
    verified_at: Optional[datetime] = Field(
        None, description="When KYC was approved (only for verified state)"
    )
    rejection_reason: Optional[str] = Field(
        None, description="Reason for failure (only for rejected state)"
    )

    class Config:
        from_attributes = True

class KYCBasicDetails(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    dob: date = Field(
        ...,
        description="Date of birth in YYYY-MM-DD format"
    )
    gender: str = Field(
        ...,
        pattern=r"^(male|female|other)$",
        description="Gender as male, female, or other"
    )
    pan_number: str = Field(
        ...,
        pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]$",
        description="Valid PAN format (e.g., ABCDE1234F)"
    )
    address_line1: str = Field(
        ...,
        max_length=200
    )
    address_line2: str = Field(
        None,
        max_length=200
    )
    city: str = Field(
        ...,
        max_length=100
    )
    state: str = Field(
        ...,
        max_length=100
    )
    pincode: str = Field(
        ...,
        pattern=r"^\d{6}$",
        description="6-digit Indian PIN code"
    )
    country: str = Field(
        default="India",
        const=True,
        description="Country fixed as India"
    )


class KYCStatusOutput(BaseModel):
    kyc_status: Literal["pending", "verified", "rejected"] = Field(
        ..., description="Current KYC state of the user"
    )
    is_kyc_complete: bool = Field(
        ..., description="Boolean flag to simplify frontend checks"
    )
    submitted_at: Optional[datetime] = Field(
        None, description="When user submitted KYC information"
    )
    verified_at: Optional[datetime] = Field(
        None, description="When KYC was approved (only for verified state)"
    )
    rejection_reason: Optional[str] = Field(
        None, description="Reason for failure (only for rejected state)"
    )

    class Config:
        from_attributes = True
