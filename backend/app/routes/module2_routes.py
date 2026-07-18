from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.module2_models import (
    ComplianceSection,
    EnvironmentalObservation,
    Project,
    SectionItem,
    ValidationResult,
)
from backend.app.schemas.module2_schemas import (
    ComplianceSectionCreate,
    ComplianceSectionResponse,
    EnvironmentalObservationCreate,
    EnvironmentalObservationResponse,
    ProjectCreate,
    ProjectResponse,
    SectionItemCreate,
    SectionItemResponse,
    ValidationResultCreate,
    ValidationResultResponse,
)


router = APIRouter(
    prefix="/projects",
    tags=["Module 2 Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=201,
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    project = Project(
        project_name=project_data.project_name,
        proponent_name=project_data.proponent_name,
        mineral_type=project_data.mineral_type,
        lease_area=project_data.lease_area,
        lease_area_unit=project_data.lease_area_unit,
        production_capacity=project_data.production_capacity,
        production_capacity_unit=project_data.production_capacity_unit,
        district=project_data.district,
        state=project_data.state,
        processing_status="PENDING",
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def get_projects(
    db: Session = Depends(get_db),
):
    return db.query(Project).all()


@router.post(
    "/{project_id}/observations",
    response_model=EnvironmentalObservationResponse,
    status_code=201,
)
def create_environmental_observation(
    project_id: UUID,
    observation_data: EnvironmentalObservationCreate,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.project_id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    observation = EnvironmentalObservation(
        project_id=project_id,
        domain=observation_data.domain,
        parameter_name=observation_data.parameter_name,
        measured_value=observation_data.measured_value,
        unit=observation_data.unit,
        station_name=observation_data.station_name,
        sample_date=observation_data.sample_date,
        source_reference=observation_data.source_reference,
    )

    db.add(observation)
    db.commit()
    db.refresh(observation)

    return observation


@router.get(
    "/{project_id}/observations",
    response_model=list[EnvironmentalObservationResponse],
)
def get_environmental_observations(
    project_id: UUID,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.project_id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return (
        db.query(EnvironmentalObservation)
        .filter(EnvironmentalObservation.project_id == project_id)
        .all()
    )


@router.post(
    "/{project_id}/validation-results",
    response_model=ValidationResultResponse,
    status_code=201,
)
def create_validation_result(
    project_id: UUID,
    validation_data: ValidationResultCreate,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.project_id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    validation_result = ValidationResult(
        project_id=project_id,
        severity=validation_data.severity,
        rule_code=validation_data.rule_code,
        field_name=validation_data.field_name,
        message=validation_data.message,
    )

    db.add(validation_result)
    db.commit()
    db.refresh(validation_result)

    return validation_result


@router.post(
    "/{project_id}/compliance-sections",
    response_model=ComplianceSectionResponse,
    status_code=201,
)
def create_compliance_section(
    project_id: UUID,
    section_data: ComplianceSectionCreate,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.project_id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    section = ComplianceSection(
        project_id=project_id,
        document_type=section_data.document_type,
        section_code=section_data.section_code,
        section_title=section_data.section_title,
        status=section_data.status,
    )

    db.add(section)
    db.commit()
    db.refresh(section)

    return section


@router.post(
    "/sections/{section_id}/items",
    response_model=SectionItemResponse,
    status_code=201,
)
def create_section_item(
    section_id: UUID,
    item_data: SectionItemCreate,
    db: Session = Depends(get_db),
):
    section = (
        db.query(ComplianceSection)
        .filter(ComplianceSection.section_id == section_id)
        .first()
    )

    if section is None:
        raise HTTPException(
            status_code=404,
            detail="Compliance section not found",
        )

    item = SectionItem(
        section_id=section_id,
        source_type=item_data.source_type,
        source_id=item_data.source_id,
        structured_content=item_data.structured_content,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item

@router.get(
    "/{project_id}/validation-results",
    response_model=list[ValidationResultResponse],
)
def get_validation_results(
    project_id: UUID,
    db: Session = Depends(get_db),
):
    return (
        db.query(ValidationResult)
        .filter(ValidationResult.project_id == project_id)
        .all()
    )


@router.get(
    "/{project_id}/compliance-sections",
    response_model=list[ComplianceSectionResponse],
)
def get_compliance_sections(
    project_id: UUID,
    db: Session = Depends(get_db),
):
    return (
        db.query(ComplianceSection)
        .filter(ComplianceSection.project_id == project_id)
        .all()
    )


@router.get(
    "/sections/{section_id}/items",
    response_model=list[SectionItemResponse],
)
def get_section_items(
    section_id: UUID,
    db: Session = Depends(get_db),
):
    return (
        db.query(SectionItem)
        .filter(SectionItem.section_id == section_id)
        .all()
    )