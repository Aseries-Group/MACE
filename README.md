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








# Module 3: Generate PDF Reports and Display Them on the React Frontend

Module 3 takes the structured, validated compliance data produced by Module 2 and turns it into a finished PDF report that a user can read, download, and print directly inside the React frontend. Where Module 2 stops at "clean, structured sections stored in the database", Module 3 begins: it binds that data into a report template, renders a well formatted PDF on the server, stores the file, and streams it back to the browser for inline viewing.

This README contains the complete Software Design Document and Technical Design Document for Module 3. Module 3 is the report generation and presentation module, so unlike Module 2 it does expose a small backend service that the React frontend calls to request and retrieve reports.

---

# **SOFTWARE DESIGN DOCUMENT (SDD) STARTS HERE**

> **Module:** Generate PDF Reports and Display Them on the React Frontend
> **Project:** MACE — Mining Automated Compliance Execution
> **Prepared By:** Kirtika (2023A7PS0219U)
> **Standard:** IEEE Std 1016 — Software Design Descriptions
> **Status:** Draft for review

---

## 1. Module Overview

Module 3 is responsible for converting structured compliance data into a styled PDF report and presenting that report to the user inside the React single page application.

The module spans two tiers. On the backend it exposes a report service that accepts a report request, reads the structured data prepared by Module 2, binds it into a report template, and renders a PDF. On the frontend it provides a dashboard where the user requests a report, watches its status, and finally views the finished PDF inline with options to download and print.

The module is designed to be report-type agnostic. A new report type is added by supplying a new template and a query. The generation pipeline itself does not change.

Module 3 supports reports such as:

- Project Description report
- Baseline Environmental Condition report
- Environmental Impact Assessment summary
- Environmental Management Plan report
- Ecology and Biodiversity report
- Socio-Economic report
- Compliance Summary report

---

## 2. Purpose

The purpose of Module 3 is to give users a reliable, repeatable way to produce a formatted compliance report from data that already exists in the system, and to read that report without leaving the application.

The module reduces:

- Manual copying of data into word processors
- Inconsistent report formatting between users
- Time spent producing routine compliance documents
- Version confusion between the data and the printed report
- Dependence on desktop tools to view or print reports

---

## 3. Objectives

- Accept a report request from the React frontend.
- Validate the request and the requesting user's access.
- Read structured compliance data produced by Module 2.
- Bind the data into a report template.
- Render a well formatted PDF on the server.
- Store the generated PDF and record a reference to it.
- Return the report to the frontend for inline viewing.
- Allow the user to download and print the report.
- Keep a record of who generated which report and when.

---

## 4. Scope

### 4.1 Included

- Report request handling
- Report type selection
- Reading structured data from Module 2
- Template binding
- Server side PDF generation
- Storage of generated PDF files
- Report status tracking
- Inline PDF viewing in React
- Download and print actions
- Error and failure states
- Audit of report generation

### 4.2 Not Included

- Creation or correction of the source business data (owned by Module 2)
- Authentication mechanics (owned by the shared security module)
- Long term archival and retention policy
- Direct submission of reports to government portals
- Editing of the PDF inside the browser
- Automatic content writing of the report body

---

## 5. Stakeholders and Users

| User / Stakeholder | Role |
|---|---|
| Environmental consultant | Requests and reads compliance reports |
| Compliance team | Reviews generated reports before submission |
| Project coordinator | Tracks which reports have been produced |
| Reviewer | Reads the PDF and approves or returns it |
| Module 2 | Supplies structured compliance data |
| Shared security module | Issues and validates access tokens |
| Administrator | Maintains report templates and types |
| Developer | Implements and tests the module |

---

