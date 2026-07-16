# MACE
Mining Automated Compliance Execution

# Installation process

 1. Install Visual Studio Code
 2. Install Docker Desktop and run it
 3. Install Git
 4. Clone the repository and open in Visual Studio Code
 5. Click on "Open In Container" if no pop-up appears use Ctrl + Shift + P and search "Rebuild dev container clear cache"


# Quick verification checklist

## Python dependency sanity
python3 -m pip check

## Node dependency sanity
npm ls --depth=0

## Port listeners
ss -tulnp | egrep ':(8000|5173|5432)'

## Backend health
curl http://localhost:8000/docs

## Frontend health
curl http://localhost:5173

## Database health
pg_isready -h localhost -p 5432


# Development Must Dos
Switch to "development" branch when writing code, do not push/merge in "main" branch.








# Module 2: Data Processing and Compliance Structuring

Module 2 receives raw mining-project and environmental-compliance data from Module 1, approved files, internal Python objects, or shared database records. It validates, normalizes, classifies, and maps this information into structured compliance sections. The processed data is stored in PostgreSQL and made available to Module 3.

This README contains the complete Software Design Document and Technical Design Document for Module 2. It follows the project rule that Module 2 does not use external Application Programming Interfaces.

---

# **SOFTWARE DESIGN DOCUMENT (SDD) STARTS HERE**

> **Module:** Data Extraction, Processing, Validation, and Compliance Document Structuring  
> **Project:** MACE — Mining Automated Compliance Execution  
> **Architecture Rule:** No external API-based communication  
> **Status:** Draft for review

---

## 1. Module Overview

Module 2 is responsible for receiving mining-project and environmental-compliance data, validating it, cleaning it, organizing it, and mapping it into structured compliance sections.

The module works as an internal Python processing layer. It does not expose web APIs. Data is received from files, shared database records, or internal Python functions and is passed to the next module through shared database tables or internal program calls.

The module supports data related to:

- Mining project details
- Pre-Feasibility Reports
- Form 1
- Environmental Impact Assessment
- Environmental Management Plan
- Air-quality data
- Water-quality data
- Soil-quality data
- Noise-monitoring data
- Ecology and biodiversity studies
- Socio-economic studies
- Environmental Clearance documentation

---

## 2. Purpose

The purpose of Module 2 is to convert raw and unorganized compliance data into a clean, validated, and structured format that can be used by later modules.

The module reduces:

- Repeated manual data entry
- Missing values
- Inconsistent units
- Duplicate records
- Incorrect field formats
- Difficulty in preparing compliance sections

---

## 3. Objectives

- Accept project data from Module 1, files, or database records.
- Validate required fields.
- Normalize names, dates, values, and units.
- Detect missing and duplicate information.
- Classify data into compliance domains.
- Map data into required report sections.
- Store structured results in PostgreSQL.
- Provide processed data to Module 3.
- Maintain warnings, errors, and source references.

---

## 4. Scope

### 4.1 Included

- Mining project information
- Project location and lease details
- Mineral and production details
- Baseline environmental data
- Air, water, soil, and noise records
- Ecology and biodiversity information
- Socio-economic information
- Impact and mitigation information
- Compliance section mapping
- Validation results
- Processing status
- Structured database storage

### 4.2 Not Included

- Direct PARIVESH submission
- External API integration
- Government approval decisions
- Legal interpretation
- Final Environmental Clearance approval
- Physical sensor control
- Laboratory testing
- Final report generation
- User authentication owned by another module

---

## 5. Stakeholders and Users

| User / Stakeholder | Role |
|---|---|
| Environmental consultant | Reviews processed information |
| Compliance team | Checks completeness and correctness |
| Project coordinator | Tracks project status |
| Data-entry user | Corrects missing or invalid values |
| Module 1 | Supplies raw or extracted data |
| Module 3 | Uses structured output |
| Administrator | Maintains reference values |
| Developer | Implements and tests the module |

---

