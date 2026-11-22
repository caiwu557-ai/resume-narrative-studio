---
name: resume-narrative-studio
description: Use when a user wants to create, revise, tailor, audit, or visually design a resume/CV/academic profile or portfolio from conversations, raw notes, uploaded files, source records, and iterative human feedback; especially when the user wants guided interviews, audience-specific storytelling, evidence checks, and multiple review stages.
---

# Resume Narrative Studio · 人机共创简历工作流 v1.3.0

**本 Skill 的产品是「帮助用户作出更好的展示判断」的多轮过程，以及由此生成的可靠简历。** 无法从一次填表替代人的自我判断。不得把本 Skill 简化成一条提示词或「上传文件直接生成最终版」。

## 使用前的五个原则

1. **读者优先**：先弄清对方要依据什么决定是否见你，再选素材、排序、命名、设计。向用户说明自己的暂定读者模型，让其修正。
2. **内部完整，对外精选**：建立完整的事实/证据台账；投递稿只选有帮助的强项。内部核验记录、失败经验与项目风险不得机械地灌入简历正文；如果某状态是理解资历所必需的，应准确标注。
3. **由人决定价值和身份，由 AI 承担整理与制作**：人决定个人定位、强调和回避、表达是否像自己；AI 负责整理证据、追问、改写、对标、排版、检验。必须给用户独立的纠偏机会。
4. **真相约束是硬边界**：可强化表达、压缩细节、突出贡献；不得虚构论文、奖项、工作职责、临床操作、数据指标、岗位、项目成熟度或“独立开发”。
5. **反馈改变方法**：不能只在原句上换词。识别反馈对应的根因（受众/内容/结构/文字/视觉/事实），重做受影响的前置决策并复查全稿。

## 启动规则

- 用户已有简历/资料：**先读原件，继承已知信息与已确认决定**；不要重复索取已经给出的姓名、用途、联系方式或偏好。
- 只有一句「帮我做简历」：先确认尚未知的高价值事项，**一次零到两个**：①交给谁/为哪一机会；②最希望对方记住的两三项优势。允许不知道，由 AI 给可调整的建议。
- 用户给了许多散乱文件：先列出已获得的材料类型、可提炼内容与缺口，再问最影响结果的一个问题；不要一次抛几十个问题或强制用户填长表。
- 用户只要求局部修订：先完成局部修订，但检查修改是否破坏整份叙事和分页；必要时解释牵连范围。
- 用户要求多轮共创：按下面全部阶段推进，**每轮只交付当前阶段所需的决定**，用户可要求跳转/暂定。

## v1.2 个性化必读入口（不增加固定访谈轮次）

先读 `references/15-low-friction-collaboration.md`，维护 `templates/personalization_contract.json`。优先从已有授权材料识别意图，已知信息不重复问，低风险工作直接做。内置规范不等于给用户的问卷。快速档、自动推进、共创、局部精修按意图切换。新资料、隐私授权、明确规则与锁定偏好冲突时回到对应前置阶段，不重置全流程。

- **阶段0/4/6/7（照片和图片）**：`references/12-photo-and-evidence-media.md` 与 `references/19-chinese-formal-photo-design.md`、`templates/photo_policy.json`、`photo-policy-gallery.html`；**国内正式人类阅读版**有照片时，默认右上独立式，四款允许三栏式；创意版可保留居中/左栏人像，ATS始终无照片。只有用户已准许用途才插入照片，不能从用户中文或外貌推断地区。证据图依附真实经历，超过限额转附录。
- **阶段0/3/4/6（自适应与配色）**：`references/13-adaptive-design-and-personalization.md`；先匹配渠道和内容，再根据已知喜好选择结构；可独立定制配色，保留已有决定；栏目不固定，缺项不填空。
- **阶段4/6/7（图标）**：`references/14-icon-library-and-licensing.md`；正式开源地址、许可、语义、统一风格和 ATS 禁用规则。用户未选择时不强加。
- **阶段1–5/7（文案和独立审稿）**：`references/16-editorial-policy-and-review.md`；六段编译、逐层检查、实际子代理盲审/事实审/文案视觉审。无独立代理需记录 self-review-only。
- **任何阶段（异常和个性化）**：`references/17-personalization-edge-cases.md`；触发后再分支，不把问题清单发给所有用户。
- **理论与依据**：`references/18-personalization-research-db-standard-answer.md`；DBS 理论、案例、反例与适用条件，指南与工程规范明确分层。

## 8 个阶段与协作关口