## 6. Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | The module shall accept a report request specifying a project and a report type. |
| FR-02 | The module shall validate the request payload before any work begins. |
| FR-03 | The module shall confirm the user is allowed to access the requested project. |
| FR-04 | The module shall read the structured compliance data from Module 2. |
| FR-05 | The module shall bind the data into the selected report template. |
| FR-06 | The module shall render a PDF document from the bound template. |
| FR-07 | The module shall store the generated PDF in file or object storage. |
| FR-08 | The module shall record report metadata and a reference to the stored file. |
| FR-09 | The module shall return the report status to the frontend. |
| FR-10 | The module shall render the PDF inline in the React frontend. |
| FR-11 | The module shall allow the user to download the report. |
| FR-12 | The module shall allow the user to print the report. |
| FR-13 | The module shall allow a failed report to be retried. |
| FR-14 | The module shall record who requested each report and when. |

---

## 7. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Responsiveness | The frontend shall stay usable while a report is generating. |
| NFR-02 | Reliability | A failure at any stage shall produce a clear, recoverable state. |
| NFR-03 | Security | Storage and database credentials shall remain outside source control. |
| NFR-04 | Testability | Template binding and PDF rendering shall support automated testing. |
| NFR-05 | Portability | The module shall run inside the project Dev Container. |
| NFR-06 | Correctness | The generated PDF shall faithfully reflect the underlying data. |
| NFR-07 | Reusability | New report types shall be added through templates, not pipeline changes. |
| NFR-08 | Auditability | Report requests and generations shall be traceable. |

---

## 8. Use Cases

### 8.1 Generate a Report

1. The user opens the report dashboard.
2. The user selects a project and a report type.
3. The frontend sends a report request.
4. The backend validates and authorizes the request.
5. The backend reads the structured data and renders a PDF.
6. The PDF is stored and marked ready.
7. The frontend loads the PDF inline.

### 8.2 View, Download, and Print

1. The user opens a ready report.
2. The PDF renders inside the viewer.
3. The user downloads the file if required.
4. The user prints the file if required.

### 8.3 Handle a Failed Report

1. Generation fails at some stage.
2. The report is marked failed with a reason.
3. The user sees a clear error and a retry action.
4. The user retries without re-entering the request.

---

## 9. High-Level Architecture

```mermaid
flowchart LR
    A[React Frontend] --> B[Report API Layer]
    B --> C[Validation and Authorization]
    C --> D[Report Service]
    D --> E[(Module 2 Structured Data)]
    D --> F[Template Engine]
    F --> G[PDF Generation]
    G --> H[(Object Storage)]
    H --> I[React PDF Viewer]
    D --> J[Errors and Status]
```

The data flow is unidirectional. The frontend talks only to the API layer and never reaches the database or storage directly.

---

## 10. Report Generation Workflow

```mermaid
flowchart TD
    A[Receive report request] --> B{Payload valid?}
    B -- No --> C[Return validation error]
    B -- Yes --> D{User authorized?}
    D -- No --> E[Return access error]
    D -- Yes --> F[Mark request as generating]
    F --> G{Required data available?}
    G -- No --> H[Mark failed with reason]
    G -- Yes --> I[Bind data into template]
    I --> J[Render PDF]
    J --> K{Render succeeded?}
    K -- No --> H
    K -- Yes --> L[Store PDF]
    L --> M[Mark ready and save reference]
    M --> N[Frontend loads PDF viewer]
```

---

## 11. Module Interaction

```mermaid
flowchart LR
    SEC[Shared Security Module] -->|Validated token| M3[Module 3]
    M2[Module 2] -->|Structured compliance data| M3
    M3 -->|Report request and status| FE[React Frontend]
    M3 -->|PDF file| ST[(Object Storage)]
    ST -->|Signed URL| FE
```

Module 3 reads Module 2 data and does not modify it.

---

## 12. Component Design

### 12.1 Report API

Exposes the report endpoints, checks the access token, validates the payload, and shapes the HTTP response. Contains no business logic.

### 12.2 Report Service

Orchestrates the pipeline: read data, bind template, render PDF, store file, update status. Owns the lifecycle of a report request.