## 6. Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | The module shall receive data from files, internal functions, or shared database tables. |
| FR-02 | The module shall validate mandatory project fields. |
| FR-03 | The module shall validate data types and numerical ranges. |
| FR-04 | The module shall normalize names, dates, units, and text formatting. |
| FR-05 | The module shall classify data into compliance domains. |
| FR-06 | The module shall detect possible duplicates. |
| FR-07 | The module shall generate validation errors and warnings. |
| FR-08 | The module shall reject records with critical errors. |
| FR-09 | The module shall map valid data into compliance sections. |
| FR-10 | The module shall store processed data in PostgreSQL. |
| FR-11 | The module shall maintain source references. |
| FR-12 | The module shall provide structured records to Module 3. |
| FR-13 | The module shall allow correction and reprocessing. |
| FR-14 | The module shall store processing status and timestamps. |

---

## 7. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Maintainability | Processing logic shall be divided into separate Python modules. |
| NFR-02 | Reliability | One invalid record shall not damage other valid records. |
| NFR-03 | Security | Database credentials shall remain outside source control. |
| NFR-04 | Testability | Validation and mapping functions shall support unit testing. |
| NFR-05 | Portability | The module shall run inside the project Dev Container. |
| NFR-06 | Consistency | Output shall follow one standard internal structure. |
| NFR-07 | Auditability | Source, status, and processing results shall be traceable. |
| NFR-08 | Performance | Normal project datasets shall process without unnecessary delay. |

---

## 8. Use Cases

### 8.1 Process New Project Data

1. Module 1 or a file provides project data.
2. Module 2 reads the input.
3. Required fields are checked.
4. Values are normalized.
5. Records are classified.
6. Compliance sections are created.
7. Results are stored.
8. Module 3 reads the structured data.

### 8.2 Correct Invalid Data

1. User reviews validation errors.
2. Incorrect data is corrected.
3. Module 2 reprocesses affected records.
4. Processing status is updated.

### 8.3 Retrieve Structured Data

1. Module 3 requests project information through shared database access or an internal Python function.
2. Module 2 checks whether the data is ready.
3. Approved structured sections are returned.

---

## 9. High-Level Architecture

```mermaid
flowchart LR
    A[Module 1 / Input Files / Shared Database] --> B[Python Input Reader]
    B --> C[Validation Layer]
    C --> D[Normalization Layer]
    D --> E[Classification Layer]
    E --> F[Compliance Mapping Layer]
    F --> G[Data Quality Check]
    G --> H[(PostgreSQL Database)]
    H --> I[Module 3]
    C --> J[Errors and Warnings]
```

The architecture contains no external API layer.

---

## 10. Processing Workflow

```mermaid
flowchart TD
    A[Read raw data] --> B{Required fields available?}
    B -- No --> C[Create validation error]
    B -- Yes --> D[Normalize values]
    D --> E{Values valid?}
    E -- No --> F[Create error or warning]
    F --> G{Critical error?}
    G -- Yes --> H[Reject affected record]
    G -- No --> I[Continue with warning]
    E -- Yes --> J[Classify record]
    I --> J
    J --> K[Map to compliance section]
    K --> L[Save structured data]
    L --> M[Update processing status]
    M --> N[Make data available to Module 3]
```

---

## 11. Module Interaction

```mermaid
flowchart LR
    M1[Module 1] -->|Files / Shared Tables / Internal Objects| M2[Module 2]
    M2 -->|Errors and Missing Fields| M1
    M2 -->|Structured Database Records| M3[Module 3]
```

No HTTP requests or external API calls are required.

---

## 12. Component Design

### 12.1 Input Reader

Reads data from:

- CSV files
- Excel files
- JSON files
- Shared database tables
- Internal Python objects

### 12.2 Validation Component

Checks:

- Required fields
- Numerical ranges
- Date formats
- Unit availability
- Duplicate records
- Cross-field consistency

### 12.3 Normalization Component

Standardizes:

- Project names
- State and district names
- Dates
- Units
- Text spacing
- Parameter labels

### 12.4 Classification Component

Groups information into:

- Project details
- Air
- Water
- Soil
- Noise
- Ecology
- Biodiversity
- Socio-economic
- Impact
- Mitigation

### 12.5 Compliance Mapping Component

Maps processed information into:

- Project description
- Site details
- Baseline environmental condition
- Impact assessment
- Mitigation measures
- Environmental Management Plan
- Ecology and biodiversity section
- Socio-economic section

### 12.6 Storage Component

Stores:

