---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "s3-credentials CLI"
sources:
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"

generation_complete: true
---

# s3-credentials

## Description

s3-credentials is a command-line tool written by [[Simon Willison]] for creating credentials that grant access to S3 buckets. Version 0.15 was released on 2023-04-30, according to the release list in the source. In the [[sources/2023-05-01-weeknotes_72fe7e|2023-05-01 weeknotes]], it is one of the two CLI tools combined with [[shot-scraper]] to build the image pipeline for [[Today I Learned]], which stores generated social media card images in S3. The pipeline moved there after the images outgrew the SQLite database and pushed the deployment past [[Vercel]]'s 50MB limit. Willison maintains s3-credentials alongside [[Datasette]] and shot-scraper.

## Related Entities

- [[entities/shot-scraper|shot-scraper]]

## Related Concepts

- [[concepts/social-media-cards|Social media cards]]

## Mentions in Source

- "This ended up being a fun exercise in combining both `shot-scraper` and my [s3-credentials](https://s3-credentials.readthedocs.io/) CLI tools." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]