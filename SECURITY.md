# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a vulnerability in AHTSE, please follow these steps:

1.  **Do NOT open a public issue.**
2.  Email the maintainers directly at `security@example.com` (replace with actual email if applicable) or use the GitHub Security Advisory "Report a Vulnerability" feature if enabled.
3.  Include details about the vulnerability, steps to reproduce, and potential impact.

We will acknowledge your report within 48 hours and work to provide a fix as soon as possible.

## Security Best Practices for Users

*   **Local Execution**: AHTSE is designed to run locally. Do not expose the API to the public internet without proper authentication and rate limiting (not included in the core repo).
*   **Data Privacy**: The system is designed to not store personal data. Ensure your input data complies with your local privacy regulations.
*   **Model Safety**: This tool is a safety layer, but it is not infallible. Always have a human in the loop for critical decision-making.
