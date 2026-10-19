---
name: test-proxy-connection
description: Use this skill to simulate an Obsidian query locally, verifying the proxy and router are correctly formatting the exact Vercel AI SDK Responses API payload.
---

# Test Proxy Connection

Before switching back to Obsidian, it is useful to verify that the proxy and router are running and correctly adhering to the strict Vercel AI SDK Responses API schema.

## Workflow

1.  Use `curl` or a Python script to send a POST request to `http://127.0.0.1:8000/v1/responses` (or whichever port the active proxy is running on).
2.  The request payload MUST use the strict `"input"` array format required by the Vercel AI SDK:
    ```json
    {
      "input": [
        {
          "role": "user",
          "content": [
            {
              "type": "input_text",
              "text": "Hello, proxy!"
            }
          ]
        }
      ]
    }
    ```
3.  Verify the response structure. It MUST contain the `"output"` array and `"type": "output_text"` instead of the standard Chat Completions `{"choices": ...}` JSON.
    ```json
    {
      "output": [
        {
          "type": "output_text",
          "text": "..."
        }
      ]
    }
    ```
