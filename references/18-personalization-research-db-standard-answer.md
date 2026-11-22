# 18｜DBS 理论研究与条件性标准答案 v1.2

研究问题：可变用户意图、事实内容及图像，如何在保有良好排版的同时，自适应地产生有说服力的简历？采用 dbs-standard-answer 的命题审查→理论映射→结构同构案例→条件性答案，并参考 dbs-theory-grounding。核查公开来源：2026-11-21。不是证明录取率的实验。以下均为概括/意译，非逐字引用。

## 1. 命题审查与理论地图
- “照片都应加”→收窄：身份归组只在照片合规且用户批准时成立，ATS 不适用。
- “好看配色就是好简历”→重构：色彩为角色和阅读服务，结构/对比度有保护线；文化语义不普适。
- “图片越多越丰富”→收窄：有意义、可读和可授权的图才增强证据；正文与作品集分离。
- “不问问题就低成本”→重构：只问会改变决策的必要问题，先检索并采用可逆默认；重大事实和权限不能跳过。
- “工整PAR模板可保证让人选中”→重构：目标相关、具体贡献与有形证据可增强辨识度；不机械套句、不保证录用。

| 理论/实践 | 作用机制 | 对应问题 | 落地 | 局限 |
|---|---|---|---|---|
| Gestalt接近/共同区域；Müller-Brockmann网格（10） | 相关元素靠近，构图对齐，分组降低寻找成本 | 1/3/5 | 头像在身份区，图随条目，证据附录 | 通用视觉理论，不证明某角落能提高录用率 |
| USWDS角色令牌＋W3C对比度 | 颜色与职责分离、确保可辨读 | 2/6 | 固定结构，语义颜色可切换，八对对比检测 | WCAG是网页标准，借作严格内部约束；非审美保证 |
| Oxford创意申请指南＋MIT/Harvard CV指南 | 依据机会筛选、以证据与个人贡献为核心，渠道分流 | 3/4/5/8 | 真实能力信号，选布局而非职业刻板印象，选材/附录/渠道 | 多样的机构要求覆盖默认值 |
| GOV.UK question protocol、Nielsen渐进披露/识别而非回忆 | 最少必要提问，先给可识别方案 | 4/7/9 | 先读资料，0–2高收益问题，决策锁和可撤销 | 不能把提问数最低作为唯一目标 |
| Amershi等 Guidelines for Human-AI Interaction (CHI 2019) | 合理期待、纠错、控制、随反馈适配 | 7/9 | 关键确认、局部修改、可逆版本、说明能力边界 | 不专门研究简历；实际交互质量待实测 |
| MIT PAR、Yale APR、Harvard写作规范 | 具体行动与结果，事实优先，读者可扫读 | 8 | 编译链、受众盲审、证据审、文案审 | 适用于经历表达，不强制学历/奖项/论文用同一公式 |

## 2. 结构同构与对照案例
结构指纹：个人手头丰富且异质的素材、不同阅读渠道、稀缺注意力与时间、统一视觉质量要求、需要保留自主控制。旧系统把所有信息或设计选择塞进固定模板，造成低相关文字、相似主题、提问负担和重新排版。可比机制为“分离稳定底层与可变模块”“按读者过滤证据”“先默认再暴露高级选项”。以下是有资料支持的设计实践或本案失败对照，不冒称测得招聘效果。

| 对照实践/案例 | 同构机制与可迁移做法 | 不同处与边界 |
|---|---|---|
| USWDS 角色化主题令牌 | 同一组件使用角色色，可定制且一致；转译为布局与配色解耦、可验证色对比 | 网站设计不是纸质简历，60/30/10等比例不能照搬 |
| Oxford 创意CV与独立作品集实践 | 主文档承担资历，精选作品提供外部证据；不同岗位适用不同形式 | 并无统一作品数量；作品集场景不能替代ATS |
| GOV.UK问答协议与NN/g渐进披露 | 先决定信息用途，减少重复输入及高级选项负担 | 行政表单更固定，个人经历访谈还需开放提问和用户回忆 |
| 本案v0.3→v0.6 失败与修复（见 REVIEW/案例） | 堆术语、QA缺点、无关样本量与不连贯分页，经真实用户反馈重编译；书卷编辑等获认可 | 单个用户体验证据，不等同独立导师评价 |
| 美国ATS/Harvard普通CV vs 德国官方就业指南 | 照片和装饰在不同渠道有不同利益/风险；规则先于预设 | 并非所有美国/德国岗位都要求同样文档，实际公告优先 |
| 本案v1.1 风格定制 | 统一灰度令牌下比较构图；内容多调分页不降低字号 | 新增图片会改变版面，原测试不保证新组合，必须重验 |

