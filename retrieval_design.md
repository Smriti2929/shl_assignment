# Retrieval Design

## Goal

Convert every SHL assessment into a searchable document for semantic retrieval.

---

## Assessment Document Structure

Each assessment will become a single text document.

Example:

Name: .NET Framework 4.5

Description:
The .NET Framework 4.5 test measures knowledge of .NET environment.

Job Levels:
Professional Individual Contributor
Mid-Professional

Categories:
Knowledge & Skills

Languages:
English (USA)

Duration:
30 minutes

---

## Fields Used For Retrieval

- name
- description
- job_levels
- keys
- languages
- duration

---

## Fields Used For Response

- name
- link
- duration
- languages
- keys

---

## Fields Ignored

- entity_id
- scraped_at
- status
- remote
- adaptive
- *_raw fields

---

## Retrieval Pipeline

Catalog JSON
↓
Document Builder
↓
Embeddings
↓
FAISS Index
↓
Top-K Retrieval
↓
LLM Recommendation