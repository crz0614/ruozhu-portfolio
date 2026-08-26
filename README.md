# Ruozhu Chen — Software & AI Engineering

Public engineering profile focused on AI workflows, developer tooling, automation and backend infrastructure.

[Live site](https://crz0614.github.io/ruozhu-portfolio/) · [GitHub profile](https://github.com/crz0614)

## Selected work

| Project | What it demonstrates | Links |
|---|---|---|
| Remote Gig Desk | Evidence-gated remote-work discovery, application execution and reply tracking | [Protected runtime (401 expected)](https://remote-gig-desk-vercel.vercel.app/) · [Source](https://github.com/crz0614/remote-gig-desk-vercel) |
| Deploy Doctor | PostgreSQL queue, recoverable worker leases, disposable network-disabled Docker workspaces, Prometheus metrics and approval-gated fixes | [Protected control plane (401 expected)](https://ruozhu-deploy-doctor.lambdfefoazis.chatgpt.site) · [Source](https://github.com/crz0614/ruozhu-deploy-doctor) · [Worker milestone](https://github.com/crz0614/ruozhu-deploy-doctor/pull/3) |
| Distributed Job Runner | Durable PostgreSQL execution, recovery, idempotency, authenticated rate limiting and Prometheus metrics | [Source](https://github.com/crz0614/distributed-job-runner) |
| AI Freelance Workbench | Verified opportunity filtering, server-persisted pipeline/drafts, append-only audit events and privacy-safe Prometheus metrics | [Preview](https://ai-freelance-workbench.vercel.app) · [Source](https://github.com/crz0614/ai-freelance-workbench) · [Audit milestone](https://github.com/crz0614/ai-freelance-workbench/pull/5) |
| Multilingual Support Copilot | API-verified GitHub sources, durable triage, signed idempotent webhooks and protected operator mutations | [Preview](https://multilingual-support-copilot.vercel.app) · [Source](https://github.com/crz0614/multilingual-support-copilot) |

## Production evidence / 真实交付证据

This portfolio is an index of inspectable engineering work, not a collection of invented customer dashboards. Each listed project links to source code, a live service where one is available, and an explicit statement of its current operational boundary.

本作品集用于索引可核验的工程成果，不使用虚构客户、虚构订单或浏览器本地样例冒充生产数据。每个项目均链接源代码；具备线上服务的项目同时提供访问地址，并明确说明当前已接入能力与尚未接入的边界。

The former browser-only product mockups are intentionally excluded from the public portfolio. A project is listed only when its operational behavior is supported by a real backend, persistent storage, a third-party API, automated tests, or an explicit deployment boundary.

原有的纯浏览器产品样例已从公开作品集中撤下。只有具备真实后端、持久化存储、第三方 API、自动化测试或明确部署边界的项目才会公开展示。

Every documented deployment is probed daily against an explicit HTTP access contract. Public previews must return `200` and contain an application-specific marker, preventing a blank page or wrong deployment from passing. Protected operator surfaces must return `401` rather than expose private data. The Support Copilot contract also exercises its live JSON health API, so a stale frontend-only deployment cannot pass. The probe verifies required content and security headers and rejects redirects to an undocumented host. Each run publishes a machine-readable health report as a GitHub Actions artifact.

所有公开列出的部署均按明确的 HTTP 访问契约每日检查：公开预览必须返回 `200` 并包含应用专属标识，防止空白页或错误部署被误判为正常；受保护的操作界面必须返回 `401`，避免泄露私有数据。Support Copilot 还会实际调用线上 JSON 健康接口，过期的纯前端部署无法通过检查。检查同时核验必要的内容类型与安全响应头，并拒绝跳转到未声明主机的重定向。每次检查都会生成可机器读取的健康报告并保存为 GitHub Actions 构件。

## Capabilities

- **AI engineering:** structured generation, classification, translation and human approval flows
- **Automation:** browser execution, APIs, resumable tasks and evidence-backed completion
- **Backend:** typed APIs, PostgreSQL, queues, concurrency, retries and metrics
- **Developer tooling:** deployment diagnosis, review-safe GitHub automation and explicit security boundaries
- **Languages and platforms:** Python, C++, Rust, Go, TypeScript, Next.js, Playwright, Docker and cloud deployment

## Evidence policy

No invented clients, revenue, user counts or delivery metrics are included. Claims are supported by inspectable source, automated checks, live deployments or clearly stated implementation boundaries. Credentials and private records remain outside public repositories.