### 12.3 Template Engine

Merges a data object into an HTML report template and returns populated HTML. Has no knowledge of PDF or storage.

### 12.4 PDF Generator

Converts populated HTML into a PDF document. Has no knowledge of the database.

### 12.5 Storage Component

Writes the PDF to object storage and returns a retrievable URL.

### 12.6 Frontend Viewer

Renders the PDF inline and provides download and print actions, along with generating and failed states.

---

## 13. Data Flow Design

```mermaid
flowchart LR
    R[Report Request] --> S[Report Service]
    D1[(Module 2 Structured Data)] --> S
    T[Report Template] --> S
    S --> P[Populated HTML]
    P --> PDF[PDF Buffer]
    PDF --> ST[(Object Storage)]
    ST --> V[React PDF Viewer]
    S --> M[(Report Metadata)]
```

---

## 14. Data Design

```mermaid
erDiagram
    REPORT_TEMPLATE ||--o{ REPORT_REQUEST : defines
    REPORT_REQUEST ||--o| GENERATED_REPORT : produces
    PROJECT ||--o{ REPORT_REQUEST : has

    REPORT_TEMPLATE {
        uuid template_id PK
        string template_code
        string template_name
        string template_file
        string version
        boolean is_active
    }

    REPORT_REQUEST {
        uuid request_id PK
        uuid project_id FK
        uuid template_id FK
        string requested_by
        string status
        text error_message
        datetime requested_at
        datetime completed_at
    }

    GENERATED_REPORT {
        uuid report_id PK
        uuid request_id FK
        string storage_key
        string file_url
        int file_size_bytes
        int page_count
        string template_version
        datetime generated_at
    }
```

---

## 15. Input and Output Design

### Example Input

```json
{
  "project_id": "example-project-uuid",
  "template_code": "COMPLIANCE_SUMMARY",
  "options": {
    "include_annexures": true,
    "period_from": "2026-01-01",
    "period_to": "2026-06-30"
  }
}
```

### Example Output

```json
{
  "request_id": "generated-uuid",
  "status": "ready",
  "file_url": "https://storage.example.com/reports/generated-uuid.pdf",
  "page_count": 24,
  "file_size_bytes": 862140,
  "generated_at": "2026-06-29T10:22:41Z"
}
```

---

## 16. Validation Rules

| Rule ID | Rule |
|---|---|
| VR-01 | Project identifier is mandatory. |
| VR-02 | Report type code is mandatory. |
| VR-03 | The report type must exist and be active. |
| VR-04 | The project must exist and be accessible to the user. |
| VR-05 | Required compliance sections must exist before generation. |
| VR-06 | Status must be one of generating, ready, or failed. |
| VR-07 | A failed request must record an error message. |
| VR-08 | A stored report reference is written only after upload succeeds. |

---

## 17. Error Handling

The module shall handle:

- Invalid request payloads
- Unauthorized project access
- Missing required compliance data
- Template binding failures
- PDF rendering failures or timeouts
- Storage upload failures
- Viewer load failures on the frontend

Each failure should record:

- The stage that failed
- A clear message
- The request reference
- The report type and template version where relevant

A request is never left silently stuck in the generating state, and a partial PDF is never presented as a finished report.

---

## 18. Security

- `.env` must not be committed.
- Storage and database credentials must be read from environment variables.
- All traffic must use HTTPS.
- Generated PDFs must be stored in a private location and served through short lived signed URLs.
- Every report endpoint must validate the access token.
- Project access must be checked on the server for every request, including file retrieval.
- Sensitive site data must not be written to world readable temporary locations.
- Report access must be traceable.

---

## 19. Assumptions and Dependencies

### Assumptions

- Module 2 supplies validated, structured compliance data.
- The shared security module issues and validates access tokens.
- A human reviewer remains responsible for final report correctness.
- Initial reporting focuses on mining compliance documents.

### Dependencies

