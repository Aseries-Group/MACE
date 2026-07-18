import uuid

from sqlalchemy import Column, Date, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.db.session import Base


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    project_name = Column(String(255), nullable=False)
    proponent_name = Column(String(255), nullable=False)
    mineral_type = Column(String(100), nullable=False)

    lease_area = Column(Numeric(12, 2), nullable=False)
    lease_area_unit = Column(String(50), nullable=False)

    production_capacity = Column(Numeric(12, 2), nullable=False)
    production_capacity_unit = Column(String(50), nullable=False)

    district = Column(String(150), nullable=False)
    state = Column(String(150), nullable=False)

    processing_status = Column(
        String(50),
        nullable=False,
        default="PENDING",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    from sqlalchemy import Date, ForeignKey, Text
from sqlalchemy.orm import relationship


class EnvironmentalObservation(Base):
    __tablename__ = "environmental_observations"

    observation_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.project_id", ondelete="CASCADE"),
        nullable=False,
    )

    domain = Column(String(50), nullable=False)
    parameter_name = Column(String(150), nullable=False)
    measured_value = Column(Numeric(14, 4))
    unit = Column(String(50))
    station_name = Column(String(150))
    sample_date = Column(Date)
    source_reference = Column(Text, nullable=False)


class ValidationResult(Base):
    __tablename__ = "validation_results"

    validation_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.project_id", ondelete="CASCADE"),
        nullable=False,
    )

    severity = Column(String(30), nullable=False)
    rule_code = Column(String(50), nullable=False)
    field_name = Column(String(100))
    message = Column(Text, nullable=False)


class ComplianceSection(Base):
    __tablename__ = "compliance_sections"

    section_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.project_id", ondelete="CASCADE"),
        nullable=False,
    )

    document_type = Column(String(100), nullable=False)
    section_code = Column(String(100), nullable=False)
    section_title = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)


class SectionItem(Base):
    __tablename__ = "section_items"

    item_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    section_id = Column(
        UUID(as_uuid=True),
        ForeignKey("compliance_sections.section_id", ondelete="CASCADE"),
        nullable=False,
    )

    source_type = Column(String(100), nullable=False)
    source_id = Column(UUID(as_uuid=True))
    structured_content = Column(Text, nullable=False)
