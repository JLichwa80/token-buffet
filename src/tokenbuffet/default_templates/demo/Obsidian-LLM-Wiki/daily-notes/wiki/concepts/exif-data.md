---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "EXIF"
  - "Exchangeable image file format"
sources:
  - "[[sources/2023-04-23-weeknotes_572e37]]"

generation_complete: true
---

# EXIF data

## Definition

EXIF data is metadata embedded in image files, such as photos, that records information about the camera and the capture, including orientation and GPS location.

## Key Characteristics

- Stored inside the image file itself, alongside the pixel data
- Records capture details such as camera information and orientation
- Can include GPS location fields that give where a photo was taken
- The orientation tag tells software how to rotate an image so it displays the right way up

## Applications

- Displaying photos upright in galleries by applying the EXIF orientation tag, as in the [[Niche Museums]] photo gallery upgrade described in [[sources/2023-04-23-weeknotes_572e37|the 2023-04-23 weeknotes]]
- Using EXIF location fields to place photos on a museum website, which is why they are useful for [[Niche Museums]]
- Documenting how to interpret orientation and location data, as in Simon Willison's TIL "Interpreting photo orientation and locations in EXIF data", which the post links as the record of his learning

## Related Concepts

- [[concepts/large-language-models|Large Language Model]]

## Related Entities

- [[entities/niche-museums|Niche Museums]]

## Mentions in Source

- "Here’s the issue, the full set of changes and a TIL describing what I learned about photo EXIF data in figuring out this project." — [[_Inbox/2023-04-23-weeknotes|2023-04-23-weeknotes]]