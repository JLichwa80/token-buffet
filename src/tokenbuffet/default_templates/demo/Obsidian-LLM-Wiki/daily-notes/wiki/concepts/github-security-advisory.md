---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "GHSA"
  - "security advisory"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# GitHub security advisory

## Definition

A GitHub security advisory is a published notice that a repository maintainer uses to disclose a security vulnerability. In the source, [[Simon Willison|Willison]] used one to disclose a bug in the [[Datasette]] 1.0 alpha that leaked database and table names to unauthenticated users. The advisory was later assigned a CVE, because GitHub is a CVE Numbering Authority (CNA). The source describes this process as the one that led to [[CVE-2023-40570]].

## Key Characteristics

- Published by a repository maintainer to disclose a security vulnerability in their project
- Hosted on GitHub and tied to the repository it concerns
- Can be assigned a CVE identifier, because GitHub is a CVE Numbering Authority
- Identified by a GHSA ID in GitHub's advisory system (the "GHSA" alias)

## Applications

- Disclosing vulnerabilities in open-source projects hosted on GitHub, as in the [[Datasette]] 1.0 alpha bug
- Obtaining a CVE for a vulnerability through GitHub's CNA role, as in [[CVE-2023-40570]]
- Notifying users of affected software, including hosted products such as [[Datasette Cloud]]

## Related Concepts

- [[concepts/cve-2023-40570|CVE-2023-40570]]

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/github|GitHub]]
- [[entities/datasette-cloud|Datasette Cloud]]

## Mentions in Source

- "I issued a GitHub security advisory for this: [Datasette 1.0 alpha series leaks names of databases and tables to unauthenticated users](https://github.com/simonw/datasette/security/advisories/GHSA-7ch3-7pp7-7cpq), which has since been issued a CVE, [CVE-2023-40570](https://nvd.nist.gov/vuln/detail/CVE-2023-40570)—GitHub is [a CVE Numbering Authority](https://docs.github.com/en/code-security/security-advisorie..." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]