- Project records
- Environmental observations
- Validation results
- Compliance sections
- Processing status
- Source references

---

## 13. Data Flow Design

```mermaid
flowchart LR
    F1[Input File] --> P[Module 2 Processing]
    D1[(Shared Raw Data Tables)] --> P
    M1[Module 1 Internal Output] --> P
    P --> D2[(Processed Project Data)]
    P --> D3[(Validation Results)]
    P --> D4[(Compliance Sections)]
    D4 --> M3[Module 3]
```

---

## 14. Data Design

```mermaid
erDiagram
    PROJECT ||--o{ ENVIRONMENTAL_OBSERVATION : contains
    PROJECT ||--o{ VALIDATION_RESULT : has
    PROJECT ||--o{ COMPLIANCE_SECTION : produces
    COMPLIANCE_SECTION ||--o{ SECTION_ITEM : contains

    PROJECT {
        uuid project_id PK
        string project_name
        string proponent_name
        string mineral_type
        decimal lease_area
        decimal production_capacity
        string district
        string state
        string processing_status
        datetime created_at
        datetime updated_at
    }

    ENVIRONMENTAL_OBSERVATION {
        uuid observation_id PK
        uuid project_id FK
        string domain
        string parameter_name
        decimal measured_value
        string unit
        string station_name
        date sample_date
        string source_reference
    }

    VALIDATION_RESULT {
        uuid validation_id PK
        uuid project_id FK
        string severity
        string rule_code
        string field_name
        string message
    }

    COMPLIANCE_SECTION {
        uuid section_id PK
        uuid project_id FK
        string document_type
        string section_code
        string section_title
        string status
    }

    SECTION_ITEM {
        uuid item_id PK
        uuid section_id FK
        string source_type
        uuid source_id
        text structured_content
    }
```

---

## 15. Input and Output Design

### Example Input

```json
{
  "project_name": "Example Limestone Mining Project",
  "proponent_name": "Example Minerals Private Limited",
  "mineral_type": "Limestone",
  "lease_area": 25.4,
  "lease_area_unit": "hectare",
  "production_capacity": 1.0,
  "production_capacity_unit": "MTPA",
  "district": "Example District",
  "state": "Example State"
}
```

### Example Output

```json
{
  "project_id": "generated-uuid",
  "processing_status": "READY_WITH_WARNINGS",
  "validation_summary": {
    "errors": 0,
    "warnings": 2
  },
  "sections": [
    {
      "section_code": "PROJECT_DESCRIPTION",
      "status": "READY"
    },
    {
      "section_code": "BASELINE_ENVIRONMENT",
      "status": "INCOMPLETE"
    }
  ]
}
```

---

## 16. Validation Rules

| Rule ID | Rule |
|---|---|
| VR-01 | Project name is mandatory. |
| VR-02 | Proponent name is mandatory. |
| VR-03 | Mineral type is mandatory. |
| VR-04 | Lease area must be greater than zero. |
| VR-05 | Production capacity must be greater than zero. |
| VR-06 | District and state are mandatory. |
| VR-07 | Environmental measurements must be numeric where required. |
| VR-08 | Every measurement must include a unit. |
| VR-09 | Sample date must be valid. |
| VR-10 | Duplicate observations must be flagged. |
| VR-11 | Critical errors must block approval. |
| VR-12 | Every structured value must retain a source reference. |

---

## 17. Error Handling

The module shall use:

- Critical errors
- Warnings
- Informational messages
- Database error handling
- File-reading error handling
- Invalid-format handling

Each issue should include:

- Rule code
- Field name
- Severity
- Message
- Source record reference

---

## 18. Security

- `.env` must not be committed.
- Database credentials must be stored in environment variables.
- Only authorized users or modules may edit approved records.
- Sensitive client information must not be printed in logs.
- Input files must be validated before processing.
- Database changes should be traceable.
- Approved records must not be silently overwritten.

---

## 19. Assumptions and Dependencies

### Assumptions

- Module 1 supplies data in an agreed format.
- Module 3 reads structured information from shared tables or internal functions.
- A human reviewer remains responsible for final correctness.
- Initial development focuses on mining.

### Dependencies

- Python
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Docker Desktop
- VS Code Dev Container
- Shared project database
- Agreed Module 1 and Module 3 formats