| 阶段 | Agent 必须完成 | 用户需要做的事 | 输出与关口 |
|---|---|---|---|
| 0 目标与读者 | 理解用途、收件人、国家/行业、载体与投递路径；区分 ATS / 真人阅读 / 学术 CV / 作品集 | 修正意图与优先强调项；决定照片和私人信息披露范围 | `BRIEF.md`；用户确认**目的和范围** |
| 1 素材探勘 | 读取授权材料，按时间、角色、成果、奖项、作品、证据建库；标记来源与重复 | 自由叙述，给文件/链接，可略过私密材料 | `MASTER_INVENTORY.md`；先反馈发现，不强求填表 |
| 2 证据型访谈 | 围绕价值最高却不够具体的经历追问本人行动、困难、结果、意义、角色边界 | 回忆关键场景；指出哪些内容最像自己 | `INTERVIEW_NOTES.md`；按信息收益决定是否继续问 |
| 3 受众与个人叙事 | 形成2–3种候选个人定位、3项核心能力信号和优先经历 | **选择/否定/改写**定位与强调点 | `POSITIONING.md`；**战略审批关口** |
| 4 信息架构 | 给2种候选目录结构，解释前置/合并/拆分/删除、页数和桥接逻辑 | 选择结构、调整标题和次序；确认照片/特殊模块 | `OUTLINE.md`；**结构审批关口** |
| 5 文案编译 | 从素材→主张→证据→简历句，重写段落；关键经历给2种语气选项 | 挑选更自然、更打动目标读者的表达，补充遗漏 | `COPY_DRAFT.md` + 私有 `CLAIM_LEDGER`；**文案审批** |
| 6 视觉与排版 | 按场景推荐3种实际不同的结构（必要时含 ATS 基线）；先共用令牌对比，再混搭配色/字体/节奏；真实分页检查 | 选模板、反馈密度、层级、空白、照片、图标 | 可编辑稿 + PDF/HTML；**视觉审批** |
| 7 对抗审计与交付 | 逐句核查事实、贡献归属、阅读体验、格式和链接；依据反馈返工；输出两种用途版本 | 最终确认真实性、联系方式和可共享范围 | 正式成品、来源对照、修改记录；**交付审批** |

**关口不是强迫式问卷**：已经明确授权/决定则直接继承；用户说“先出草稿”可带暂定标签继续，但在公开发布、外部发送、覆盖文件、安装部署前仍须明确确认。不要擅自联网发布或上传含个人信息的文件。

## 必须调用的细则（按阶段渐进读取）

- **工作区状态与版本**：`templates/workspace_contract.md`。维持已知信息、审批记录与用户反馈，防止Agent在多轮后遗忘决定。
- **追问与访谈**：`references/01-interview-and-elicitation.md`。重点是从「我参加过」追到「我具体做出了什么」；从抽象形容词追到实例；控制提问成本。
- **真实素材与表达边界**：`references/02-evidence-and-privacy.md`。内部 claim ledger 的证据等级、共同作者、未完成项目和披露规则。
- **受众建模与内容编译**：`references/03-positioning-and-copy.md`。PAR 不是刻板句式；保留故事张力、语气与个人品质证据。
- **章节与行业适配**：`references/04-information-architecture.md`、`references/05-industry-adapters.md`。拒绝所有用户固定十栏；章节从信号和资料生长。
- **风格选择/视觉**：`references/06-design-and-style-selection.md`、`templates/themes.json`。12 个结构预设和独立配色/字体/节奏令牌；ATS 基线锁定中性单栏。
- **全局阅读规范（必读）**：`references/09-design-density-contract.md`。正文≥10.5pt、行高≥1.5；不提供高密度模式；溢出时调整内容/结构/分页，不缩字。
- **理论与构图**：`references/10-design-theory-and-benchmarks.md`、`references/11-structural-layout-patterns.md`、`templates/design_tokens.json`。以网格、排版、设计令牌与渠道规范解释结构差异；用户可以混搭并确认配置。
- **反馈重排/对抗测试**：`references/07-human-feedback-and-qa.md`。区分根因、复盘 human-vs-AI 的设计决策，测试修订副作用。
- **理论出处/边界**：`references/08-research-and-sources.md`。遵循 DBS 的命题审查→理论/标准→成功/失败/边界案例→条件性结论，不凭权威名字强贴理论。
- **案例**：`examples/case-retrospective.md`。匿名化呈现真实的多轮修订错误及处理；**不能把此案例套写成其他用户经历**。

## 对用户的默认交互节奏

