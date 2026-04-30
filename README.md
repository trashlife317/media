# U.S. Traumatic Brain Injury (TBI) Resource Directory Plan

## 1) Assumptions and Scope Confirmation

### Confirmed assumptions
- **Geography:** United States only (national, state, and local resources where verifiable).
- **Audience:** TBI survivors and caregivers (including family caregivers, guardians, and care coordinators).
- **Resource domains in scope:**
  - Medical care (neurology, trauma centers, TBI clinics)
  - Rehabilitation (inpatient/outpatient rehab, cognitive rehab, therapy)
  - Support services (peer groups, caregiver support)
  - Advocacy and education
  - Benefits navigation (federal/state public benefits)
  - Legal aid and rights support
  - Assistive technology/equipment access
  - Crisis lines and urgent support pathways
- **Quality bar:** Only resources with **confirmed existence and current status** are listed as “verified.”

### Recommended refinements
- Add a **verification confidence tier** (A/B/C) to distinguish direct-primary verification (A) from secondary confirmation (B/C).
- Keep “not currently verifiable” resources in a **separate quarantine table** (not shown to end users until re-verified).
- Use a **service area normalization standard** (ISO country + state abbreviations + county/city where applicable).

---

## 2) Directory Reliability Framework

Each entry must pass all four dimensions:

1. **Source Credibility**
   - Organization type documented: government, accredited healthcare provider, registered nonprofit, or professional association.
   - Credential checks as applicable:
     - Hospitals/rehab centers: accreditation/licensure confirmation.
     - Nonprofits: IRS nonprofit status / known national reputation.
     - Government services: .gov or official state/municipal domain.

2. **Currentness**
   - `last_verified` date captured in ISO format (`YYYY-MM-DD`).
   - `verification_source` includes exact URL and verification method.
   - `next_review_due` assigned by cadence:
     - High-risk data (hotlines, addresses, admissions): 30–60 days.
     - Medium-risk data (eligibility/service descriptions): 90 days.
     - Stable policy pages/associations: 180 days.

3. **Accessibility**
   - Language availability captured (English, Spanish, ASL services, interpreter options, etc.).
   - Disability access captured (TTY/relay, wheelchair access info, accessible intake formats).
   - Digital accessibility indicators captured (WCAG statement, accessible forms, alternative contact methods).

4. **Eligibility Clarity**
   - Who is served (adult/pediatric, survivor/caregiver/veteran/low-income, etc.).
   - Geographic scope (national/state/local/catchment).
   - Requirements (insurance, referral, diagnosis documentation, residency).

---

## 3) Canonical Data Schema

### Core fields (required unless noted)
- `id` (string, unique)
- `name` (string)
- `type` (enum: government | medical_center | rehab_provider | nonprofit | professional_association | legal_aid | crisis_line | equipment_provider | support_group | benefits_program)
- `category` (array of controlled terms)
- `services` (array of strings)
- `location` (object)
  - `country` (default: US)
  - `state` (2-letter when applicable)
  - `city` (optional)
  - `address` (optional)
  - `service_area` (national/state/local + details)
- `contact` (object)
  - `phone` (array)
  - `tty` (optional)
  - `email` (optional)
  - `hours` (optional)
- `website` (URL)
- `eligibility` (object)
  - `population_served`
  - `age_range`
  - `requirements`
  - `insurance_or_cost`
- `accessibility` (object)
  - `languages` (array)
  - `interpreter_available` (boolean/unknown)
  - `wheelchair_access_info` (string/unknown)
  - `digital_access_notes` (string)
- `last_verified` (date)
- `verification_source` (array of objects: `url`, `source_type`, `method`, `verified_on`)
- `verification_status` (enum: verified | needs_review | unverifiable)
- `next_review_due` (date)
- `notes` (string)

### Optional governance fields
- `created_at`, `updated_at`
- `verified_by` (reviewer ID)
- `confidence_tier` (A/B/C)
- `duplicates_of` (array of IDs)

---

## 4) Source Prioritization and Verification Rules

### Priority source hierarchy
1. **Official U.S. government and state agencies** (CDC, NIH/NINDS, HRSA, SAMHSA, SSA, VA, state health departments).
2. **Accredited medical and rehabilitation providers** (CARF-accredited rehab, major academic centers, trauma centers).
3. **Recognized nonprofits and advocacy organizations** (e.g., Brain Injury Association network).
4. **Professional associations** (AAN, ACRM, etc.).

### Verification method per entry
- Minimum two checks where possible:
  - Primary source check (official website record).
  - Secondary corroboration (accreditation listing, association directory, or direct call/email).