### Constraints

- No API-based communication.
- No direct government portal submission.
- No legal approval decision.
- No final report-generation responsibility.

---

## 20. Acceptance Criteria

1. Valid project data is processed successfully.
2. Missing required fields produce clear errors.
3. Invalid values are rejected.
4. Units and dates are normalized.
5. Data is classified correctly.
6. Compliance sections are created.
7. Validation results are stored.
8. Critical errors prevent approval.
9. Module 3 can read the processed data.
10. The module runs in the Dev Container.
11. Core Python functions are tested.
12. No API dependency is required.

---

## 21. Future Enhancements

- Additional file formats
- Configurable validation rules
- Automated completeness scoring
- Versioned compliance templates
- Reviewer approval workflow
- Additional industries beyond mining
- Intelligent section suggestions

---

# **TECHNICAL DESIGN DOCUMENT (TDD) STARTS HERE**

> **Module:** Data Extraction, Processing, Validation, and Compliance Document Structuring  
> **Project:** MACE — Mining Automated Compliance Execution  
> **Architecture Rule:** No external API-based communication  
> **Status:** Draft for review

---

## 1. Technical Overview

Module 2 is designed as an internal Python processing module.

It does not expose FastAPI endpoints and does not depend on HTTP communication. It receives information through internal Python objects, approved files, or shared PostgreSQL tables.

The module performs:

- Data reading
- Validation
- Normalization
- Classification
- Compliance-section mapping
- Database storage
- Data-quality evaluation
- Output preparation for Module 3

---

## 2. Technical Scope

### Included

- Python file readers
- Internal processing functions
- Pydantic data models
- Validation rules
- Normalization functions
- Classification functions
- Mapping functions
- SQLAlchemy models
- PostgreSQL storage
- Alembic migrations
- Unit and integration tests
- Dev Container execution

### Excluded

- FastAPI routers
- HTTP endpoints
- REST APIs
- External service calls
- Direct PARIVESH integration
- User-interface code
- Final report generation
- Authentication implementation

---

## 3. Technology Stack

| Area | Technology | Purpose |
|---|---|---|
| Language | Python | Core module development |
| Validation | Pydantic | Internal data models and validation |
| Database | PostgreSQL | Persistent storage |
| Object relational mapping | SQLAlchemy | Database access |
| Async database driver | asyncpg | Asynchronous PostgreSQL connection |
| Migration | Alembic | Database schema changes |
| Data files | CSV, Excel, JSON | Supported internal inputs |
| Container | Docker Dev Container | Reproducible environment |
| Testing | pytest | Unit and integration testing |
| Browser testing | Playwright, if needed | Only for project-level user-interface tests |

---

## 4. Technical Architecture

```mermaid
flowchart TB
    subgraph Inputs
        F[CSV / Excel / JSON Files]
        D[(Shared Raw Database Tables)]
        M1[Module 1 Internal Python Output]
    end

    subgraph Module_2
        IR[Input Reader]
        VM[Pydantic Models]
        VS[Validation Service]
        NS[Normalization Service]
        CS[Classification Service]
        MS[Compliance Mapping Service]
        QS[Data Quality Service]
        RP[Repository Layer]
    end

    subgraph Storage_and_Output
        DB[(PostgreSQL)]
        M3[Module 3]
        LG[Logs and Audit Records]
    end

    F --> IR
    D --> IR
    M1 --> IR
    IR --> VM
    VM --> VS
    VS --> NS
    NS --> CS
    CS --> MS
    MS --> QS
    QS --> RP
    RP --> DB
    DB --> M3
    QS --> LG
```

---

## 5. Design Principles

### 5.1 No API Layer

Module communication occurs through:

- Internal Python function calls
- Shared database tables
- Approved files
- Shared domain objects

### 5.2 Separation of Responsibilities

Validation, normalization, classification, mapping, and storage are separate.

### 5.3 Stable Internal Models

All input formats are converted into one internal structure.

### 5.4 Traceability

Every processed record retains its source.

### 5.5 Transaction Safety

Related database changes are committed together.

---

## 6. Proposed Folder Structure

