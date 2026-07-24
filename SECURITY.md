# Security Policy

## Scope

mad-scientist-skills is a collection of text-based AI prompt definitions for Claude Code. The skills contain no executable code, run no server, and store no user data. They are Markdown files that instruct a language model how to perform code audits.

The primary security concern for this project is **prompt injection**: a malicious skill definition or crafted input could attempt to override the model's intended behavior or exfiltrate information through the model's responses. If you discover a way to exploit skill definitions to cause Claude Code to behave outside its intended scope, that is in scope for this policy.

The following are **out of scope**:

- Vulnerabilities in Claude Code itself or the Anthropic API (report those to Anthropic directly)
- Vulnerabilities in repositories that the skills are used to audit
- General bugs or incorrect findings (open a regular GitHub issue)

## Supported Versions

Only the latest release is actively maintained. Security fixes are not backported to older versions.

| Version | Supported |
|---------|-----------|
| Latest release | Yes |
| Older releases | No |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Please report vulnerabilities via [GitHub Security Advisories](https://github.com/karsten-s-nielsen/mad-scientist-skills/security/advisories/new). This keeps the report private until a fix is available.

Include in your report:

- A description of the vulnerability and its potential impact
- Steps to reproduce or a proof-of-concept skill definition or input
- Any suggested mitigations if you have them

## Response Timeline

This project is volunteer-maintained. We aim to acknowledge reports and respond with a timeline on a best-effort basis, typically within 7 days. We appreciate your patience and your help keeping the project trustworthy.