- Node.js and Express
- Puppeteer with a headless browser
- A template engine for HTML report layouts
- PostgreSQL for report metadata
- Object storage for PDF files
- React with react-pdf for the frontend
- Docker Desktop and the VS Code Dev Container

### Constraints

- No editing of PDF content in the browser.
- No direct government portal submission.
- No responsibility for creating the source data.
- No ownership of authentication.

---

## 20. Acceptance Criteria

1. A user can request a report from the React dashboard.
2. The request is validated and authorized.
3. Structured Module 2 data is read correctly.
4. A well formatted PDF is generated.
5. The PDF is stored and referenced.
6. The report renders inline in the frontend.
7. The user can download and print the report.
8. The frontend stays usable while generating.
9. Every failure produces a clear, recoverable state.
10. A user cannot access a report for a project they are not assigned to.
11. Each report records who requested it and which template version was used.
12. A new report type can be added through a template.

---

## 21. Future Enhancements

- Additional report types and templates
- Scheduled and automatic report generation
- Export to Word in addition to PDF
- Digital signing of generated reports
- Template preview before full generation
- Report comparison across periods
- Reviewer approval workflow inside the viewer

---

# **TECHNICAL DESIGN DOCUMENT (TDD) STARTS HERE**

> **Module:** Generate PDF Reports and Display Them on the React Frontend
> **Project:** MACE — Mining Automated Compliance Execution
> **Prepared By:** Kirtika (2023A7PS0219U)
> **Technology Focus:** Node.js and Express backend, Puppeteer PDF generation, React frontend
> **Status:** Draft for review

---

## 1. Technical Overview

Module 3 is designed as a report generation and presentation module.

On the backend it runs a small Node.js and Express service that exposes report endpoints to the React frontend. It reads structured compliance data prepared by Module 2, binds that data into an HTML report template, and uses Puppeteer to render the template into a PDF document. The PDF is stored in object storage and a reference is saved in the database.

On the frontend it uses React with react-pdf to render the generated report inline, along with download and print actions.

The module performs:

- Report request handling
- Validation and authorization
- Data reading from Module 2
- Template binding
- PDF rendering with Puppeteer
- Storage and metadata recording
- Status reporting
- Inline rendering in React

---

## 2. Technical Scope

### Included

- Express report routes and controllers
- Request validation
- Report orchestration service
- HTML template engine integration
- Puppeteer PDF rendering
- Object storage access
- Report metadata tables
- React report dashboard and viewer
- Unit and integration tests
- Dev Container execution

### Excluded

- Creation of source business data
- Authentication implementation
- Browser side PDF editing
- Direct PARIVESH integration
- Long term archival policy

---

## 3. Technology Stack

| Area | Technology | Purpose |
|---|---|---|
| Backend runtime | Node.js with Express | Expose report endpoints and orchestrate generation |
| PDF rendering | Puppeteer | Render HTML report templates into PDF |
| Templating | HTML template engine | Bind compliance data into report layouts |
| Database | PostgreSQL | Store report request and generated report metadata |
| Storage | Object storage (S3 compatible) | Store generated PDF files |
| Frontend | React with react-pdf | Request reports and render PDFs inline |
| Container | Docker Dev Container | Reproducible environment |
| Testing | Jest and integration tests | Unit and integration testing |

---

## 4. Technical Architecture

```mermaid
flowchart TB
    subgraph Frontend
        DASH[Report Dashboard]
        VIEW[React PDF Viewer]
    end

    subgraph Module_3_Backend
        API[Express Routes and Controllers]
        VAL[Validation and Authorization]
        SVC[Report Service]
        TMP[Template Engine]
        PDF[Puppeteer PDF Generator]
        REPO[Report Repository]
        STG[Storage Client]
    end

    subgraph Storage_and_Sources
        M2[(Module 2 Structured Data)]
        DB[(PostgreSQL Metadata)]
        OBJ[(Object Storage)]
    end

    DASH --> API
    API --> VAL
    VAL --> SVC
    SVC --> M2
    SVC --> TMP
    TMP --> PDF
    PDF --> STG
    STG --> OBJ
    SVC --> REPO
    REPO --> DB
    OBJ --> VIEW
```

