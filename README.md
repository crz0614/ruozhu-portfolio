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
| SyncBridge | Signed webhook ingestion, idempotent delivery, bounded retries and durable SQLite/PostgreSQL storage | [Source](https://github.com/crz0614/syncbridge) |

## Production evidence / 真实交付证据

### SyncBridge outbound safety — 2026-09-01

[Security PR #4](https://github.com/crz0614/syncbridge/pull/4) adds redirect
rejection to REST/Notion delivery and status-only HTTP errors. Local HTTP-server
tests verify that 301/302/303/307/308 redirects never reach a second endpoint with
credentials or payloads. This is source/test evidence, **not** deployed
WordPress-to-CRM end-to-end acceptance. The latter remains unverified.

[安全修复 PR #4](https://github.com/crz0614/syncbridge/pull/4) 为 REST/Notion
投递增加重定向拒绝及 HTTP 错误信息最小化。真实本地 HTTP 服务回归测试覆盖
五种跳转状态，确认第二个端点收不到凭据或数据。这是代码与测试证据，
**不代表** WordPress→CRM 已完成真实部署端到端验收。

[WordPress key-collision fix #5](https://github.com/crz0614/syncbridge/pull/5)
preserves distinct enquiry identifiers instead of stripping punctuation or
folding case. Boundary tests cover Unicode, zero, reserved hash namespaces and
legacy retry keys. Review the connector's bilingual upgrade/replay warning
before installing version 0.1.1. This remains source/CI evidence, not live CRM
acceptance.

[WordPress 编号碰撞修复 #5](https://github.com/crz0614/syncbridge/pull/5)
避免不同询盘编号被误去重，补充 Unicode、零值、哈希命名空间和旧重试键测试。
安装 0.1.1 前须阅读升级与历史数据重放警告；仍不代表真实 CRM 端到端验收。

[Database recovery PR #6](https://github.com/crz0614/syncbridge/pull/6)
separates delivery from outcome persistence: a failed database acknowledgement
retries only the same database write, not an already accepted delivery. SQLite
fault-injection tests cover failures before/after commit and interruptible shutdown;
the health endpoint returns 503 when its database probe fails. Process crashes can
still require reconciliation of `processing` records; this is not exactly-once
delivery or live WordPress→CRM acceptance.

[数据库恢复 PR #6](https://github.com/crz0614/syncbridge/pull/6)
将实际投递与结果写入分离，数据库确认失败时仅重试写入，不立即重复发送。
SQLite 故障注入覆盖提交前后失败与停止信号，健康接口在数据库探测失败时返回
503。进程崩溃后仍可能需要核对 `processing` 记录；不承诺恰好一次投递，
也不将本次回归测试当作真实 WordPress→CRM 验收。

[CSV integrity PR #7](https://github.com/crz0614/syncbridge/pull/7) validates
the complete input before queue writes, rejecting duplicate/empty headers,
incorrect column counts and invalid encoding/quoting. SQLite tests verify no
partial import on format errors, compatibility with prior deduplication keys,
and resumability after database failures. Database ingestion is still per-row,
not a whole-file transaction; directory-watcher concurrency remains unverified.

[CSV 完整性 PR #7](https://github.com/crz0614/syncbridge/pull/7) 在写队列前预检
整份输入，拒绝重复/空列名、列数异常及编码/引号错误。SQLite 回归测试验证坏文件
不会先导入部分行、旧幂等键仍兼容、数据库故障后可重试续传。入库仍按行提交，
不是整文件事务；目录监听并发场景仍待验证，不冒充客户生产验收。

[PostgreSQL container fix #8](https://github.com/crz0614/syncbridge/pull/8)
adds the missing driver to the shipped image and a running-container CI gate:
non-root/read-only startup, PostgreSQL readiness, operator/HMAC authorization,
signed ingestion and deduplication, authenticated HTTP fixture delivery, and
retained database state after restart. This is an actual container integration
test, not an external WordPress→CRM sandbox acceptance.

[PostgreSQL 容器修复 #8](https://github.com/crz0614/syncbridge/pull/8) 补齐镜像
缺失的数据库驱动，并在 CI 中实际启动非 root、只读容器，验证 PostgreSQL、
鉴权、签名入库、去重、HTTP 测试接收端投递和重启后的持久化。
这是容器集成测试，不冒充外部 WordPress→CRM 沙盒验收。

[Native setup repair #9](https://github.com/crz0614/syncbridge/pull/9) restores
the documented `init` command and loads literal `.env` configuration before native
commands. Generated secrets are not printed or overwritten; process environment
wins. CI installs and runs the CLI outside the checkout on Linux, Windows and
macOS. Docker context exclusions and an image-level check prevent local `.env`
from being included. These are installation checks, not external CRM acceptance.

[原生安装修复 #9](https://github.com/crz0614/syncbridge/pull/9) 补齐实际缺失的
初始化命令和配置加载，并增加三个操作系统的真实安装后命令测试。密钥不打印、
不覆盖，进程环境优先；Docker 增加配置排除及镜像内检查。此证据只覆盖安装与
配置，不代表外部 CRM 验收。

[Configuration guard #10](https://github.com/crz0614/syncbridge/pull/10)
requires explicitly selected environment files and rejects unsupported non-empty
database URL schemes before opening storage, preventing accidental SQLite fallback.
[CI #102](https://github.com/crz0614/syncbridge/actions/runs/33541380494) exercises
the configuration regressions, three native installation platforms, and the
PostgreSQL container integration gate. Empty/unset database URLs retain SQLite;
no automatic data migration or external CRM acceptance is claimed.

[配置保护 #10](https://github.com/crz0614/syncbridge/pull/10) 在显式配置文件
缺失或数据库 URL 类型错误时停止，避免误用 SQLite。回归测试覆盖命令不启动、
数据库不被打开及错误信息不泄密；同时运行三平台安装与 PostgreSQL 容器检查。
数据库 URL 未设置/空值仍保留 SQLite 行为；不自动迁移历史数据，不冒充外部 CRM 验收。

### Marketplace atomic checkout settlement — 2026-09-03

[Payment safety PR #8](https://github.com/crz0614/marketplace-payment-loop/pull/8)
moves Checkout event deduplication and order settlement into one restricted PostgreSQL
transaction. It validates paid status, currency, amount, Checkout/order identity and
payment intent; a mismatch rolls back the event record so a corrected Stripe retry is
not suppressed. [CI run 33753880691](https://github.com/crz0614/marketplace-payment-loop/actions/runs/33753880691)
passed 11 tests plus syntax and image-build checks. On 2026-09-03, migration
`20260903130601_atomic_checkout_settlement` was applied to hosted PostgreSQL; a disposable
transaction verified initial settlement, duplicate suppression and rollback, and Edge
Function v4 was deployed. External HTTP probing was blocked by the verification
environment, so current uptime is not claimed. Real Stripe Checkout/webhook/refund
acceptance remains outstanding, so hosted payment routes stay disabled.

[支付安全 PR #8](https://github.com/crz0614/marketplace-payment-loop/pull/8)
将 Checkout 事件去重与订单入账收进同一受限 PostgreSQL 事务，并核验支付状态、
币种、金额、Checkout/订单对应关系及 Payment Intent。校验失败会回滚事件记录，
避免阻断修正后的 Stripe 重试。CI 已通过 11 项测试、语法及镜像构建检查。2026-09-03
已将 `20260903130601_atomic_checkout_settlement` 应用于线上 PostgreSQL，在可回滚
事务中验证首次入账、重复抑制与失败回滚，并部署 Edge Function v4。外部 HTTP 探测受
验证环境网络策略阻止，因此不声明当前在线可用；真实 Stripe 支付、签名 Webhook 与退款
验收仍未完成，线上支付接口继续关闭。

### Marketplace atomic registration — 2026-09-03

[Registration integrity PR #10](https://github.com/crz0614/marketplace-payment-loop/pull/10)
creates the account and first hashed session in one restricted PostgreSQL transaction.
Hosted migration `20260903140721_atomic_registration` was verified with disposable data:
the success path created exactly one user and one session; a forced session conflict
left zero orphan users. Edge Function v5 was deployed. The CI suite passed 11 tests.

[注册完整性 PR #10](https://github.com/crz0614/marketplace-payment-loop/pull/10)
将账户与首个哈希会话收进同一受限 PostgreSQL 事务。线上迁移
`20260903140721_atomic_registration` 使用可回滚数据验证：正常路径只创建一个
用户和一个会话；强制会话冲突后遗留用户为零。Edge Function v5 已部署，CI 的
11 项测试通过。

### Pages deployment recovery — 2026-09-02 (UTC+08:00)

[Pages run 33536150633](https://github.com/crz0614/ruozhu-portfolio/actions/runs/33536150633)
built commit `bf44a82` successfully but timed out in `updating_pages`. A bounded
retry completed successfully at 2026-09-01 18:00:32 UTC without changing code or
weakening checks. This records deployment-system success, not a fresh browser
end-to-end assertion; public-page inspection was unavailable in this check.

Pages 对 `bf44a82` 构建成功，但发布状态持续等待直至超时；仅重试失败任务后
平台确认部署成功，未修改代码或放宽验收。本记录是部署系统证据，不代替新的
浏览器端到端验证；本次公开页面读取未能完成。

This portfolio is an index of inspectable engineering work, not a collection of invented customer dashboards. Each listed project links to source code, a live service where one is available, and an explicit statement of its current operational boundary.

本作品集用于索引可核验的工程成果，不使用虚构客户、虚构订单或浏览器本地样例冒充生产数据。每个项目均链接源代码；具备线上服务的项目同时提供访问地址，并明确说明当前已接入能力与尚未接入的边界。

The former browser-only product mockups are intentionally excluded from the public portfolio. A project is listed only when its operational behavior is supported by a real backend, persistent storage, a third-party API, automated tests, or an explicit deployment boundary.

The legacy `projects/` pages were removed from the published repository as well as the homepage. CI rejects any attempt to restore those browser-local mockups, so obsolete demo URLs cannot remain publicly accessible and contradict the evidence policy.

原有的纯浏览器产品样例已从公开作品集中撤下。只有具备真实后端、持久化存储、第三方 API、自动化测试或明确部署边界的项目才会公开展示。

旧版 `projects/` 页面也已从发布仓库中删除，而不是仅从首页隐藏。CI 会拒绝这些浏览器本地样例重新进入仓库，避免旧演示链接继续公开并与证据标准冲突。

Every documented deployment is probed daily against an explicit HTTP access contract. Public previews must return `200` and contain an application-specific marker, preventing a blank page or wrong deployment from passing. Protected operator surfaces must return `401` rather than expose private data. The Support Copilot contract also exercises its live JSON health API, so a stale frontend-only deployment cannot pass. The probe verifies required content and security headers and rejects redirects to an undocumented host. Each run publishes a machine-readable health report as a GitHub Actions artifact.

所有公开列出的部署均按明确的 HTTP 访问契约每日检查：公开预览必须返回 `200` 并包含应用专属标识，防止空白页或错误部署被误判为正常；受保护的操作界面必须返回 `401`，避免泄露私有数据。Support Copilot 还会实际调用线上 JSON 健康接口，过期的纯前端部署无法通过检查。检查同时核验必要的内容类型与安全响应头，并拒绝跳转到未声明主机的重定向。每次检查都会生成可机器读取的健康报告并保存为 GitHub Actions 构件。

## Capabilities

### Probe failure semantics / 探测失败分类

Reports distinguish `passed`, `failed` (an HTTP response violates its contract),
and `unverified` (no HTTP response because of proxy, DNS, TLS or timeout errors).
Unverified probes keep `healthy=false` and a nonzero exit code, but do not invent
missing content/security headers. Transport details are not proof of an origin
outage. All existing checks remain enforced when a response is received.
No database migration is needed; rollback restores the preceding checker.

报告区分通过、响应不符合契约和未能验证。代理、DNS、TLS 或超时导致未收到
响应时，仍以非零退出码阻止误报健康，但不再声称服务缺少未曾观测到的响应头。
网络错误不等同于源站故障；收到响应后仍执行全部安全和内容检查。无需数据迁移，
回滚时恢复前版检查脚本即可。

- **AI engineering:** structured generation, classification, translation and human approval flows
- **Automation:** browser execution, APIs, resumable tasks and evidence-backed completion
- **Backend:** typed APIs, PostgreSQL, queues, concurrency, retries and metrics
- **Developer tooling:** deployment diagnosis, review-safe GitHub automation and explicit security boundaries
- **Languages and platforms:** Python, C++, Rust, Go, TypeScript, Next.js, Playwright, Docker and cloud deployment

## Evidence policy

No invented clients, revenue, user counts or delivery metrics are included. Claims are supported by inspectable source, automated checks, live deployments or clearly stated implementation boundaries. Credentials and private records remain outside public repositories.