- Confirm and record:
  - Service still active.
  - Contact path operational.
  - Eligibility and service area accurate.
- For time-sensitive resources (crisis lines), perform **live contact validation** when feasible and timestamp it.

---

## 5) Research, Verification, and De-duplication Workflow

1. **Seed list generation**
   - Gather candidates by category from priority sources.
2. **Normalize records**
   - Standardize names, addresses, phones, URLs, and taxonomy tags.
3. **First-pass validation**
   - Remove obvious out-of-scope or inactive entries.
4. **Primary verification**
   - Verify from official source pages; capture screenshot or archival note.
5. **Secondary verification**
   - Cross-check with accreditation databases/directories or direct outreach.
6. **Eligibility and accessibility extraction**
   - Populate structured fields; mark unknown explicitly.
7. **De-duplication**
   - Match on normalized name + domain + phone + address fingerprints.
   - Merge records; preserve source provenance.
8. **Quality review gate**
   - Reject entries missing required fields or stale verification date.
9. **Publish export set**
   - JSON/YAML/CSV and human-readable directory.
10. **Maintenance cycle**
   - Auto-queue entries by `next_review_due` and high-change risk.

---

## 6) MVP Delivery Plan (100+ Verified Resources)

### Phase 0 (Week 1): Setup
- Finalize taxonomy, schema, QA checklist, and reviewer SOP.
- Build ingestion templates and validation scripts.

### Phase 1 (Weeks 2–4): Initial directory build
- Target: **100–150 verified entries** covering all required categories.
- Include national baseline plus at least 15–20 states with one or more local resources.

### Phase 2 (Weeks 5–6): Search/filter and accessibility MVP
- Launch user-facing directory with:
  - Keyword search
  - Filters: category, state, population served, language, virtual/in-person, cost/insurance
  - Sort by recently verified
- Accessibility baseline:
  - WCAG 2.2 AA-aligned color contrast
  - Keyboard-only navigation
  - Screen-reader-friendly semantic structure and labels

### Phase 3 (Ongoing monthly): Verification operations
- Reverification backlog management.
- Dead-link monitoring and hotline fast-lane checks.
- Monthly quality report and gap analysis (state/category coverage).

### Suggested team roles
- **Research Lead:** source discovery and taxonomy governance.
- **Verification Specialists (2+):** evidence checks and outreach.
- **Data QA Analyst:** schema validation and de-duplication audits.
- **Accessibility/UX Lead:** end-user access compliance.
- **Project Owner:** KPI tracking and stakeholder reporting.

### Success metrics
- ≥100 verified resources in MVP.
- ≥95% entries with complete required fields.
- ≥90% entries reverified within defined cadence.
- <2% broken links at monthly scan.
- Accessibility conformance score (internal checklist) ≥95%.
- Median search-to-resource click time <60 seconds in usability testing.

---

## 7) End-User Accessibility Requirements

- **Screen reader support**
  - Proper heading hierarchy, landmarks, descriptive link text, ARIA only when necessary.
  - Announce filter changes and result counts.
- **High contrast and low vision**
  - Meet/exceed WCAG contrast thresholds.
  - Visible focus states and scalable text at 200%.
- **Navigation and input**
  - Full keyboard operability.
  - Predictable filter controls with clear reset.
- **Content clarity**
  - Plain-language summaries.
  - Crisis resources pinned and visually prioritized.
- **Accessible alternatives**
  - Export to accessible CSV and printer-friendly format.
  - Multiple contact modalities (phone/web/email where available).

---

## 8) Human-Readable Directory Outline

Recommended sections:
1. Immediate Help & Crisis
2. Medical Diagnosis & Specialty Care
3. Rehabilitation (Inpatient/Outpatient/Home/Telehealth)
4. Caregiver & Peer Support
5. Benefits and Financial Assistance
6. Legal Rights and Advocacy
7. Assistive Technology and Equipment
8. State-by-State Resource Hubs
9. How to Verify/Report Changes

For each listing card:
- Name
- Category/Type
- Services summary
- Who it serves
- Location/service area
- Contact and website
- Languages/accessibility indicators
- “Last verified” + source badge

---

## 9) Sample Records (Illustrative Structure)

