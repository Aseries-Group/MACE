from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    project_name: str
    proponent_name: str
    mineral_type: str
    lease_area: Decimal
    lease_area_unit: str
    production_capacity: Decimal
    production_capacity_unit: str
    district: str
    state: str


class ProjectResponse(ProjectCreate):
    project_id: UUID
    processing_status: str

    model_config = ConfigDict(from_attributes=True)


class EnvironmentalObservationCreate(BaseModel):
    project_id: UUID
    domain: str
    parameter_name: str
    measured_value: Decimal | None = None
    unit: str | None = None
    station_name: str | None = None
    sample_date: date | None = None
    source_reference: str


class EnvironmentalObservationResponse(EnvironmentalObservationCreate):
    observation_id: UUID

    model_config = ConfigDict(from_attributes=True)


class ValidationResultCreate(BaseModel):
    project_id: UUID
    severity: str
    rule_code: str
    field_name: str | None = None
    message: str


class ValidationResultResponse(ValidationResultCreate):
    validation_id: UUID

    model_config = ConfigDict(from_attributes=True)


class ComplianceSectionCreate(BaseModel):
    project_id: UUID
    document_type: str
    section_code: str
    section_title: str
    status: str


class ComplianceSectionResponse(ComplianceSectionCreate):
    section_id: UUID

    model_config = ConfigDict(from_attributes=True)


class SectionItemCreate(BaseModel):
    section_id: UUID
    source_type: str
    source_id: UUID | None = None
    structured_content: str


class SectionItemResponse(SectionItemCreate):
    item_id: UUID

    model_config = ConfigDict(from_attributes=True)