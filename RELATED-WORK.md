# RELATED WORK · 本草案与既有工作的关系

这一页的目的只有一个：让评审在半小时内看清 **哪些机制已经有人做了、我们照抄了什么、我们没做什么、以及唯一值得讨论的差异在哪**。它不主张新颖性；凡是借来的，写明借自哪里。

状态：draft-00 配套说明，非规范文本。

## 一 直接相邻：签名收据 / 透明收据

| 工作 | 形态 | 与我们重合 | 我们不同 | 我们缺 |
|---|---|---|---|---|
| **SCITT**，RFC 9943（Standards Track，2026）+ RFC 9942（COSE Receipts）+ SCRAPI `draft-ietf-scitt-scrapi` | Signed Statement 注册到 Transparency Service，TS 出 receipt | "可信收据"这件事本身；都强调 receipt 只签字节、不证真 | 我们不要求 TS，不需要注册流程，离线可判；我们的 receipt 是线性摘要链，不是 COSE | 我们**没有**透明日志/见证人（TS 提供的正是我们不提供的） |
| `draft-noa-scitt-ai-agent-receipt-01`（SCITT 的 AI Agent Action Receipt Profile） | 把 receipt 用到 agent 动作上 | 受众相同：给 agent 动作留可验证据 | 它仍以 TS 为锚；我们以"包内闭合 + 可选外部锚"为最小形态 | 同为 agent 场景，但它有 TS 生态背书 |
| `draft-gruszka-signed-evaluation-receipts` | 单个 JSON 评测收据，Ed25519 | 结论句几乎同构：收据证明谁签的，不证明结果是真的 | 我们管的是"生命周期 + 证据包"，不是单次评测 | 它更小、更容易被采纳为单一格式 |
| `draft-watts-eqr-conformance` | 21 条冻结规范向量 + 15 条对抗补充；含"不得把 INDETERMINATE 升格为 PASS"的负测 | **三值判定纪律**：把不确定/不得升格写成 MUST-reject | 我们三值是 PASS/FAIL/INCONCLUSIVE（包层），并有 `keyswap PASS` 这种"绿而不安全"的显式负对照 | 它的向量集有摘要冻结与规范编号，我们只有仓库内期望表 |
| `draft-farley-acta-signed-receipts` + `agent-governance-testvectors` | Ed25519 访问控制收据；CI 跨实现回放（4 个实现通过，2 个未通过） | 同一条路：收据 + 共享向量 + CI 回放 | 我们**还没有**跨实现回放（只有同方两实现的一致检查） | 这是他们领先我们的地方：真·多实现 |
| `draft-chueayen-attestation-receipts` | 推理决策收据 + PyPI/npm 参考验签器 | 离线可验、固定测试公钥 | 我们覆盖整包与生命周期链 | 发布渠道（PyPI/npm）我们只有一个包 |

**结论**：收据格式这个赛道已经拥挤。"我们做了一种收据"不是差异化；差异化只能在 **包层（身份+生命周期+动作证据一体）** 与 **不需要信任根的离线判定** 上。

## 二 媒体溯源与 PKI 路线

**C2PA 2.4（2026-04）+ 一致性计划 + Trust List**：6000+ 成员与附属机构；软启动于 2025-06；2026-01-01 起旧 ITL 冻结；产品需通过一致性评估 + 安全评估 + 法务准入，再由 Trust List 上的 CA 签发签名证书，证书携带 assurance level；相机/手机侧已有 Nikon、Sony、Canon、Leica、Pixel 10、三星等落地。

借来的：**Conforming Products List 的 JSON 化、Trust List 与 assurance level 的分层**——我们的"目录 + 六态"就是这套思路的极简版（见 `.github/registry/`）。
不做的：CA 签发、安全评估、法务准入、硬件背书。C2PA 自己的 Harms Modelling 也写明：2.0 起"只能签自己的、必须在 trust list 内"，对小型组织与个人构成门槛——**这正是我们不设信任根的理由，也是我们的市场缝隙**。

## 三 构建溯源路线

**sigstore / SLSA / GitHub Artifact Attestations**：Fulcio 短时证书 + Rekor 透明日志 + in-toto/SLSA 谓词；npm provenance、Homebrew ~7000 bottles、PyPI 至 2026-03 已有 132,360+ 包带 attestation（约占上传 17%）；但一项 2026 的测量研究指出 npm 上 keyless 签名只覆盖 5.9% 的发布，**"有机制"与"有覆盖"是两件事**。

借来的：**bundle 式封装与"摘要即承诺"**；我们的 §8 外部锚只把 root 过线，不外传证据。
不做的：构建溯源。我们不证明"这个包是怎么构建的"，只证明"这份证据自洽且未被改"。
不重复的坑：把 coverage 当 adoption 讲。