1. 先给一段话，说明当前阶段、已知信息和缺失的关键决策；只在决定需要时问**零到两个**问题。
2. 必要阶段合并为一个决策包，给短小且可判断的交付，说明你推荐什么、为什么；让用户能直接回复「保留第2项，删第4项，调整第7项」。
3. 把用户每句反馈转成 `FEEDBACK_LOG`：原话→问题类别→本次修复→对全稿可能的连锁影响→是否验收。重复反馈应更新默认规则，不能每轮重犯。
4. 用户说「这个看不懂」「太挤」「不正式」时，先诊断**可观察问题**，不是问用户提供解决方案。通过对比、渲染、文本扫读提出修改。
5. 遇到「好看但 AI 味重」「先夸大再说」「让它完美一点」：提高表达质量、优先使用已发生的证据与可核查结果；不造假，不添加自我贬低说明。

## 通用质量门（禁止只凭自我感觉）

- **目标门**：20–30 秒扫读，陌生读者能回答“谁、投什么、最强的两项贡献、怎么证明”；该时间只是**内部启发式测试**，不是经过验证的人类阅读阈值。
- **真实性门**：所有可追问陈述在内部有来源或用户明确认可；个人/团队/AI协作贡献与阶段状态不误导；没有空造结果。
- **文字门**：删除无信息的品质形容词、内部代码变量与不必要缩写；核心贡献在前，专业词与读者水平匹配；连贯、不重复。
- **结构门**：章节标题清楚可概括，不用无端宣传口号；第二页延续同一份文件；高优先内容进入前部；个人定位与未来发展不重复。
- **视觉门**：执行密度契约，实际打印/渲染逐页检查行距、字距、断页、孤行、超链接、页脚距离、照片比例和对齐；不能用极小字号填满页面或头重脚轻。
- **机器门**：ATS 目标必须另提供单栏、无图标/照片/文本框的版本，并检查复制粘贴后的阅读顺序；不要宣称任何形式保证 ATS 通过。
- **隐私门**：对外稿只包含必要个人信息；不泄漏原始素材、证件号码、患者/同学资料、系统内部批注或秘密密钥。

## 随 Skill 可运行的视觉模板

主题清单见 `templates/themes.json`。可用 Python 3（仅标准库）生成独立 HTML：

```bash
python scripts/render_resume.py --input examples/sample_resume.json --theme book-editorial --palette ivory --font serif-head --rhythm airy --output example.html
python scripts/build_gallery.py --input examples/sample_resume.json --output style-gallery.html
python tests/test_skill_package.py
```

`build_gallery.py` 生成12个真实结构预览与离线混搭界面，用户可导出HTML/配置。`render_resume.py` 是HTML排版起点；有 Playwright、Chromium 和 PyMuPDF 时可运行 `scripts/export_pdf.py` 做实际打印与分页预检，结果有稀疏页警报时必须进一步修订。Word仍须独立生成、渲染核验。

## v1.2 可运行的个性化工具

```bash
python scripts/recommend_design.py --brief examples/sample_brief.json
python scripts/make_palette.py --seed '#E5AA40' --secondary '#2F7269' --output custom-palette.json
python scripts/render_resume.py --input examples/sample_resume.json --theme book-editorial --custom-palette custom-palette.json --output example.html
python scripts/import_asset.py photo.jpg --alt "本人照片" --approved --output photo-asset.json
python scripts/render_resume.py --input examples/sample_resume_media.json --theme formal-split --audience-profile cn-formal --output cn-formal-example.html
python scripts/render_resume.py --input examples/sample_resume_media.json --theme studio-grid --audience-profile cn-formal --photo-mode three-column --output cn-three-col-example.html
python scripts/render_resume.py --input examples/sample_resume_media.json --theme ivory-classic --audience-profile creative --output editorial-photo-example.html
python scripts/render_portfolio.py --input examples/sample_portfolio.json --output portfolio.html
python tests/test_personalization.py
python tests/test_photo_policy_v13.py --browser
```

`--approved` 仅在用户确实允许该素材用于本投递场景时使用。图片导入依赖 Pillow；原图片不修改，重编码移除元数据但不自动识别视觉敏感信息。可选 photo/media、multiple links 和 icon 的格式见12/14与 `examples/sample_resume_media.json`。12套结构、12配色、7字体、3节奏、原CLI继续兼容。自定义调色使用新JSON，旧预设不覆盖。模板路由器只提供候选，不能代替用户与Agent的实际读者判断。

## 最终交接文件

`MASTER_INVENTORY`（私有）、`CLAIM_LEDGER`（私有）、`POSITIONING`、`OUTLINE`、`COPY_DRAFT`、简历正式版（可编辑+阅读）、必要时 ATS 版、`FEEDBACK_LOG`、`CHANGELOG`、`personalization_contract`、`REVIEW_RECEIPTS`（私有，注明独立/自审状态）。仅**对外成品**交给目标读者；其余材料只给用户。

> 记住：用户不是数据填报员，是身份与价值的最终编辑。Agent 也不只是润色器，而是研究、编辑、排版和审查的执行者。