```text
backend/
├── module2/
│   ├── __init__.py
│   ├── models/
│   │   ├── project_models.py
│   │   ├── observation_models.py
│   │   └── processing_models.py
│   ├── readers/
│   │   ├── csv_reader.py
│   │   ├── excel_reader.py
│   │   ├── json_reader.py
│   │   └── database_reader.py
│   ├── services/
│   │   ├── processor.py
│   │   ├── validator.py
│   │   ├── normalizer.py
│   │   ├── classifier.py
│   │   ├── mapper.py
│   │   └── quality_checker.py
│   ├── repositories/
│   │   ├── project_repository.py
│   │   ├── observation_repository.py
│   │   └── section_repository.py
│   ├── rules/
│   │   ├── project_rules.py
│   │   └── environmental_rules.py
│   ├── constants.py
│   └── exceptions.py
├── db/
│   ├── session.py
│   └── models/
├── tests/
│   ├── unit/
│   └── integration/
└── alembic/
```

This is a proposed structure and should be adjusted to the final MACE repository.

---

## 7. Main Components

### 7.1 Input Reader

```python
class InputReader:
    def read(self, source_path: str) -> list[dict]:
        ...
```

Separate readers may handle:

- CSV
- Excel
- JSON
- Shared database records

### 7.2 Processing Controller

```python
async def process_project_data(
    raw_project: dict,
    raw_observations: list[dict]
) -> "ProcessingResult":
    ...
```

Responsibilities:

1. Build internal models.
2. Validate.
3. Normalize.
4. Classify.
5. Map.
6. Store.
7. Return processing result.

### 7.3 Validation Service

```python
class ValidationService:
    def validate_project(self, project) -> list["ValidationIssue"]:
        ...

    def validate_observation(self, observation) -> list["ValidationIssue"]:
        ...
```

### 7.4 Normalization Service

```python
class NormalizationService:
    def normalize_project(self, project):
        ...

    def normalize_observation(self, observation):
        ...
```

### 7.5 Classification Service

```python
class ClassificationService:
    def classify_record(self, record) -> str:
        ...
```

### 7.6 Mapping Service

```python
class ComplianceMappingService:
    def map_record_to_sections(self, record) -> list["SectionItem"]:
        ...
```

### 7.7 Repository Layer

```python
class ProjectRepository:
    async def save_project(self, session, project):
        ...

    async def get_project(self, session, project_id):
        ...
```

---

## 8. Processing Sequence

```mermaid
sequenceDiagram
    participant M1 as Module 1 / File
    participant R as Input Reader
    participant P as Processor
    participant V as Validator
    participant N as Normalizer
    participant C as Classifier
    participant M as Mapper
    participant DB as PostgreSQL
    participant M3 as Module 3

    M1->>R: Provide raw data
    R->>P: Return internal records
    P->>V: Validate records
    V-->>P: Errors and warnings
    alt Critical errors found
        P-->>M1: Return correction details
    else Data can continue
        P->>N: Normalize values
        N-->>P: Normalized records
        P->>C: Classify records
        C-->>P: Compliance domains
        P->>M: Map to sections
        M-->>P: Structured sections
        P->>DB: Save project and results
        DB-->>P: Commit successful
        M3->>DB: Read structured data
    end
```

---

## 9. Internal Data Models

### Project Input Model

```python
class ProjectInput(BaseModel):
    project_name: str
    proponent_name: str
    mineral_type: str
    lease_area: float
    lease_area_unit: str
    production_capacity: float
    production_capacity_unit: str
    district: str
    state: str
```

### Environmental Observation Model

```python
class EnvironmentalObservationInput(BaseModel):
    domain: str
    parameter_name: str
    measured_value: float | None
    unit: str | None
    station_name: str | None
    sample_date: date | None
    source_reference: str
```

### Validation Issue Model

```python
class ValidationIssue(BaseModel):
    rule_code: str
    severity: str
    field_name: str | None
    message: str
    source_record_id: str | None
```

### Processing Result Model

```python
class ProcessingResult(BaseModel):
    project_id: str
    processing_status: str
    errors: list[ValidationIssue]
    warnings: list[ValidationIssue]
    generated_sections: list[str]
```

---

## 10. Database Design

### Project Table

