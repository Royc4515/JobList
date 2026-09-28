# JobList — Job Search Tracker

My job-application pipeline. Each role lives in [`applications/`](applications/) as its own Markdown file (structured header + notes). To add one, copy [`templates/application.md`](templates/application.md), fill it in, then run:

```bash
python scripts/build_dashboard.py
```

The dashboard below is auto-generated — edit application files, not this block.

<!-- DASHBOARD:START -->

**49 applications** — **4** In review · **23** Submitted · **16** Not submitted · **6** Rejected

## Next to submit

Not-submitted roles ranked by fit score out of 40 (rubric in [`PROFILE.md`](PROFILE.md)).

1. **26** [FIL Robotics (Fives) — Junior Software Engineer - Student Position (Ref 6148)](applications/fil-robotics-junior-software-engineer-student.md) · role 8 · stack 6 · gates 7 · path 5 — Backend, asks exactly 3rd year and names Bar-Ilan; JVM-leaning stack, Binyamina offset by hybrid
2. **26** [ChargeAfter — Integration Engineer Intern - Operations Group](applications/chargeafter-integration-engineer-intern.md) · role 7 · stack 8 · gates 6 · path 5 — Python automation + AI dev tools valued explicitly; studies gate borderline (>=1 year), GPA>84 to verify
3. **25** [SAP — Software Eng. Intern (Gateway)](applications/sap-software-eng-intern-gateway.md) · role 8 · stack 4 · gates 6 · path 7 — Backend direction, but Java/Spring/AWS are gaps; Oriyah is an insider not yet asked
4. **23** [CrowdStrike — Engineering Intern](applications/crowdstrike-engineering-intern.md) · role 6 · stack 5 · gates 9 · path 3 — Generic SWE intern, cloud gap; no JD link and cold big-brand ATS
5. **21** [SAP — Software Engineering Intern - Unified Gateway](applications/sap-software-engineering-intern-unified-gateway.md) · role 6 · stack 3 · gates 7 · path 5 — Infra-heavy (Go/K8s); duplicate of Student Developer UG - apply to one at most
6. **20** [SAP — Student Developer - Unified Gateway](applications/sap-student-developer-unified-gateway.md) · role 6 · stack 3 · gates 6 · path 5 — Infra-heavy (Go/K8s); duplicate of Engineering Intern UG - apply to one at most
7. **20** [Mobileye — ML Software & Infrastructure Engineer (Student) - Hawkeye](applications/mobileye-ml-software-infrastructure-student.md) · role 7 · stack 5 · gates 5 · path 3 — Posting appears CLOSED since 2026-08-09; location/gates unknown - verify it is live first
8. **18** [SAP — Student DevOps](applications/sap-student-devops.md) · role 3 · stack 2 · gates 6 · path 7 — DevOps is a stated gap and off-direction; only the Noam contact lifts it
9. **17** [Cellebrite — Associate Software Engineer](applications/cellebrite-associate-software-engineer.md) · role 4 · stack 6 · gates 2 · path 5 — Offensive-security domain; full-time on-site and requires a finished BSc
10. **17** [Keysight — Full Stack Dev Student](applications/keysight-full-stack-dev-student.md) · role 5 · stack 2 · gates 7 · path 3 — Hard C#/.NET requirement Roy does not have
11. **15** [Microsoft — Security Research Intern](applications/microsoft-security-research-intern.md) · role 2 · stack 1 · gates 9 · path 3 — Vulnerability research with no project in the field; cold big-brand

**Gated out (5)** - a hard gate failed; close or drop:
- [Ceva — Architecture Software Tools Developer Student](applications/ceva-architecture-software-tools-developer-student.md) · role 8 · stack 6 · gates 0 · path 4 — GATED: requires 3+ semesters remaining, Roy has about 2
- [Elbit Systems — Software Quality Student - Haifa (Req 7130)](applications/elbit-software-quality-student-haifa.md) · role 0 · stack 3 · gates 0 · path 3 — GATED: 2 years remaining required, and QA is a Skip category
- [Intel — ML Engineer Student](applications/intel-ml-engineer-student.md) · role 7 · stack 5 · gates 0 · path 3 — GATED: requires 2+ years remaining
- [Motorola Solutions — Student - Software Engineer (R66325)](applications/motorola-solutions-student-software-engineer.md) · role 5 · stack 3 · gates 0 · path 5 — GATED: requires currently being in 2nd year
- [Personetics — AI & Automation Specialist Student](applications/personetics-ai-automation-specialist-student.md) · role 7 · stack 6 · gates 0 · path 4 — GATED: requires 1.5-2 years until graduation

