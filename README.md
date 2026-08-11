# Ruozhu Chen — Engineering Portfolio

Production-oriented software engineering work with inspectable source, live deployments, and explicit evidence boundaries.

## Featured project: Remote Gig Desk

Remote Gig Desk is a full-stack workbench for discovering verified remote opportunities, preparing individualized application materials, tracking replies, and executing supported ATS submissions. It is designed to avoid two common automation failures: fabricated opportunity data and false “submitted” states.

### Links

- [Live workbench](https://remote-gig-desk-vercel.vercel.app/) — owner-authenticated because it contains private application data
- [Source repository](https://github.com/crz0614/remote-gig-desk-vercel)
- [Public portfolio page](https://crz0614.github.io/ruozhu-portfolio/)

### Implemented capabilities

- Multi-source opportunity aggregation with original source links
- Complete per-opportunity Chinese translation using a free translation path
- Job-specific application packs grounded in a private profile and verified evidence
- Automatic DOCX résumé creation and real attachment upload
- Gmail reply synchronization, classification, translation, summary, and next-action tracking
- Greenhouse, Lever, Ashby, and Workable browser execution
- Verified session reuse and explicit CAPTCHA/MFA/legal-confirmation takeover
- Submission evidence validation before a task can become `submitted`
- Verified portfolio import, preview, GitHub synchronization, and Pages publishing

### Architecture

| Layer | Technology |
|---|---|
| Web application | Next.js 16, React 19, TypeScript |
| Persistence | Neon serverless PostgreSQL |
| Automation | Vercel Sandbox, Playwright, paired Chrome extension |
| Integrations | Gmail OAuth, GitHub OAuth/API, Gemini free tier |
| Deployment | Vercel and GitHub Pages |

### Trust and privacy boundaries

- Private profile, résumé, email, OAuth tokens, and application records are not stored in this public repository.
- Tokens and private profile data are encrypted before database storage.
- CAPTCHA, MFA, identity, and legal-consent prompts are sent to a human checkpoint rather than bypassed.
- A click is not treated as a successful submission; official provider evidence is required.
- No fictional client, revenue, user-count, or delivery metric is presented.

### Verification

The repository includes automated coverage for ATS URL detection, session reuse, attachment delivery, evidence validation, cloud execution checkpoints, email analysis, translation completeness, opportunity state, and portfolio publishing. The test command also performs a production Next.js build.

```bash
cd remote-gig-desk-vercel
npm install
npm test
```

## Current scope

This portfolio currently contains one project because it is the only public repository with directly inspectable implementation evidence. Additional projects will be added only when their source, deployment, or other evidence is available—never as invented placeholders.