| Field | Type |
|---|---|
| project_id | UUID |
| project_name | VARCHAR |
| proponent_name | VARCHAR |
| mineral_type | VARCHAR |
| lease_area | NUMERIC |
| lease_area_unit | VARCHAR |
| production_capacity | NUMERIC |
| production_capacity_unit | VARCHAR |
| district | VARCHAR |
| state | VARCHAR |
| processing_status | VARCHAR |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

### Environmental Observation Table

| Field | Type |
|---|---|
| observation_id | UUID |
| project_id | UUID |
| domain | VARCHAR |
| parameter_name | VARCHAR |
| measured_value | NUMERIC |
| unit | VARCHAR |
| station_name | VARCHAR |
| sample_date | DATE |
| source_reference | TEXT |

### Validation Result Table

| Field | Type |
|---|---|
| validation_id | UUID |
| project_id | UUID |
| severity | VARCHAR |
| rule_code | VARCHAR |
| field_name | VARCHAR |
| message | TEXT |

### Compliance Section Table

| Field | Type |
|---|---|
| section_id | UUID |
| project_id | UUID |
| document_type | VARCHAR |
| section_code | VARCHAR |
| section_title | VARCHAR |
| status | VARCHAR |

---

## 11. Internal Communication Design

Module 2 receives and sends data without APIs.

### Module 1 to Module 2

Possible methods:

- Internal Python object
- CSV file
- Excel file
- JSON file
- Shared database table

### Module 2 to Module 3

Possible methods:

- Shared PostgreSQL tables
- Internal Python function returning structured objects
- Approved JSON output file

### Example Internal Function

```python
async def get_ready_sections(project_id: str) -> list[dict]:
    ...
```

---

## 12. Validation Design

### Schema Validation

Handled using Pydantic:

- Required values
- Data types
- Date formats
- Nested structures

### Business Validation

Handled through rule functions:

```python
def validate_positive_value(value: float, field_name: str):
    ...

def validate_required_text(value: str, field_name: str):
    ...

def detect_duplicate_observations(records: list):
    ...
```

Validation results should be returned as structured objects, not only printed.

---

## 13. Normalization Design

Normalization functions should:

- Trim spaces
- Standardize text case
- Convert supported units
- Standardize dates
- Standardize project names
- Standardize location labels
- Standardize environmental parameter names

Example:

```python
def normalize_unit(unit: str) -> str:
    unit_map = {
        "ha": "hectare",
        "hectares": "hectare"
    }
    return unit_map.get(unit.strip().lower(), unit.strip().lower())
```

---

## 14. Classification Design

Classification domains:

- PROJECT
- AIR
- WATER
- SOIL
- NOISE
- ECOLOGY
- BIODIVERSITY
- SOCIO_ECONOMIC
- IMPACT
- MITIGATION

Example:

```python
def classify_record(record) -> str:
    ...
```

Classification may use:

- Field name
- Parameter name
- Source section
- Input type
- Reference configuration

---

## 15. Compliance Mapping Design

Mapping rules link classified data to report sections.

Example mapping:

| Domain | Compliance Section |
|---|---|
| PROJECT | Project Description |
| AIR | Baseline Air Environment |
| WATER | Baseline Water Environment |
| SOIL | Baseline Soil Environment |
| NOISE | Baseline Noise Environment |
| ECOLOGY | Ecology and Biodiversity |
| SOCIO_ECONOMIC | Socio-Economic Environment |
| IMPACT | Anticipated Environmental Impacts |
| MITIGATION | Environmental Management Plan |

---

## 16. Processing Algorithm

```text
INPUT:
- Raw project data
- Raw observation records

1. Read the input.
2. Convert values into internal Pydantic models.
3. Run project validation.
4. Run observation validation.
5. Detect duplicate records.
6. If critical errors exist:
      a. Return validation result.
      b. Do not approve the record.
7. Normalize accepted values.
8. Classify each record.
9. Map each record to compliance sections.
10. Calculate processing status.
11. Begin database transaction.
12. Save project data.
13. Save observations.
14. Save validation results.
15. Save compliance sections.
16. Commit transaction.
17. Return ProcessingResult.
```

---

## 17. Error Handling

Custom exceptions may include:

```python
class Module2Error(Exception):
    pass

class InputFileError(Module2Error):
    pass

class ValidationFailedError(Module2Error):
    pass

class DatabaseOperationError(Module2Error):
    pass
```