## Pipeline

### 🔎 In review (4)
- [Siemens Industry Software Ltd. — AI Research Student (Job ID 512848)](applications/siemens-ai-research-student-512848.md)
- [Siemens Industry Software Ltd. — Application Engineering Student (Job ID 512845)](applications/siemens-application-engineering-student-512845.md)
- [Siemens Industry Software Ltd. — Software Engineering Student](applications/siemens-software-engineering-student.md)
- [Texas Instruments — WiFi Software Development Intern (25007138)](applications/ti-wifi-software-development-intern.md)

### 📤 Submitted (23)
- [AI6Labs (Wearable Devices) — AI Engineer Student](applications/ai6labs-ai-engineer-student.md)
- [Apple — SW Engineering Student (Herzliya)](applications/apple-sw-engineering-student-herzliya.md)
- [Apple — SW Engineering Student](applications/apple-sw-engineering-student-jerusalem.md)
- [Check Point — Software Developer - Student Position (AI POCs team)](applications/checkpoint-software-developer-student-ai-pocs.md)
- [Dell Technologies — Software Engineer Student - Glil Yam (ID: 292526)](applications/dell-software-engineer-student-glil-yam.md)
- [Elbit Systems — Software Developer Student - Netanya (Req 6355)](applications/elbit-software-developer-student-netanya.md)
- [Elbit Systems — Software Engineering Student - Modi'in (Req 6608)](applications/elbit-software-engineering-student-modiin-6608.md)
- [Elbit Systems — Software Engineering Student - Modi'in (Req 6610)](applications/elbit-software-engineering-student-modiin.md)
- [Fullpath — Junior Backend Engineer](applications/fullpath-junior-backend-engineer.md)
- [IAI (Israel Aerospace Industries) — Software Development Student](applications/iai-software-development-student-ashdod.md)
- [Intel — AI Product Analyst Student - AI Solutions Group (JR0284923)](applications/intel-ai-product-analyst-student.md)
- [Mobileye — Algorithm Developer Student](applications/mobileye-algorithm-developer-student.md)
- [Mobileye — Operating System Architecture Student](applications/mobileye-os-architecture-student-haifa.md)
- [Mobileye — Python Developer - Student Position (Road algorithm team)](applications/mobileye-python-developer-student-jerusalem.md)
- [Mobileye — Software CI and Automation Student (EPG CI team)](applications/mobileye-software-ci-automation-student.md)
- [Mobileye — Software Engineer Student Position](applications/mobileye-software-engineer-student.md)
- [NiCE — DevOps Student (Associate DevOps Engineer, CSA team)](applications/nice-devops-student.md)
- [Qualcomm — Intern FY27 - AI Driven Test Automation Engineer (3092068)](applications/qualcomm-intern-fy27-ai-test-automation.md)
- [SAP — Cloud Platform Engineer - Student (Java, UCP team) (Req 459254)](applications/sap-cloud-platform-engineer-student-java.md)
- [SentinelOne — macOS Software Engineering Intern](applications/sentinelone-macos-software-engineering-intern.md)
- [SentinelOne — Software Engineer Intern (Backend)](applications/sentinelone-software-engineer-intern.md)
- [Waterfall Security Solutions — Full Stack Developer (Student)](applications/waterfall-security-full-stack-developer.md)
- [מערך הדיגיטל הלאומי — סטודנט/ית מפתח/ת Design System](applications/national-digital-agency-design-system-student.md)

### 📝 Not submitted (16)
- [Cellebrite — Associate Software Engineer](applications/cellebrite-associate-software-engineer.md)
- [Ceva — Architecture Software Tools Developer Student](applications/ceva-architecture-software-tools-developer-student.md)
- [ChargeAfter — Integration Engineer Intern - Operations Group](applications/chargeafter-integration-engineer-intern.md)
- [CrowdStrike — Engineering Intern](applications/crowdstrike-engineering-intern.md)
- [Elbit Systems — Software Quality Student - Haifa (Req 7130)](applications/elbit-software-quality-student-haifa.md)
- [FIL Robotics (Fives) — Junior Software Engineer - Student Position (Ref 6148)](applications/fil-robotics-junior-software-engineer-student.md)
- [Intel — ML Engineer Student](applications/intel-ml-engineer-student.md)
- [Keysight — Full Stack Dev Student](applications/keysight-full-stack-dev-student.md)
- [Microsoft — Security Research Intern](applications/microsoft-security-research-intern.md)
- [Mobileye — ML Software & Infrastructure Engineer (Student) - Hawkeye](applications/mobileye-ml-software-infrastructure-student.md)
- [Motorola Solutions — Student - Software Engineer (R66325)](applications/motorola-solutions-student-software-engineer.md)
- [Personetics — AI & Automation Specialist Student](applications/personetics-ai-automation-specialist-student.md)
- [SAP — Software Eng. Intern (Gateway)](applications/sap-software-eng-intern-gateway.md)
- [SAP — Software Engineering Intern - Unified Gateway](applications/sap-software-engineering-intern-unified-gateway.md)
- [SAP — Student Developer - Unified Gateway](applications/sap-student-developer-unified-gateway.md)
- [SAP — Student DevOps](applications/sap-student-devops.md)

### ❌ Rejected (6)
- [Amazon — 2026 Software Dev Engineer Intern - Haifa, Israel (3147202)](applications/amazon-software-dev-engineer-intern-haifa.md)
- [Astera Labs — (ראה מייל לפרטי המשרה)](applications/astera-labs-see-email.md)
- [Chef.i — Full-Stack Developer (Student/Junior)](applications/chefi-full-stack-developer.md)
- [Intel — Wi-Fi Driver Software Developer Student (JR0284349)](applications/intel-wifi-driver-software-developer-student.md)
- [Red Hat — Software Engineering Intern - Ecosystem Engineering (Special Projects) R-055020](applications/redhat-software-engineering-intern-ecosystem.md)
- [Wix — (ראה מייל לפרטי המשרה)](applications/wix-see-email.md)

## All applications

| Company | Role | Status | Fit | Applied | Follow-up |
| --- | --- | --- | --- | --- | --- |
| [Cellebrite](applications/cellebrite-associate-software-engineer.md) | Associate Software Engineer | 📝 Not submitted | 17 | — | — |
| [Ceva](applications/ceva-architecture-software-tools-developer-student.md) | Architecture Software Tools Developer Student | 📝 Not submitted | gated | — | — |
| [ChargeAfter](applications/chargeafter-integration-engineer-intern.md) | Integration Engineer Intern - Operations Group | 📝 Not submitted | 26 | — | — |
| [CrowdStrike](applications/crowdstrike-engineering-intern.md) | Engineering Intern | 📝 Not submitted | 23 | — | — |
| [Elbit Systems](applications/elbit-software-quality-student-haifa.md) | Software Quality Student - Haifa (Req 7130) | 📝 Not submitted | gated | — | — |
| [FIL Robotics (Fives)](applications/fil-robotics-junior-software-engineer-student.md) | Junior Software Engineer - Student Position (Ref 6148) | 📝 Not submitted | 26 | — | — |
| [Intel](applications/intel-ml-engineer-student.md) | ML Engineer Student | 📝 Not submitted | gated | — | — |
| [Keysight](applications/keysight-full-stack-dev-student.md) | Full Stack Dev Student | 📝 Not submitted | 17 | — | — |
| [Microsoft](applications/microsoft-security-research-intern.md) | Security Research Intern | 📝 Not submitted | 15 | — | — |
| [Mobileye](applications/mobileye-ml-software-infrastructure-student.md) | ML Software & Infrastructure Engineer (Student) - Hawkeye | 📝 Not submitted | 20 | — | — |
| [Motorola Solutions](applications/motorola-solutions-student-software-engineer.md) | Student - Software Engineer (R66325) | 📝 Not submitted | gated | — | — |
| [Personetics](applications/personetics-ai-automation-specialist-student.md) | AI & Automation Specialist Student | 📝 Not submitted | gated | — | — |
| [SAP](applications/sap-software-eng-intern-gateway.md) | Software Eng. Intern (Gateway) | 📝 Not submitted | 25 | — | — |
| [SAP](applications/sap-software-engineering-intern-unified-gateway.md) | Software Engineering Intern - Unified Gateway | 📝 Not submitted | 21 | — | TBD |
| [SAP](applications/sap-student-developer-unified-gateway.md) | Student Developer - Unified Gateway | 📝 Not submitted | 20 | — | TBD |
| [SAP](applications/sap-student-devops.md) | Student DevOps | 📝 Not submitted | 18 | — | — |
| [Siemens Industry Software Ltd.](applications/siemens-ai-research-student-512848.md) | AI Research Student (Job ID 512848) | 🔎 In review | — | — | — |
| [Siemens Industry Software Ltd.](applications/siemens-application-engineering-student-512845.md) | Application Engineering Student (Job ID 512845) | 🔎 In review | — | — | — |
| [Waterfall Security Solutions](applications/waterfall-security-full-stack-developer.md) | Full Stack Developer (Student) | 📤 Submitted | — | — | — |
| [IAI (Israel Aerospace Industries)](applications/iai-software-development-student-ashdod.md) | Software Development Student | 📤 Submitted | — | 2026-09-14 | — |
| [SAP](applications/sap-cloud-platform-engineer-student-java.md) | Cloud Platform Engineer - Student (Java, UCP team) (Req 459254) | 📤 Submitted | — | 2026-08-25 | — |
| [Check Point](applications/checkpoint-software-developer-student-ai-pocs.md) | Software Developer - Student Position (AI POCs team) | 📤 Submitted | — | 2026-08-24 | — |
| [Elbit Systems](applications/elbit-software-engineering-student-modiin-6608.md) | Software Engineering Student - Modi'in (Req 6608) | 📤 Submitted | — | 2026-08-24 | — |
| [NiCE](applications/nice-devops-student.md) | DevOps Student (Associate DevOps Engineer, CSA team) | 📤 Submitted | — | 2026-08-24 | 2026-09-07 |
| [Mobileye](applications/mobileye-software-ci-automation-student.md) | Software CI and Automation Student (EPG CI team) | 📤 Submitted | — | 2026-08-16 | — |
| [Intel](applications/intel-ai-product-analyst-student.md) | AI Product Analyst Student - AI Solutions Group (JR0284923) | 📤 Submitted | — | 2026-08-10 | — |
| [SentinelOne](applications/sentinelone-macos-software-engineering-intern.md) | macOS Software Engineering Intern | 📤 Submitted | — | 2026-08-10 | — |
| [SentinelOne](applications/sentinelone-software-engineer-intern.md) | Software Engineer Intern (Backend) | 📤 Submitted | — | 2026-08-10 | — |
| [Elbit Systems](applications/elbit-software-engineering-student-modiin.md) | Software Engineering Student - Modi'in (Req 6610) | 📤 Submitted | — | 2026-08-09 | — |
| [Mobileye](applications/mobileye-algorithm-developer-student.md) | Algorithm Developer Student | 📤 Submitted | — | 2026-08-09 | — |
| [Mobileye](applications/mobileye-os-architecture-student-haifa.md) | Operating System Architecture Student | 📤 Submitted | — | 2026-08-09 | — |
| [Mobileye](applications/mobileye-python-developer-student-jerusalem.md) | Python Developer - Student Position (Road algorithm team) | 📤 Submitted | — | 2026-08-09 | — |
| [Mobileye](applications/mobileye-software-engineer-student.md) | Software Engineer Student Position | 📤 Submitted | — | 2026-08-05 | — |
| [Apple](applications/apple-sw-engineering-student-herzliya.md) | SW Engineering Student (Herzliya) | 📤 Submitted | — | 2026-07-31 | 2026-08-14 |
| [Apple](applications/apple-sw-engineering-student-jerusalem.md) | SW Engineering Student | 📤 Submitted | — | 2026-07-31 | 2026-08-14 |
| [Amazon](applications/amazon-software-dev-engineer-intern-haifa.md) | 2026 Software Dev Engineer Intern - Haifa, Israel (3147202) | ❌ Rejected | — | 2026-07-23 | — |
| [Texas Instruments](applications/ti-wifi-software-development-intern.md) | WiFi Software Development Intern (25007138) | 🔎 In review | — | 2026-07-23 | — |
| [Fullpath](applications/fullpath-junior-backend-engineer.md) | Junior Backend Engineer | 📤 Submitted | — | 2026-07-21 | — |
| [Qualcomm](applications/qualcomm-intern-fy27-ai-test-automation.md) | Intern FY27 - AI Driven Test Automation Engineer (3092068) | 📤 Submitted | — | 2026-06-29 | — |
| [מערך הדיגיטל הלאומי](applications/national-digital-agency-design-system-student.md) | סטודנט/ית מפתח/ת Design System | 📤 Submitted | — | 2026-06-24 | — |
| [Siemens Industry Software Ltd.](applications/siemens-software-engineering-student.md) | Software Engineering Student | 🔎 In review | — | 2026-06-23 | — |
| [AI6Labs (Wearable Devices)](applications/ai6labs-ai-engineer-student.md) | AI Engineer Student | 📤 Submitted | — | 2026-06-21 | — |
| [Chef.i](applications/chefi-full-stack-developer.md) | Full-Stack Developer (Student/Junior) | ❌ Rejected | — | 2026-06-21 | — |
| [Astera Labs](applications/astera-labs-see-email.md) | (ראה מייל לפרטי המשרה) | ❌ Rejected | — | 2026-06-16 | — |
| [Elbit Systems](applications/elbit-software-developer-student-netanya.md) | Software Developer Student - Netanya (Req 6355) | 📤 Submitted | — | 2026-06-02 | — |
| [Intel](applications/intel-wifi-driver-software-developer-student.md) | Wi-Fi Driver Software Developer Student (JR0284349) | ❌ Rejected | — | 2026-06-02 | — |
| [Dell Technologies](applications/dell-software-engineer-student-glil-yam.md) | Software Engineer Student - Glil Yam (ID: 292526) | 📤 Submitted | — | 2026-05-20 | — |
| [Red Hat](applications/redhat-software-engineering-intern-ecosystem.md) | Software Engineering Intern - Ecosystem Engineering (Special Projects) R-055020 | ❌ Rejected | — | 2026-05-18 | 2026-05-18 |
| [Wix](applications/wix-see-email.md) | (ראה מייל לפרטי המשרה) | ❌ Rejected | — | 2026-05-11 | — |

## Networking leads

**8 leads** — **1** Referred · **3** Contacted · **4** To contact

| Company | Contact | Connection | Target role | Status | Follow-up |
| --- | --- | --- | --- | --- | --- |
| [Apple](leads/apple-dolev-orgad-referral.md) | Dolev Orgad | inside | SW Engineering Student (Jerusalem / Herzliya) | ✅ Referred | 2026-07-28 |
| [Cellebrite](leads/cellebrite-afik-referral.md) | Afik | knows-someone | Associate Software Engineer | 📨 Contacted | — |
| [Mobileye](leads/mobileye-afik-referral.md) | Afik | knows-someone | Python Developer - Student Position (Jerusalem) | 📨 Contacted | — |
| [Motorola Solutions](leads/motorola-afik-referral.md) | Afik | knows-someone | Student - Software Engineer (R66325) | 📨 Contacted | — |
| [NiCE / Altera](leads/altera-ex-nice-family-friend.md) | — | inside | Student Developer - via NiCE referral and Kravi Tech mentorship | 🔵 To contact | 2026-09-29 |
| [Hemispheric](leads/hemispheric-cold-outreach.md) | Hagai Lalazar (co-founder, computational neuroscientist) / Gidi Littwin (co-founder) | cold | Student / intern - NeuroAI (no specific req open) | 🔵 To contact | 2026-08-23 |
| [SAP](leads/sap-noam-community.md) | Noam | inside | Student DevOps | 🔵 To contact | — |
| [SAP](leads/sap-oriyah-community.md) | Oriyah | inside | Software Eng. Intern (Gateway) | 🔵 To contact | — |

<!-- DASHBOARD:END -->