结论等级：**条件性答案**。在读者需求明确、事实可追溯且允许可逆修改时，稳定的排版契约、分离的设计令牌、与事实相邻的证据图、少量高价值追问与人类审核能解决此类异质信息的组织问题。实际招聘强制模板、极端篇幅、未知授权或关键证据缺失时必须分流/停在待确认，不存在可保证“就是他了”的公式。未做独立用户录用结果研究。

## 3. 官方来源索引
- P1 Harvard College Guide to Creating a Strong Resume — https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/ （照片、易扫读、清晰事实）
- P2 MIT CAPD ATS — https://capd.mit.edu/resources/make-your-resume-ats-friendly/
- P3 Bundesagentur für Arbeit, 2026 CV guidance — https://www.arbeitsagentur.de/vor-ort/zav/working-and-living-in-germany/iss-en/issue-01-2026/application-cv （德国照片非强制；顶部或封页）
- P4 Aurora Harley, NN/g, Proximity Principle in Visual Design (2020) — https://www.nngroup.com/articles/gestalt-proximity/
- P5 Oxford University, Creative portfolios, CVs, and applications — https://www.ox.ac.uk/careers/careers-guidance/job-search-and-applications/writing-applications/creative-portfolios-cvs-and-applications
- P6 W3C WAI Decorative Images — https://www.w3.org/WAI/tutorials/images/decorative/ （有意义图片不能无等效文字；装饰图可空alt）
- P7 US Web Design System, Theme color tokens — https://designsystem.digital.gov/design-tokens/color/theme-tokens/
- P8 W3C WCAG 1.4.3 — https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
- P9 GOV.UK question pages — https://design-system.service.gov.uk/patterns/question-pages/ ; question protocol — https://www.gov.uk/service-manual/design/form-structure
- P10 NN/g Progressive Disclosure — https://www.nngroup.com/articles/progressive-disclosure/
- P11 Jakob Nielsen, 10 Usability Heuristics — https://www.nngroup.com/articles/ten-usability-heuristics/
- P12 Saleema Amershi et al., Guidelines for Human-AI Interaction (CHI 2019), DOI 10.1145/3290605.3300233 — https://www.microsoft.com/en-us/research/project/guidelines-for-human-ai-interaction/
- P13 Lucide official license — https://lucide.dev/license
- P14 Tabler Icons MIT — https://github.com/tabler/tabler-icons/blob/master/LICENSE
- P15 Heroicons — https://github.com/tailwindlabs/heroicons
- P16 Phosphor Icons MIT — https://github.com/phosphor-icons/core/blob/main/LICENSE
- P17 MIT CAPD, Resumes — https://capd.mit.edu/resources/resumes/
- P18 MIT CAPD, Career toolkit; PAR — https://capd.mit.edu/resources/career-toolkit-crafting-an-effective-resume/
- P19 Yale OCS, Writing Impactful Resume Bullets — https://ocs.yale.edu/resources/writing-impactful-resume-bullets/
- P20 MIT CAPD, Using AI for your resume and CV — https://capd.mit.edu/resources/using-ai-for-your-resume-and-cv/ （PAR非每条必需，审查重复）
- P21 Harvard HES, impactful resumes — https://careerservices.fas.harvard.edu/resources/hes-create-impactful-resumes-and-cover-letters/ （岗位相关性与直截了当的事实表达）
