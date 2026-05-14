# Laboratory & Diagnostics

Manage laboratory test requests, specimen collection, result entry, and report publication in the Care platform.

## Overview

Streamline laboratory operations from test ordering through result reporting. This section covers the complete laboratory workflow.

---

## Available Guides

<div class="grid cards" markdown>

-   **Raise Lab Test Request**

    Create and submit laboratory test requests for patients.

    [:octicons-arrow-right-24: Read More](raise-lab-test-request.md)

-   **Service Request Review & Results**

    Review requests, collect specimens, enter results, and publish reports.

    [:octicons-arrow-right-24: Read More](service-request-review-specimen-result.md)

</div>

---

## Laboratory Workflow

```mermaid
graph LR
    A[Raise Test Request] --> B[Review Request]
    B --> C[Collect Specimen]
    C --> D[Process Test]
    D --> E[Enter Results]
    E --> F[Publish Report]
```

---

## Quick Stats

- **Total Guides**: 2
- **Workflow Stages**: 6 (Request → Review → Collect → Process → Result → Publish)
- **User Roles**: Clinicians, Lab Technicians, Pathologists

---

!!! info "Integration Note"
    Laboratory results are automatically integrated with patient clinical records for seamless access by care team members.
