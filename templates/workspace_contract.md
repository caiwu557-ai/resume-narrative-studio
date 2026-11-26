# 工作区状态与交付物契约（Agent执行用）

此契约解决“每次重新开始都遗忘用户已确认决定”的问题。可只在当前对话中维护；有文件能力时存入**用户私有且已授权**的工作区。禁止未经授权同步到公开仓库。

## 建议工作区

```text
resume-workspace/
  private/
    MASTER_INVENTORY.md       # 原始素材汇总与出处；不发给收件人
    CLAIM_LEDGER.csv          # 每条对外事实的来源、贡献归属、核验状态
    INTERVIEW_NOTES.md        # 只记录与任务有关的访谈
    FEEDBACK_LOG.md           # 用户反馈，含已确认决定
  editorial/
    BRIEF.md                  # 收件人、场景、风格、照片与隐私边界
    POSITIONING.md            # 定位候选与用户选择
    OUTLINE.md                # 章节提纲、排序、页数和通过的关口
    COPY_DRAFT.md             # 用户可审的文案
    CHANGELOG.md              # 各轮做了什么、为什么
  delivery/
    resume-v01.docx           # 可编辑版本（若系统支持）
    resume-v01.pdf            # 阅读版（若系统支持）
    resume-ats-v01.docx       # 当ATS投递需要时
    portfolio-v01.html        # 当作品集需要时
```

示意文件名不是要求所有用户必须生成十个文件。无持久存储时，可在对话末输出简要续接状态与待确认事项；不要幻想已有后台文件。

## 审批与版本门

```text
stage_id: 0..7
brief_confirmed: true|false
positioning_confirmed: true|false
outline_confirmed: true|false
copy_confirmed: true|false
visual_confirmed: true|false
final_user_approved: true|false
external_publish_approved: true|false
current_version: v0.1...
```

不要将“用户无异议”自动解释为批准公开发布。内部工作文件可自行更新已授权的新版本；若涉及覆盖、公开、安装或发送外部收件人，需要独立明确许可。

## BRIEF 摘要格式（尽可能控制在一页）

- 用户当前身份与资料来源（不得偷带其他客户的内容）：
- 目标读者/机会/所在国或学院：
- 阅读/投递渠道（真人/ATS/学术CV/作品集）：
- 读者需要判断的三件事：
- 用户希望强调的三件事：
- 用户明确不希望的表达方式/视觉元素：
- 优先证明的作品或经历：
- 是否附照片与依据：
- 是否可公开作品链接：
- 隐私处理规则：
- 预计页数与需要的输出格式：
- 用户确认与待确认：

## CLAIM_LEDGER CSV 推荐列

```csv
claim_id,claim_text,source_ref,source_type,contribution,scope,status,target_section,editor_note
C001,示例事实,source://example,D,本人,完整项目,verified,研究经历,仅内部核查
```

优先用 `source_ref` 指向可查文件、原件页码/链接或用户访谈轮次；不能伪造 `D` 级来源。此 CSV 的样例内容是虚构的，不代表真实用户。

## FEEDBACK_LOG 要包含对方法的修正

```text
版本 v0.x
用户原话：
发现症状：
根因类别（目标/结构/文案/事实/视觉/链接）：
本次修复：
牵连变更：
反向审计结果：
用户是否验收：
下一次必须避免：
```

这使“AI以后不要再犯”转化为**可执行、可检查的制作约束**，而不仅仅是长篇复盘感想。

## v1.2 持续状态扩展
`personalization_contract.json` 记录受众、语言、渠道、素材授权、锁定范围、用户委托和审核状态；每个问题须记录能改变哪项交付。保存并沿用用户批准的 `approved_design`；不得因颜色或图片反馈重置结构。`REVIEW_RECEIPTS` 记录实际独立子代理审稿凭据或 self-review-only 降级。


## v1.4 回归状态
按 `references/20-revision-continuity.md` 保存 `revision_state`（前后快照、变更授权、验收凭据）、`emphasis map` 与 `delivery-audit`。原始事实记录补充 source_kind、inspection_scope、stage、conflicts、next_verification。不要将 FEEDBACK_LOG 当当前有效规则清单。
