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


---

# Module 1: Scheduled EC/FC Mining Clearance Scraper

This README section contains the SDD and TDD for Module 1 only. It is written as GitHub Markdown text so it can be pasted directly into the repository `README.md` or submitted as a pull request without uploading Word `.docx` files.

## Reference Links Used

- [Atlassian - Software Design Document Tips and Best Practices](https://www.atlassian.com/work-management/knowledge-sharing/documentation/software-design-document)
- [Medium - The Ultimate Guide to Writing a Great README.md for Your Project](https://medium.com/@kc_clintone/the-ultimate-guide-to-writing-a-great-readme-md-for-your-project-3d49c2023357)

## Acronyms

| Acronym | Meaning |
|---|---|
| EC | Environmental Clearance |
| FC | Forest Clearance |
| SDD | Software/System Design Document |
| TDD | Technical Design Document |
| UI | User Interface |
| DB | Database |
| DOM | Document Object Model |

## Module Summary

Module 1 is responsible for building a scheduled web scraper that collects Environmental Clearance and Forest Clearance data for mining-sector projects only. The target websites are assumed to be UI-only and JavaScript-rendered, meaning the module cannot depend on a public API. The scraper must open the pages like a browser, wait for the UI content to load, extract listing and detail records, filter the records to mining projects, normalize the extracted fields, and keep a local database updated through repeated scheduled runs.

This module is important because the rest of the application depends on having clean, current, and traceable EC/FC project data. If this ingestion layer is weak, later modules such as analytics, dashboards, reporting, search, or alerts will also become unreliable.

---

# 1. SDD - Software/System Design Document

## 1.1 Purpose

The purpose of Module 1 is to design a reliable local data ingestion system for EC and FC clearance records related to mining-sector projects. Since the source portals do not provide a usable API, the module must use browser automation to interact with JavaScript-rendered pages.

The module must:

- Run automatically on a recurring schedule.
- Scrape EC and FC records from UI pages.
- Extract listing-page and detail-page data.
- Keep only mining-sector records.
- Store normalized records in a local database.
- Detect new, updated, unchanged, failed, and possibly missing records.
- Maintain logs and scrape history for debugging and audit purposes.

## 1.2 Problem Statement

Environmental and forest clearance information is usually published across web portals that are designed for human browsing. These pages may require JavaScript rendering, pagination, filtering, clicking detail pages, or downloading linked documents. Because no direct API is available, manually collecting this data is slow, inconsistent, and difficult to repeat.

Module 1 solves this problem by automating the data collection process while keeping the system safe, traceable, and repeatable.

## 1.3 Goals

- Build a recurring scraper for EC and FC data.
- Support JavaScript-rendered pages using browser automation.
- Extract records consistently from listing and detail pages.
- Filter results so only mining-sector projects are stored.
- Store data in a local database using idempotent upsert logic.
- Preserve raw scraped payloads for traceability.
- Track every scrape run and every error.
- Support future modules by providing clean and normalized data.

## 1.4 Non-Goals

This module will not:

- Submit EC or FC applications.
- Modify any government or public portal data.
- Bypass captchas, authentication, paywalls, or access controls.
- Scrape unrelated sectors for final storage.
- Build a full analytics dashboard.
- Provide real-time streaming updates.
- Replace official records or legal verification.

## 1.5 Assumptions

- EC and FC data is available through public UI pages.
- Source pages are JavaScript-rendered and require browser automation.
- No reliable public API exists for the required data.
- Mining-sector identification can be performed using source fields and fallback keywords.
- A local database is acceptable for the first implementation.
- The scraper will run on a controlled schedule instead of continuously.
- Source portal layouts may change, so selectors must be isolated and testable.

## 1.6 Scope

### In Scope

- Scheduled EC scraping.
- Scheduled FC scraping.
- Browser-rendered page loading.
- Listing-page extraction.
- Detail-page extraction.
- Mining-sector filtering.
- Data normalization.
- Local database persistence.
- Change detection.
- Scrape run logs.
- Error logs.
- Retry handling.
- Screenshot or HTML capture for debugging failures.

### Out of Scope

- Non-mining project storage.
- User interface screens.
- Authentication workflows.
- Captcha solving.
- Cloud deployment automation.
- Legal validation of clearance decisions.

## 1.7 Users and Stakeholders

| Stakeholder | Interest in Module |
|---|---|
| Developers | Need a clear architecture and implementation plan. |
| Data users | Need accurate and current EC/FC records. |
| Project maintainers | Need scheduled ingestion that can be monitored and debugged. |
| Future module owners | Need normalized data for dashboards, reports, search, or analytics. |
| Reviewers/teachers | Need evidence that the module architecture, data flow, and technical plan are understood before coding. |

## 1.8 External Systems

| External System | Role |
|---|---|
| EC source portal | Provides Environmental Clearance records through UI pages. |
| FC source portal | Provides Forest Clearance records through UI pages. |
| Local file system | Stores debug screenshots, optional HTML snapshots, logs, or downloaded documents. |
| Local database | Stores normalized clearance data, scrape runs, errors, and change history. |

## 1.9 High-Level Context Diagram

```mermaid
flowchart LR
    Scheduler["Scheduler"] --> Scraper["Module 1 Scraper"]
    Scraper --> EC["EC Portal UI"]
    Scraper --> FC["FC Portal UI"]
    EC --> Scraper
    FC --> Scraper
    Scraper --> DB["Local Database"]
    Scraper --> Logs["Run Logs and Error Logs"]
    Scraper --> Files["Debug Files / Screenshots / Optional Documents"]
    DB --> Future["Future Modules: Search, Dashboard, Reports, Analytics"]
```

## 1.10 System Architecture

```mermaid
flowchart TD
    A["Scheduler"] --> B["Scrape Orchestrator"]
    B --> C["EC Scraper Adapter"]
    B --> D["FC Scraper Adapter"]
    C --> E["Browser Renderer"]
    D --> E
    E --> F["Rendered Listing Pages"]
    F --> G["Listing Extractor"]
    G --> H["Detail Page Extractor"]
    H --> I["Raw Record Payload"]
    I --> J["Mining-Sector Filter"]
    J --> K["Normalizer"]
    K --> L["Validator"]
    L --> M["Content Hash Generator"]
    M --> N["Persistence Service"]
    N --> O["Local Database"]
    B --> P["Run Logger"]
    E --> Q["Error Logger"]
    H --> Q
    N --> Q
```

## 1.11 Component Responsibilities

| Component | Responsibility | Output |
|---|---|---|
| Scheduler | Starts scraping jobs based on configured time intervals. | Run trigger |
| Scrape Orchestrator | Coordinates the full scrape workflow. | Run summary |
| EC Scraper Adapter | Handles EC-specific URLs, filters, selectors, pagination, and extraction. | Raw EC records |
| FC Scraper Adapter | Handles FC-specific URLs, filters, selectors, pagination, and extraction. | Raw FC records |
| Browser Renderer | Loads JavaScript-rendered pages using a browser automation tool. | Rendered DOM, screenshots |
| Listing Extractor | Reads records from tables, cards, or listing views. | Listing records |
| Detail Extractor | Opens detail pages and extracts full record fields. | Raw detail payload |
| Mining Filter | Keeps only mining-sector records. | Accepted or rejected decision |
| Normalizer | Converts inconsistent source fields into the local schema. | Normalized record |
| Validator | Checks required fields and data formats. | Valid record or validation error |
| Hash Generator | Creates stable hashes for change detection. | Content hash |
| Persistence Service | Inserts, updates, or marks records unchanged. | Database result |
| Run Logger | Stores run-level metrics. | Scrape run record |
| Error Logger | Stores failures, retry counts, URLs, and debug paths. | Error record |

## 1.12 Main Data Flow

```mermaid
sequenceDiagram
    autonumber
    participant S as Scheduler
    participant O as Orchestrator
    participant A as EC/FC Adapter
    participant B as Browser Renderer
    participant F as Mining Filter
    participant N as Normalizer
    participant P as Persistence
    participant D as Local Database

    S->>O: Start scheduled run
    O->>D: Create scrape_run record
    O->>A: Start EC or FC scrape
    A->>B: Open listing page
    B-->>A: Rendered DOM
    A->>A: Extract listing rows
    A->>B: Open detail pages
    B-->>A: Rendered detail DOM
    A-->>O: Raw records
    O->>F: Check mining relevance
    F-->>O: Accepted mining record
    O->>N: Normalize record
    N-->>O: Canonical record
    O->>P: Upsert record
    P->>D: Insert, update, or unchanged
    O->>D: Finalize scrape_run metrics
```

## 1.13 Mining-Sector Filtering Design

The module must store only mining-sector records. Filtering should happen after extraction but before final database persistence.

### Preferred Filtering

Use source-provided structured fields when available:

- Sector
- Project category
- Proposal type
- Industry type
- Clearance category
- Mineral name
- Mining lease information

### Fallback Keyword Filtering

If structured fields are missing or inconsistent, inspect text fields such as project name, description, proposal summary, and document titles.

Mining indicators include:

- mining
- mine
- mineral
- coal
- iron ore
- bauxite
- limestone
- quarry
- mining lease
- lease area
- extraction
- beneficiation
- manganese
- dolomite
- laterite
- granite
- sand mining

### Rejection Examples

Records should be rejected when they clearly belong to unrelated sectors such as:

- highways
- buildings
- hospitals
- tourism
- irrigation
- non-mining manufacturing
- residential townships
- ports unrelated to mining

### Filtering Decision Flow

```mermaid
flowchart TD
    A["Raw scraped record"] --> B{"Structured sector field exists?"}
    B -- Yes --> C{"Sector says mining/mineral/coal/quarry?"}
    C -- Yes --> D["Accept as mining record"]
    C -- No --> E["Reject as non-mining"]
    B -- No --> F["Run keyword classification"]
    F --> G{"Strong mining terms found?"}
    G -- Yes --> D
    G -- No --> H{"Ambiguous terms?"}
    H -- Yes --> I["Log for review / skip final storage"]
    H -- No --> E
```

## 1.14 Local Database Design

The local database stores both the latest version of each clearance record and the operational history needed to understand how that data was collected.

### Main Entities

| Entity | Purpose |
|---|---|
| `clearance_projects` | Stores the latest known EC/FC data for each mining project. |
| `scrape_runs` | Stores one row for every scheduled, manual, or backfill run. |
| `scrape_errors` | Stores page-level and record-level errors. |
| `clearance_change_history` | Stores old and new payloads when a record changes. |
| `source_documents` | Stores links to clearance letters, PDFs, or supporting documents found during scraping. |

## 1.15 ER Diagram

```mermaid
erDiagram
    clearance_projects ||--o{ clearance_change_history : has
    clearance_projects ||--o{ source_documents : has
    scrape_runs ||--o{ scrape_errors : records
    scrape_runs ||--o{ clearance_change_history : creates

    clearance_projects {
        int id PK
        string clearance_type
        string source_record_id
        string proposal_number
        string project_name
        string project_proponent
        string sector
        string state
        string district
        string status
        string content_hash
        datetime first_seen_at
        datetime last_seen_at
        datetime last_changed_at
        boolean is_active
    }

    scrape_runs {
        int id PK
        string run_type
        datetime started_at
        datetime finished_at
        string status
        int records_found
        int records_inserted
        int records_updated
        int records_failed
    }

    scrape_errors {
        int id PK
        int scrape_run_id FK
        string clearance_type
        string url
        string error_type
        string error_message
        int retry_count
    }

    clearance_change_history {
        int id PK
        int project_id FK
        int scrape_run_id FK
        text old_payload
        text new_payload
        string old_hash
        string new_hash
        datetime changed_at
    }

    source_documents {
        int id PK
        int project_id FK
        string document_type
        string document_url
        datetime discovered_at
    }
```

## 1.16 Data Freshness and Update Rules

The scraper should not blindly replace records every time it runs. It should compare the new normalized data with the existing database record.

| Case | Meaning | Action |
|---|---|---|
| New record | Record does not exist in database. | Insert new row. |
| Existing unchanged record | Record exists and content hash is the same. | Update `last_seen_at` only. |
| Existing changed record | Record exists and content hash is different. | Save change history and update current row. |
| Missing record | Previously seen record is not found in current run. | Do not immediately delete; mark inactive only after repeated missed runs. |
| Failed record | Page or detail extraction failed. | Log error and retry if allowed. |

## 1.17 Scheduling Requirements

| Run Type | Suggested Frequency | Purpose |
|---|---:|---|
| Incremental scrape | Daily | Capture new or recently updated records. |
| Recent reconciliation | Weekly | Recheck recent records for delayed updates. |
| Full reconciliation | Monthly | Detect drift between source portals and local DB. |
| Manual backfill | On demand | Load historical records or recover after scraper changes. |

The scheduler must prevent overlapping runs. If a previous run is still active, the next scheduled run should either be skipped or delayed.

## 1.18 Reliability Requirements

- Retry transient failures with exponential backoff.
- Continue scraping after individual record failures.
- Log every failed URL.
- Capture screenshot or HTML snapshot for selector failures.
- Store raw payloads for later reprocessing.
- Keep selectors isolated so portal UI changes are easier to fix.
- Use conservative stale-record logic to avoid false deletion.

## 1.19 Security and Ethical Requirements

- Do not hardcode credentials, tokens, API keys, or proxy secrets.
- Do not bypass captchas, login pages, or anti-abuse controls.
- Use environment variables for configuration.
- Treat scraped data as untrusted input.
- Validate all extracted fields before writing to the database.
- Use parameterized SQL or ORM-based writes.
- Sanitize scraped text before displaying it in any UI.
- Use polite scraping speeds to avoid overloading source portals.
- Keep logs free of secrets and private credentials.

## 1.20 SDD Acceptance Criteria

The system design is acceptable when:

- EC and FC sources are represented as separate adapters.
- The scraper supports JavaScript-rendered pages.
- The workflow includes listing extraction and detail extraction.
- Mining-sector filtering is clearly defined.
- The database design supports current records, run history, error history, document links, and change history.
- The design includes retry handling and non-overlapping scheduled runs.
- The design explains how duplicates and updates are handled.
- The design includes diagrams showing architecture, flow, and database relationships.

---

# 2. TDD - Technical Design Document

## 2.1 Technical Objective

The technical objective is to implement Module 1 as a maintainable, testable, and scheduled scraper service. The implementation should separate source-specific scraping logic from shared processing logic so EC and FC pages can evolve independently.

## 2.2 Recommended Technology Stack

| Concern | Recommended Tool | Reason |
|---|---|---|
| Language | Python 3.11+ | Good support for scraping, scheduling, data validation, and testing. |
| Browser automation | Playwright | Handles JavaScript-rendered pages, waiting, screenshots, and browser contexts. |
| Scheduler | APScheduler or cron | Simple recurring runs. |
| Database | SQLite for local prototype, PostgreSQL for production | Easy local setup with a clean migration path. |
| ORM | SQLAlchemy | Safer database operations and clearer models. |
| Migrations | Alembic | Version-controlled schema evolution. |
| Testing | pytest | Unit and integration testing. |
| Coverage | pytest-cov | Measures test coverage. |
| Formatting | Black and Ruff | Consistent code style and linting. |

## 2.3 Proposed Folder Structure

```text
module_1_scraper/
  app/
    main.py
    config.py

    scheduler/
      jobs.py
      locks.py

    scrapers/
      base.py
      browser.py
      ec_scraper.py
      fc_scraper.py
      selectors.py

    services/
      mining_filter.py
      normalizer.py
      hashing.py
      persistence.py
      retry.py

    db/
      models.py
      session.py
      migrations/

    logging/
      run_logger.py
      error_logger.py

  tests/
    unit/
      test_mining_filter.py
      test_normalizer.py
      test_hashing.py
      test_persistence.py

    integration/
      test_ec_scraper_fixture.py
      test_fc_scraper_fixture.py
      test_scheduler_lock.py

    fixtures/
      ec_listing.html
      ec_detail.html
      fc_listing.html
      fc_detail.html
```

## 2.4 Runtime Configuration

Configuration must come from environment variables or a `.env` file. Secrets must never be committed.

```text
DATABASE_URL=sqlite:///mace_clearances.db
EC_PORTAL_URL=<to-be-confirmed>
FC_PORTAL_URL=<to-be-confirmed>
SCRAPE_HEADLESS=true
SCRAPE_TIMEOUT_MS=30000
MAX_PAGE_RETRIES=3
SCRAPE_CONCURRENCY=1
MISSED_RUN_STALE_THRESHOLD=3
SCREENSHOT_ON_FAILURE=true
HTML_SNAPSHOT_ON_FAILURE=true
```

## 2.5 Core Classes

### `ScrapeOrchestrator`

Coordinates the full scrape run.

Responsibilities:

- Create a scrape run record.
- Start EC and FC adapters.
- Send raw records to the mining filter.
- Normalize accepted records.
- Persist records.
- Track inserted, updated, unchanged, skipped, and failed counts.
- Finalize run status.

### `BaseScraper`

Defines the common scraper interface.

```python
class BaseScraper:
    clearance_type: str

    def scrape(self) -> list[dict]:
        ...

    def fetch_listing_pages(self) -> list[dict]:
        ...

    def fetch_detail(self, listing_record: dict) -> dict:
        ...
```

### `ECScraper`

Handles EC-specific behavior:

- EC listing URL.
- EC filters.
- EC table selectors.
- EC detail page selectors.
- EC field mapping.

### `FCScraper`

Handles FC-specific behavior:

- FC listing URL.
- FC filters.
- FC table selectors.
- FC detail page selectors.
- FC field mapping.

### `BrowserRenderer`

Responsible for browser automation.

```python
class BrowserRenderer:
    def open_page(self, url: str):
        ...

    def wait_for_selector(self, selector: str):
        ...

    def get_text(self, selector: str) -> str:
        ...

    def get_html(self) -> str:
        ...

    def screenshot_on_error(self, path: str):
        ...
```

### `MiningFilter`

Returns a structured decision.

```python
{
  "accepted": true,
  "reason": "sector field matched Mining",
  "matched_terms": ["Mining"]
}
```

### `Normalizer`

Converts raw source values into a stable canonical record.

Responsibilities:

- Trim whitespace.
- Normalize dates.
- Normalize status values.
- Normalize document URLs.
- Standardize empty values to `null`.
- Preserve original raw payload.

### `PersistenceService`

Handles database writes.

```python
def upsert_clearance_project(record: dict, scrape_run_id: int) -> str:
    ...
```

Return values:

- `inserted`
- `updated`
- `unchanged`
- `failed`

## 2.6 Normalized Record Shape

```json
{
  "clearance_type": "EC",
  "source_record_id": "source-specific-id",
  "proposal_number": "IA/XX/MIN/000000/2026",
  "project_name": "Mining Project Name",
  "project_proponent": "Company or Agency",
  "sector": "Mining",
  "sub_sector": "Coal / Non-coal / Mineral Type",
  "state": "State",
  "district": "District",
  "mineral": "Iron Ore",
  "mine_area": "100 ha",
  "capacity": "1.0 MTPA",
  "status": "Granted",
  "stage": "EC Granted",
  "clearance_date": "YYYY-MM-DD",
  "validity_date": "YYYY-MM-DD",
  "source_url": "https://source-detail-page",
  "document_urls": [
    "https://source-document-url"
  ],
  "raw_payload": {
    "source_label": "source value"
  }
}
```

## 2.7 Database Schema Draft

### `clearance_projects`

```sql
CREATE TABLE clearance_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clearance_type TEXT NOT NULL,
    source_record_id TEXT,
    proposal_number TEXT,
    project_name TEXT NOT NULL,
    project_proponent TEXT,
    sector TEXT,
    sub_sector TEXT,
    state TEXT,
    district TEXT,
    mineral TEXT,
    mine_area TEXT,
    capacity TEXT,
    status TEXT,
    stage TEXT,
    clearance_date DATE,
    validity_date DATE,
    source_url TEXT,
    document_urls TEXT,
    raw_payload TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    first_seen_at DATETIME NOT NULL,
    last_seen_at DATETIME NOT NULL,
    last_changed_at DATETIME,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    UNIQUE(clearance_type, source_record_id)
);
```

### `scrape_runs`

```sql
CREATE TABLE scrape_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_type TEXT NOT NULL,
    started_at DATETIME NOT NULL,
    finished_at DATETIME,
    status TEXT NOT NULL,
    records_found INTEGER DEFAULT 0,
    records_accepted INTEGER DEFAULT 0,
    records_inserted INTEGER DEFAULT 0,
    records_updated INTEGER DEFAULT 0,
    records_unchanged INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0
);
```

### `scrape_errors`

```sql
CREATE TABLE scrape_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scrape_run_id INTEGER NOT NULL,
    clearance_type TEXT,
    url TEXT,
    source_record_id TEXT,
    error_type TEXT,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    screenshot_path TEXT,
    html_snapshot_path TEXT,
    created_at DATETIME NOT NULL
);
```

### `clearance_change_history`

```sql
CREATE TABLE clearance_change_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    scrape_run_id INTEGER NOT NULL,
    old_payload TEXT NOT NULL,
    new_payload TEXT NOT NULL,
    old_hash TEXT NOT NULL,
    new_hash TEXT NOT NULL,
    changed_at DATETIME NOT NULL
);
```

### `source_documents`

```sql
CREATE TABLE source_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    document_type TEXT,
    document_url TEXT NOT NULL,
    file_name TEXT,
    discovered_at DATETIME NOT NULL,
    UNIQUE(project_id, document_url)
);
```

## 2.8 Upsert Algorithm

```mermaid
flowchart TD
    A["Normalized mining record"] --> B["Validate required fields"]
    B --> C{"Valid?"}
    C -- No --> D["Log validation error"]
    C -- Yes --> E["Build unique key"]
    E --> F["Find existing DB row"]
    F --> G{"Row exists?"}
    G -- No --> H["Insert new project"]
    G -- Yes --> I["Compute new content hash"]
    I --> J{"Hash changed?"}
    J -- No --> K["Update last_seen_at"]
    J -- Yes --> L["Insert change history"]
    L --> M["Update project row"]
```

Detailed steps:

1. Validate required fields.
2. Build unique key using `clearance_type + source_record_id`.
3. If `source_record_id` is missing, fall back to `clearance_type + proposal_number`.
4. Normalize all business fields.
5. Compute content hash.
6. Insert new record when no matching row exists.
7. Update only `last_seen_at` when the hash is unchanged.
8. Write change history and update the main row when the hash changes.
9. Log validation failures without stopping the whole run.

## 2.9 Content Hash Rules

Include fields that represent meaningful source changes:

- `project_name`
- `project_proponent`
- `sector`
- `sub_sector`
- `state`
- `district`
- `mineral`
- `mine_area`
- `capacity`
- `status`
- `stage`
- `clearance_date`
- `validity_date`
- sorted `document_urls`

Exclude operational fields:

- `first_seen_at`
- `last_seen_at`
- `last_changed_at`
- `scrape_run_id`
- retry count
- screenshot path
- temporary page metadata

## 2.10 Error Handling Strategy

| Error Type | Example | Handling |
|---|---|---|
| Navigation timeout | Page does not load in time. | Retry with exponential backoff. |
| Selector missing | Expected table selector is not found. | Capture screenshot and HTML snapshot. |
| Pagination failure | Next button not clickable. | Log page failure and continue if possible. |
| Detail extraction failure | Detail page layout changed. | Log record-level error and continue. |
| Validation failure | Missing project name or identifier. | Reject record and log reason. |
| Database failure | Insert or update fails. | Roll back transaction and mark run failed if needed. |
| Source unavailable | Portal is down. | Abort adapter and preserve run summary. |

## 2.11 Test Plan

### Unit Tests

| Test File | What It Verifies |
|---|---|
| `test_mining_filter.py` | Mining keyword detection, structured sector matching, rejection of non-mining sectors. |
| `test_normalizer.py` | Date parsing, whitespace cleanup, status normalization, URL normalization. |
| `test_hashing.py` | Stable hash generation and exclusion of operational fields. |
| `test_persistence.py` | Insert, update, unchanged, and change-history behavior. |

### Integration Tests

| Test File | What It Verifies |
|---|---|
| `test_ec_scraper_fixture.py` | EC listing and detail fixture extraction. |
| `test_fc_scraper_fixture.py` | FC listing and detail fixture extraction. |
| `test_scheduler_lock.py` | Prevents overlapping scheduled runs. |
| `test_database_flow.py` | End-to-end persistence using a temporary database. |

### Browser Smoke Test

The browser smoke test should:

1. Open a saved JS-rendered fixture page.
2. Wait for the listing table or record container.
3. Extract listing rows.
4. Open a detail fixture.
5. Extract raw fields.
6. Filter to mining-sector records.
7. Normalize the accepted record.
8. Persist it.
9. Verify the database row exists.

## 2.12 Dev Container Environment Check

If the repository uses a VS Code dev container, open the repository in VS Code and run:

```text
Dev Containers: Reopen in Container
```

After the container starts, verify:

```bash
python --version
pip --version
pytest --version
playwright --version
```

Install Playwright browsers if needed:

```bash
python -m playwright install
```

Run tests:

```bash
pytest
```

Run coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

Expected coverage target:

```text
80% or higher
```

## 2.13 Implementation Phases

```mermaid
flowchart LR
    A["Phase 1: Schema and config"] --> B["Phase 2: Unit tests"]
    B --> C["Phase 3: Browser renderer"]
    C --> D["Phase 4: EC adapter"]
    D --> E["Phase 5: FC adapter"]
    E --> F["Phase 6: Scheduler and locks"]
    F --> G["Phase 7: Error handling"]
    G --> H["Phase 8: Integration tests"]
    H --> I["Phase 9: Pilot run"]
```

### Phase Details

1. Create project structure, settings, database models, and migrations.
2. Write unit tests for filtering, normalization, hashing, and persistence.
3. Implement browser rendering and fixture-based extraction.
4. Implement EC source adapter.
5. Implement FC source adapter.
6. Add scheduler jobs and non-overlap locking.
7. Add retry handling, screenshots, and scrape error logging.
8. Run integration and browser smoke tests.
9. Pilot the scraper with conservative concurrency and inspect logs.

## 2.14 TDD Acceptance Criteria

The technical design is complete when:

- EC and FC adapters are separated.
- JavaScript-rendered pages can be loaded through Playwright.
- Listing and detail extraction are both supported.
- Mining-sector filtering has structured and keyword-based paths.
- Data normalization produces a stable canonical record.
- Database upsert behavior prevents duplicates.
- Changed records create change-history rows.
- Failed pages are logged and retried.
- Scheduled runs do not overlap.
- Unit and integration tests can reach at least 80 percent coverage.

---

# 3. Open Items Before Implementation

These items should be confirmed before coding:

- Exact EC portal URL.
- Exact FC portal URL.
- Final database choice: SQLite or PostgreSQL.
- Required production schedule.
- Whether source documents should only be linked or also downloaded.
- Deployment target: local machine, dev container, server, Docker, or cloud job.
- Naming convention for this module inside the shared repository.

---

# 4. Pull Request Notes

This README content is intentionally module-specific. It avoids repeating shared repository-level information such as overall project name, team members, or global setup instructions, because those sections may be handled by other team members in separate pull requests.

Suggested commit message:

```bash
docs: add module 1 SDD and TDD
```



# Development Must Dos
Switch to "development" branch when writing code, do not push/merge in "main" branch.





# Module 2: Data Processing and Compliance Structuring

Module 2 receives raw mining-project and environmental-compliance data from Module 1, approved files, internal Python objects, or shared database records. It validates, normalizes, classifies, and maps this information into structured compliance sections. The processed data is stored in PostgreSQL and made available to Module 3.

This README contains the complete Software Design Document and Technical Design Document for Module 2. It follows the project rule that Module 2 does not use external Application Programming Interfaces.

# Module 3: Generate PDF Reports and Display Them on the React Frontend

Module 3 takes the structured, validated compliance data produced by Module 2 and turns it into a finished PDF report that a user can read, download, and print directly inside the React frontend. Where Module 2 stops at "clean, structured sections stored in the database", Module 3 begins: it binds that data into a report template, renders a well formatted PDF on the server, stores the file, and streams it back to the browser for inline viewing.

This README contains the complete Software Design Document and Technical Design Document for Module 3. Module 3 is the report generation and presentation module, so unlike Module 2 it does expose a small backend service that the React frontend calls to request and retrieve reports.


---

# **SOFTWARE DESIGN DOCUMENT (SDD) STARTS HERE**


> **Module:** Data Extraction, Processing, Validation, and Compliance Document Structuring  
> **Project:** MACE — Mining Automated Compliance Execution  
> **Architecture Rule:** No external API-based communication  

> **Module:** Generate PDF Reports and Display Them on the React Frontend
> **Project:** MACE — Mining Automated Compliance Execution
> **Prepared By:** Kirtika (2023A7PS0219U)
> **Standard:** IEEE Std 1016 — Software Design Descriptions
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


The purpose of Module 2 is to convert raw and unorganized compliance data into a clean, validated, and structured format that can be used by later modules.

The module reduces:

- Repeated manual data entry
- Missing values
- Inconsistent units
- Duplicate records
- Incorrect field formats
- Difficulty in preparing compliance sections

The purpose of Module 3 is to give users a reliable, repeatable way to produce a formatted compliance report from data that already exists in the system, and to read that report without leaving the application.

The module reduces:

- Manual copying of data into word processors
- Inconsistent report formatting between users
- Time spent producing routine compliance documents
- Version confusion between the data and the printed report
- Dependence on desktop tools to view or print reports


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

| Environmental consultant | Reviews processed information |
| Compliance team | Checks completeness and correctness |
| Project coordinator | Tracks project status |
| Data-entry user | Corrects missing or invalid values |
| Module 1 | Supplies raw or extracted data |
| Module 3 | Uses structured output |
| Administrator | Maintains reference values |

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

| NFR-01 | Maintainability | Processing logic shall be divided into separate Python modules. |
| NFR-02 | Reliability | One invalid record shall not damage other valid records. |
| NFR-03 | Security | Database credentials shall remain outside source control. |
| NFR-04 | Testability | Validation and mapping functions shall support unit testing. |
| NFR-05 | Portability | The module shall run inside the project Dev Container. |
| NFR-06 | Consistency | Output shall follow one standard internal structure. |
| NFR-07 | Auditability | Source, status, and processing results shall be traceable. |
| NFR-08 | Performance | Normal project datasets shall process without unnecessary delay. |

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

    M1[Module 1] -->|Files / Shared Tables / Internal Objects| M2[Module 2]
    M2 -->|Errors and Missing Fields| M1
    M2 -->|Structured Database Records| M3[Module 3]
```

No HTTP requests or external API calls are required.

    SEC[Shared Security Module] -->|Validated token| M3[Module 3]
    M2[Module 2] -->|Structured compliance data| M3
    M3 -->|Report request and status| FE[React Frontend]
    M3 -->|PDF file| ST[(Object Storage)]
    ST -->|Signed URL| FE
```

Module 3 reads Module 2 data and does not modify it.


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

    F1[Input File] --> P[Module 2 Processing]
    D1[(Shared Raw Data Tables)] --> P
    M1[Module 1 Internal Output] --> P
    P --> D2[(Processed Project Data)]
    P --> D3[(Validation Results)]
    P --> D4[(Compliance Sections)]
    D4 --> M3[Module 3]

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

  "project_name": "Example Limestone Mining Project",
  "proponent_name": "Example Minerals Private Limited",
  "mineral_type": "Limestone",
  "lease_area": 25.4,
  "lease_area_unit": "hectare",
  "production_capacity": 1.0,
  "production_capacity_unit": "MTPA",
  "district": "Example District",
  "state": "Example State"

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

- Database credentials must be stored in environment variables.
- Only authorized users or modules may edit approved records.
- Sensitive client information must not be printed in logs.
- Input files must be validated before processing.
- Database changes should be traceable.
- Approved records must not be silently overwritten.

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


- Additional file formats
- Configurable validation rules
- Automated completeness scoring
- Versioned compliance templates
- Reviewer approval workflow
- Additional industries beyond mining
- Intelligent section suggestions

- Additional report types and templates
- Scheduled and automatic report generation
- Export to Word in addition to PDF
- Digital signing of generated reports
- Template preview before full generation
- Report comparison across periods
- Reviewer approval workflow inside the viewer


---

# **TECHNICAL DESIGN DOCUMENT (TDD) STARTS HERE**


> **Module:** Data Extraction, Processing, Validation, and Compliance Document Structuring  
> **Project:** MACE — Mining Automated Compliance Execution  
> **Architecture Rule:** No external API-based communication  

> **Module:** Generate PDF Reports and Display Them on the React Frontend
> **Project:** MACE — Mining Automated Compliance Execution
> **Prepared By:** Kirtika (2023A7PS0219U)
> **Technology Focus:** Node.js and Express backend, Puppeteer PDF generation, React frontend

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


- FastAPI routers
- HTTP endpoints
- REST APIs
- External service calls
- Direct PARIVESH integration
- User-interface code
- Final report generation
- Authentication implementation

- Creation of source business data
- Authentication implementation
- Browser side PDF editing
- Direct PARIVESH integration
- Long term archival policy


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


## 27. Future Technical Improvements

- Configurable validation-rule files
- Additional file readers
- Background processing
- Versioned project records
- Reviewer approval workflow
- Reference-data caching
- Processing metrics
- More sectors beyond mining

## 22. Future Technical Improvements

- A job queue with workers so generation survives a restart
- Server sent events or websockets to replace status polling
- Scheduled report generation
- Export to Word reusing the same template layer
- Digital signing of generated reports
- Template preview screen
- Generation metrics and dashboards