## 四 目录与注册表路线

**MCP Registry**（官方，preview）：以反向 DNS 命名空间 + GitHub/域名归属验证作为唯一信任手段，代码扫描交给下游；2026-11 的第三方普查读到 **59,944 个 active server**，并指出 PR #1806 的"共享 remote URL、不校验 URL 所有权"缺口。

**Agent Skills 供应链**（OWASP Agentic Skills Top 10 AST02；arXiv 2605.11418）：SKILL.md 本身就是语义攻击面——发现阶段最高 86% 成对胜率、选择阶段 77.6%、治理阶段 36.5%–100% 逃避拦截；ClawHub 上发布门槛曾是"一个 SKILL.md + 一周龄 GitHub 账号"。

借来的：**命名空间即身份**（我们的目录条目要求 `namespace` + 归属证据）。
差异：注册表给的是"是谁发的"，我们给的是"这份证据能不能被字节层复核"。二者互补，不互替。

## 五 认证/审计路线（商业侧）

**AIUC-1**：6 原则 / 51 项要求，季度第三方对抗测试（典型 1,000–3,000 次模拟），认证由认可审计机构出具（Schellman 为首家，2026-02-03），证书有效期 12 个月。

我们的位置：**不是认证机构，也不出证书**。我们提供可被这类审计直接采信的机器可核证据件；把"自评"升级成"可复跑"，但不跨越到"第三方结论"。

## 六 身份路线

**W3C VC 2.0（2025-05-15 成为 Recommendation）**、**AGNTCY Agent Badge（W3C VC + Identity Node）**、**A2A（Linux Foundation，100+ 公司）**、**MCP 的 OAuth 2.1 + RFC 8707 资源指示**、`draft-tonyai-a2a-trust`、`draft-nandakumar-agent-sd-card`、OpenA2A AIP。

我们的位置：**不签发身份**，只消费身份引用（`agent_id` / DID / VC 的摘要可以进包，但我们不校验证书链的信任根）。这一层已经很拥挤，进去就是把最贵的活干在最不缺人的地方。

## 七 医疗器械与 AI 设备的缝隙

**FDA《Cybersecurity in Medical Devices》2026-02-03 终版**（取代 2025-06 与 2023-09 版），锚定 AAMI SW96 与 **IEC 81001-5-1**；AI 赋能设备软件功能的 draft guidance 要求在 Cybersecurity/Interoperability 一节说明 AI 相关威胁建模、测试与控制。现实是：这些提交件是文档与截图，**没有一种"可被复核的字节结构"**。

这是本草案唯一真正空着的场景：把"证据边界检查"落到一个具体的、有法定提交义务的包上。我们**不**声称符合 FDA 或 IEC 81001-5-1；我们只提供让审查者能重算的那一层。

## 八 我们不主张的

- 不主张"首个""唯一""领先"。
- 不主张与 SCITT/C2PA/AIUC-1 互认或对齐（**尚未**做过任何互操作测试）。
- 不主张我们的向量是第三方一致性套件（目前只有一个实现被跑过）。

## 参考文献（可直达）

- RFC 9943 https://www.rfc-editor.org/rfc/rfc9943.pdf ／ RFC 9942（COSE Receipts）
- SCRAPI https://datatracker.ietf.org/doc/draft-ietf-scitt-scrapi/
- AI Agent Action Receipts https://www.ietf.org/archive/id/draft-noa-scitt-ai-agent-receipt-01.html
- Signed Evaluation Receipts https://www.ietf.org/archive/id/draft-gruszka-signed-evaluation-receipts-03.txt
- EQR Conformance https://datatracker.ietf.org/doc/draft-watts-eqr-conformance/
- ACTA Signed Receipts https://www.ietf.org/archive/id/draft-farley-acta-signed-receipts-02.txt
- Attestation Receipts https://www.ietf.org/archive/id/draft-chueayen-attestation-receipts-02.txt
- C2PA Conformance https://c2pa.org/conformance/ ／ 规范 2.4 https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html
- C2PA Harms Modelling https://c2pa.org/specifications/specifications/2.0/security/Harms_Modelling.html
- MCP Registry https://modelcontextprotocol.io/registry/about
- sigstore 生态路线 https://github.com/sigstore/community/blob/main/ROADMAP.md
- OWASP Agentic Skills Top 10 AST02 https://owasp.org/www-project-agentic-skills-top-10/ast02
- VC 2.0 https://www.w3.org/TR/vc-data-model-2.0/
- AGNTCY Agent Badge https://blogs.agntcy.org/technical/identity/2026/08/25/agent-identity-tbac-a2a-task-authorization.html
- AIUC-1 https://www.aiuc-1.com/
- FDA 2026 终版 https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-management-system-considerations-and-content-premarket