---

## 5. Design Principles

### 5.1 Separation of Responsibilities

Data reading, template binding, PDF rendering, storage, and display are separate units with defined interfaces.

### 5.2 Report Type Agnostic Pipeline

The pipeline does not change per report type. A report type is a template plus a query.

### 5.3 Asynchronous Generation

A report request returns immediately with a status so the frontend stays responsive.

### 5.4 Reuse of the Browser Instance

A single Puppeteer browser is reused across requests because launching is the dominant cost.

### 5.5 Traceability

Every generated report records the template version used, so an old report can be explained.

---

## 6. Proposed Folder Structure

```text
module3/
├── api/
│   ├── reportRoutes.js
│   ├── reportController.js
│   └── validators.js
├── services/
│   ├── reportService.js
│   ├── templateService.js
│   └── pdfService.js
├── data/
│   ├── reportRepository.js
│   └── complianceRepository.js
├── storage/
│   └── objectStorage.js
├── templates/
│   ├── base.html
│   └── compliance_report.html
├── utils/
│   ├── logger.js
│   └── errors.js
└── tests/
    ├── unit/
    └── integration/

frontend/src/module3/
├── ReportDashboard.jsx
├── ReportViewer.jsx
├── ReportStatus.jsx
└── api/reportApi.js
```

This is a proposed structure and should be adjusted to the final MACE repository.

---

## 7. Main Components

### 7.1 Report Controller

```javascript
async function requestReport(req, res) {
  // validate payload, authorize user,
  // create request, trigger generation,
  // return 202 with request id
}
```

### 7.2 Report Service

```javascript
async function generateReport(requestId) {
  // read compliance data
  // bind template
  // render pdf
  // store file
  // update status
}
```

### 7.3 Template Service

```javascript
function renderTemplate(templateCode, data) {
  // return populated HTML string
}
```

### 7.4 PDF Service

```javascript
async function htmlToPdf(html) {
  // render HTML in headless browser
  // return PDF buffer
}
```

### 7.5 Report Repository

```javascript
async function createRequest(request) { /* ... */ }
async function updateStatus(requestId, status) { /* ... */ }
async function saveGeneratedReport(report) { /* ... */ }
```

---

## 8. Processing Sequence

```mermaid
sequenceDiagram
    participant FE as React Frontend
    participant API as Express API
    participant SVC as Report Service
    participant M2 as Module 2 Data
    participant PDF as Puppeteer
    participant ST as Object Storage
    participant DB as PostgreSQL

    FE->>API: POST report request
    API->>API: Validate and authorize
    API->>DB: Create request (generating)
    API-->>FE: 202 Accepted with request id
    API->>SVC: Start generation
    SVC->>M2: Read structured data
    M2-->>SVC: Compliance sections
    SVC->>PDF: Render bound template
    PDF-->>SVC: PDF buffer
    SVC->>ST: Upload PDF
    ST-->>SVC: Storage key and URL
    SVC->>DB: Update request (ready)
    FE->>API: GET report status
    API-->>FE: Ready with file URL
    FE->>ST: Load PDF into viewer
```

---

## 9. Internal Data Models

### Report Request Model

```javascript
const ReportRequest = {
  requestId: "uuid",
  projectId: "uuid",
  templateCode: "string",
  requestedBy: "string",
  status: "generating | ready | failed",
  errorMessage: "string | null"
};
```

### Generated Report Model

```javascript
const GeneratedReport = {
  reportId: "uuid",
  requestId: "uuid",
  storageKey: "string",
  fileUrl: "string",
  fileSizeBytes: 0,
  pageCount: 0,
  templateVersion: "string"
};
```

---

## 10. Database Design