### YAML
```yaml
- id: us-nih-ninds-tbi
  name: National Institute of Neurological Disorders and Stroke (NINDS) - Traumatic Brain Injury Information Page
  type: government
  category: [advocacy, education, medical_care]
  services:
    - Evidence-based TBI information
    - Research updates
    - Links to clinical resources
  location:
    country: US
    service_area: national
  contact:
    phone: []
    hours: "Web resource"
  website: https://www.ninds.nih.gov/health-information/disorders/traumatic-brain-injury-tbi
  eligibility:
    population_served: "General public, survivors, caregivers, clinicians"
    age_range: "All ages"
    requirements: "None"
    insurance_or_cost: "Free"
  accessibility:
    languages: [English]
    interpreter_available: unknown
    wheelchair_access_info: unknown
    digital_access_notes: "Federal website accessibility standards apply"
  last_verified: 2026-04-30
  verification_source:
    - url: https://www.ninds.nih.gov/health-information/disorders/traumatic-brain-injury-tbi
      source_type: official_website
      method: webpage_review
      verified_on: 2026-04-30
  verification_status: verified
  next_review_due: 2026-10-30
  notes: "National educational resource; not a direct care provider"

- id: us-samhsa-988
  name: 988 Suicide & Crisis Lifeline
  type: crisis_line
  category: [crisis, caregiver_support]
  services:
    - 24/7 crisis counseling
    - Phone, text, and chat support
    - Referral to local emergency and behavioral health resources
  location:
    country: US
    service_area: national
  contact:
    phone: ["988"]
    hours: "24/7"
  website: https://988lifeline.org
  eligibility:
    population_served: "People in emotional distress, including survivors/caregivers"
    age_range: "All ages"
    requirements: "None"
    insurance_or_cost: "Free"
  accessibility:
    languages: [English, Spanish]
    interpreter_available: true
    wheelchair_access_info: n/a
    digital_access_notes: "Phone/text/chat channels"
  last_verified: 2026-04-30
  verification_source:
    - url: https://988lifeline.org
      source_type: official_website
      method: webpage_review
      verified_on: 2026-04-30
  verification_status: verified
  next_review_due: 2026-05-30
  notes: "Include immediate escalation protocol for active emergencies"
```

### JSON
```json
[
  {
    "id": "us-cdc-tbi",
    "name": "CDC Traumatic Brain Injury",
    "type": "government",
    "category": ["education", "prevention", "advocacy"],
    "services": ["TBI education", "data/statistics", "prevention guidance"],
    "location": {"country": "US", "service_area": "national"},
    "contact": {"phone": [], "hours": "Web resource"},
    "website": "https://www.cdc.gov/traumatic-brain-injury/",
    "eligibility": {
      "population_served": "Public, survivors, caregivers, professionals",
      "age_range": "All ages",
      "requirements": "None",
      "insurance_or_cost": "Free"
    },
    "accessibility": {
      "languages": ["English", "Spanish (selected content)"],
      "interpreter_available": "unknown",
      "wheelchair_access_info": "n/a",
      "digital_access_notes": "Accessible federal web content"
    },
    "last_verified": "2026-04-30",
    "verification_source": [
      {
        "url": "https://www.cdc.gov/traumatic-brain-injury/",
        "source_type": "official_website",
        "method": "webpage_review",
        "verified_on": "2026-04-30"
      }
    ],
    "verification_status": "verified",
    "next_review_due": "2026-10-30",
    "notes": "Information and prevention hub"
  }
]
```

### CSV (header + one row)
```csv
id,name,type,category,services,location_country,location_state,location_city,service_area,phone,website,population_served,age_range,requirements,insurance_or_cost,languages,last_verified,verification_status,next_review_due,verification_source_url,notes
us-bia-usa,Brain Injury Association of America,nonprofit,"advocacy|support_group|caregiver_support","Information and referral|education|state affiliate navigation",US,,,national,"1-800-444-6443",https://www.biausa.org,"Survivors,caregivers,families",All ages,None,Free,"English",2026-04-30,verified,2026-07-30,https://www.biausa.org,"National nonprofit with state affiliate network"
```

---

## 10) Ongoing Maintenance SOP (Actionable)

- Run automated weekly checks:
  - HTTP status and TLS validity
  - Redirect changes
  - Phone formatting/field integrity
- Run monthly human verification queue:
  - All crisis lines
  - Recently changed websites
  - Entries older than cadence threshold
- Quarterly audit:
  - Duplicate detection rerun
  - Taxonomy cleanup
  - Accessibility metadata completeness
- Change logging:
  - Keep revision history per entry (`what changed`, `who`, `when`, `why`).
- Community feedback intake:
  - “Report outdated info” button creating moderation tickets.

This framework yields a reliable, scalable, and user-centered TBI resource directory with clear verification provenance and sustainable maintenance operations.
