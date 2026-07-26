# Hayate design-partner program

Hayate is recruiting three owner-external applications to test the decisions
that will become its v1 compatibility contract. This is a bounded engineering
partnership for teams already planning to build or migrate a real service, not
a request for endorsements.

[Apply with the public design-partner intake form](https://github.com/hayatepy/.github/issues/new?template=design_partner.yml).

## The three tracks

We are looking for one application in each track:

1. a conventional HTTP API on CPython and ASGI;
2. an MCP or agent backend;
3. a Cloudflare Workers deployment.

An application may cover more than one track. It should use a released Hayate
package and should intend to use at least one ecosystem package alongside the
core, such as `hayate-auth`, `hayate-mcp`, `hayate-openapi`, or `hayate-sql`.

## What partners receive

- bounded help selecting the smallest suitable package set;
- a guided first local run, test, and deployment;
- prompt investigation of reproducible P0/P1 adoption blockers;
- a direct route for evidence-backed documentation, scaffold, API, runtime,
  and compatibility feedback.

This program does not provide a production SLA, on-call support, funding, or
open-ended application development. Participation and timing are agreed after
intake; submitting an application does not guarantee selection.

## What we measure

The program records the same adoption evidence for every partner:

- time to the first passing test;
- time to the first successful local request;
- time to the first deployment, when deployment is in scope;
- production dependency count and deployment or bundle size;
- every maintainer intervention, categorized as documentation, scaffold, API,
  runtime, or ecosystem compatibility work;
- unresolved P0/P1 blockers and the v1 decision they affect.

An application counts toward the program only after an owner-external project
runs a released Hayate package. Repository views, CI bots, unfinished intake
forms, and maintainer-owned projects do not count.

## Privacy and publication

The intake issue is public. Include only high-level, non-confidential
information. Never post credentials, tokens, customer data, proprietary source
code, unreleased product details, or vulnerability information.

If selected, we can agree on a private follow-up channel before discussing
non-public constraints. General findings become public issues without exposing
partner-specific details. A named or anonymized case study is published only
with the partner's explicit approval. Security vulnerabilities must use the
affected repository's private vulnerability-reporting flow.

## Selection and exit

Selection balances the three tracks, runtimes, current stacks, and target
milestones. A suitable partner:

- is independent of the Hayate maintainer;
- has a concrete application and accountable technical contact;
- can test a released package on a mutually agreed timeline;
- can share measured onboarding outcomes, privately when necessary.

Either side may pause or end the engagement. A completed engagement has run a
released Hayate package, captured the agreed measurements, categorized all
maintainer interventions, and resolved or explicitly accepted every observed
P0/P1 adoption blocker.