### Report Template Table

| Field | Type |
|---|---|
| template_id | UUID |
| template_code | VARCHAR |
| template_name | VARCHAR |
| template_file | VARCHAR |
| version | VARCHAR |
| is_active | BOOLEAN |

### Report Request Table

| Field | Type |
|---|---|
| request_id | UUID |
| project_id | UUID |
| template_id | UUID |
| requested_by | VARCHAR |
| status | VARCHAR |
| error_message | TEXT |
| requested_at | TIMESTAMP |
| completed_at | TIMESTAMP |

### Generated Report Table

| Field | Type |
|---|---|
| report_id | UUID |
| request_id | UUID |
| storage_key | VARCHAR |
| file_url | VARCHAR |
| file_size_bytes | INTEGER |
| page_count | INTEGER |
| template_version | VARCHAR |
| generated_at | TIMESTAMP |

---

## 11. API Design

Module 3 exposes a small set of REST endpoints to the React frontend.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/reports | Request generation of a report. Returns 202 with a request id. |
| GET | /api/reports/{id} | Return the status of a request, and the file URL when ready. |
| GET | /api/reports/{id}/file | Stream or redirect to the PDF for viewing and download. |
| GET | /api/reports?project_id= | List previous reports for a project. |
| GET | /api/report-templates | List active report types the user may request. |
| POST | /api/reports/{id}/retry | Retry a failed request. |

The request that starts generation returns immediately with status generating, and the frontend polls the status endpoint until the report is ready.

---

## 12. Template and Rendering Design

The report layout is authored in HTML and CSS so that new report types can be styled with familiar tools.

Rendering steps:

1. Load the template file for the requested report type.
2. Bind the compliance data into the template.
3. Pass the populated HTML to Puppeteer.
4. Render to a PDF buffer with a fixed page size and margins.
5. Enforce a render timeout and release the page afterwards.

```javascript
async function htmlToPdf(html) {
  const page = await browser.newPage();
  try {
    await page.setContent(html, { waitUntil: "networkidle0" });
    return await page.pdf({ format: "A4", printBackground: true });
  } finally {
    await page.close();
  }
}
```

---

## 13. Frontend Rendering Design

The frontend uses react-pdf to render the generated PDF inline.

Responsibilities:

- Request a report and show a generating state
- Poll the status endpoint until the report is ready
- Render the PDF inside the viewer
- Provide download and print actions
- Show a clear failed state with a retry action

```javascript
import { Document, Page } from "react-pdf";

function ReportViewer({ fileUrl, pageCount }) {
  // render Document with fileUrl and map pages
}
```

---

## 14. Error Handling

Custom error categories may include:

```javascript
class ReportError extends Error {}
class ValidationError extends ReportError {}
class DataUnavailableError extends ReportError {}
class RenderError extends ReportError {}
class StorageError extends ReportError {}
```

Expected error situations:

- Invalid request payload
- Unauthorized project access
- Missing required compliance data
- Template binding failure
- Puppeteer render failure or timeout
- Storage upload failure
- Frontend viewer load failure

No internal stack trace should be shown to normal users. Each failure is recorded with a stage, a message, and the request reference.

---

## 15. Performance Considerations

- Reuse a single Puppeteer browser instance instead of launching per request.
- Generate asynchronously so the HTTP request is not blocked.
- Cap concurrent generation to protect memory.
- Cache a generated report by its key and reuse it when the data is unchanged.
- Index report tables on the request id and the project id.
- Enforce a render timeout to prevent runaway pages.

---

## 16. Security Requirements

- Keep `.env` in `.gitignore`.
- Read storage and database credentials from environment variables.
- Validate the access token on every endpoint, including file retrieval.
- Serve PDFs through short lived signed URLs from a private bucket.
- Authorize project access on the server for every request.
- Do not log report contents or personal data, only identifiers.
- Do not write sensitive PDFs to world readable temporary directories.