Expected error categories:

- File not found
- Unsupported file type
- Invalid input format
- Missing mandatory values
- Duplicate data
- Database unavailable
- Transaction failure
- Unexpected processing error

No internal stack trace should be shown to normal users.

---

## 18. Database Transaction Design

All records created for one processing operation should be stored in one transaction.

If any critical database operation fails:

1. Roll back the transaction.
2. Log the failure.
3. Return a controlled error result.
4. Do not leave partially saved data.

---

## 19. Security Requirements

- Keep `.env` in `.gitignore`.
- Read database credentials using environment variables.
- Do not log full database URLs.
- Validate all file paths.
- Restrict accepted file formats.
- Prevent unauthorized modification of approved data.
- Preserve source and change history.
- Use SQLAlchemy instead of manually building unsafe SQL strings.

---

## 20. Logging and Audit

Suggested log information:

- Timestamp
- Project ID
- Processing step
- Number of records
- Error count
- Warning count
- Final status
- Processing duration

Audit events:

- Data imported
- Data corrected
- Project reprocessed
- Validation status changed
- Compliance sections generated
- Approved data modified

---

## 21. Performance Considerations

- Process records in batches.
- Avoid one database query per row.
- Use bulk insert where appropriate.
- Add database indexes.
- Cache stable reference values.
- Avoid reading the same file repeatedly.
- Use asynchronous database sessions.
- Support future background processing for large files.

---

## 22. Database Migrations

Alembic should manage:

1. Project table
2. Environmental observation table
3. Validation result table
4. Compliance section table
5. Section item table
6. Foreign keys
7. Indexes
8. Reference data tables if required

No real client data should be stored in migration files.

---

## 23. Testing Strategy

### Unit Tests

- Required-field validation
- Positive number validation
- Date normalization
- Unit normalization
- Duplicate detection
- Classification
- Mapping
- Processing-status calculation

### Integration Tests

- File reading to database storage
- Shared database input processing
- Transaction rollback
- Reprocessing
- Module 3 data retrieval

### Test Cases

| ID | Test | Expected Result |
|---|---|---|
| TC-01 | Valid project | Processed and stored |
| TC-02 | Missing project name | Validation error |
| TC-03 | Negative lease area | Validation error |
| TC-04 | Unsupported unit | Warning or error |
| TC-05 | Duplicate observation | Duplicate flagged |
| TC-06 | Missing optional data | Ready with warning |
| TC-07 | Database failure | Rollback |
| TC-08 | Invalid file format | Controlled error |
| TC-09 | Valid structured data | Module 3 can read it |
| TC-10 | Critical errors present | Downstream use blocked |

---

## 24. Dev Container and Setup

Expected dependencies:

```text
pydantic
sqlalchemy
alembic
psycopg2-binary
asyncpg
pytest
pandas
openpyxl
```

Example environment variable:

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database
```

Development checks:

```bash
python3 -m pip check
npm ls --depth=0
ss -tulnp | egrep ':(8000|5173|5432)'
```

Module 2 itself does not require port 8000 because it does not expose an API.

---

## 25. Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Input format changes | Use separate readers |
| Missing data | Structured validation |
| Duplicate records | Duplicate checks and indexes |
| Wrong mapping | Preserve source and require review |
| Database failure | Transactions and rollback |
| Rule changes | Keep rules modular |
| Large files | Batch processing |
| Secret exposure | Environment variables and safe logs |
| Module mismatch | Shared internal data contract |

---

## 26. Technical Acceptance Criteria

1. No API-based dependency exists.
2. Data can be read from approved files or shared database tables.
3. Internal Python models are defined.
4. Validation returns structured issues.
5. Normalization is deterministic.
6. Classification is testable.
7. Mapping is testable.
8. Database changes use transactions.
9. Source references are preserved.
10. Alembic migrations are available.
11. Unit and integration tests pass.
12. Module 3 can read structured output.
13. Secrets are not committed.
14. The module runs in the Dev Container.
15. Mermaid diagrams render correctly on GitHub.

---

## 27. Future Technical Improvements

- Configurable validation-rule files
- Additional file readers
- Background processing
- Versioned project records
- Reviewer approval workflow
- Reference-data caching
- Processing metrics
- More sectors beyond mining
