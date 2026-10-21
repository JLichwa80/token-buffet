---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags: [terminology]
aliases:
  - "Bounding box"
  - "bbox"
sources:
  - "[[sources/2024-09-06-weeknotes_32f8a8]]"

generation_complete: true
---

# Bounding boxes

## Definition

A bounding box is a rectangle that marks where an object appears in an image. Vision models can return bounding boxes as coordinates, which can be drawn over the image to show the detected object.

## Key Characteristics

- Defined as a rectangle that encloses an object's location in an image.
- Usually expressed as coordinates (for example, JSON values).
- Can be drawn over the source image to check a model's detections visually.
- Reliability varies by model. The author reports that [[Gemini|Gemini Pro]] was the only vision LLM he tried that handled bounding boxes reliably.

## Applications

- **Visualizing model output:** The author uses [[Gemini|Gemini Pro]] to return bounding boxes as JSON coordinates and draws them on the image, as implemented in the [[gemini-bbox]] tool.
- **Figure extraction from PDFs:** The author proposes detecting bounding boxes on PDF pages to locate figures. Each figure can then be cropped out as a separate image.

## Related Concepts

## Related Entities

- [[entities/gemini|Gemini]]

## Mentions in Source

- "Gemini Pro is the only of the vision LLMs that I’ve tried that has reliable support for bounding boxes." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]
- "I have a hunch that getting Gemini to return bounding boxes for figures on the PDF pages could be the key here, since then each figure could be automatically extracted as an image." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]