---

## 17. Logging and Audit

Suggested log information:

- Timestamp
- Request id
- Report type and template version
- Pipeline stage
- Generation duration
- Error count and reason
- Final status

Audit events:

- Report requested
- Report generated
- Report failed
- Report downloaded
- Report retried

---

## 18. Testing Strategy

### Unit Tests

- Payload validation
- Template binding output
- PDF buffer generation
- Repository create, read, and status update
- Storage upload and URL generation
- Error class behavior

### Integration Tests

- Full pipeline from request to ready
- Missing data producing a failed state
- Unauthorized project access
- Retry of a failed request
- Frontend rendering, download, and failed states

### Test Cases

| ID | Test | Expected Result |
|---|---|---|
| TC-01 | Valid request with complete data | Accepted, then ready with a working URL |
| TC-02 | Missing template code | Validation error, no request created |
| TC-03 | Non-existent project | Error, no generation attempted |
| TC-04 | Unauthorized project | Access error, no request created |
| TC-05 | Inactive template | Error stating the type is unavailable |
| TC-06 | Missing required section | Failed with a clear reason |
| TC-07 | Render timeout | Failed, retry offered, page released |
| TC-08 | Storage upload fails | Failed, no report reference written |
| TC-09 | Ready PDF opens in viewer | All pages render, page count matches |
| TC-10 | Download and print | Downloaded file matches the stored file |
| TC-11 | Duplicate request | Stored report reused, not regenerated |
| TC-12 | Expired token on file endpoint | Access denied, PDF not served |

---

## 19. Dev Container and Setup

Expected dependencies:

```text
express
puppeteer
pg
aws-sdk (or S3 compatible client)
jest
react
react-pdf
```

Example environment variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/mace
STORAGE_ENDPOINT=http://localhost:9000
STORAGE_BUCKET=mace-reports
PDF_RENDER_TIMEOUT_MS=30000
PDF_MAX_CONCURRENCY=2
REPORT_URL_TTL_SECONDS=900
```

Puppeteer needs headless browser libraries installed in the Dev Container image. If they are missing, the browser fails to launch and every generation fails at the same point. This is the most common setup issue for this module.

Development checks:

```bash
python3 -m pip check
npm ls --depth=0
ss -tulnp | egrep ':(8000|5173|5432)'
```

---

## 20. Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Puppeteer fails to launch in the container | Install browser libraries in the Dev Container image and smoke test on startup |
| Large reports render slowly | Generate asynchronously, reuse the browser, cap concurrency, cache reports |
| Memory growth from unreleased pages | Close each page in a finally block and enforce a timeout |
| PDF layout differs from the approved design | Keep templates in version control and record the template version |
| Incomplete data produces a misleading report | Validate required sections before rendering and fail with a clear reason |
| Report URLs leak sensitive data | Private bucket with short lived signed URLs and per request authorization |
| Frontend appears frozen | Return immediately and show an explicit generating status |
| Template change breaks old reports | Store the template version and keep the generated PDF |

---

## 21. Technical Acceptance Criteria

1. A report can be requested from the React frontend.
2. Requests are validated and authorized.
3. Structured Module 2 data is read correctly.
4. Templates bind data into HTML.
5. Puppeteer renders a valid PDF.
6. Generated PDFs are stored and referenced.
7. Generation runs asynchronously.
8. Every failure resolves to a recoverable state.
9. The PDF renders inline in the frontend.
10. Download and print work correctly.
11. Report metadata records requester and template version.
12. Unit and integration tests pass.
13. Secrets are not committed.
14. The module runs in the Dev Container.
15. Mermaid diagrams render correctly on GitHub.

---

## 22. Future Technical Improvements

- A job queue with workers so generation survives a restart
- Server sent events or websockets to replace status polling
- Scheduled report generation
- Export to Word reusing the same template layer
- Digital signing of generated reports
- Template preview screen
- Generation metrics and dashboards
