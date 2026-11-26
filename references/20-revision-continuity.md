# 20｜跨版本约束回归（v1.4 必须执行）

## 何时运行
每次新建或修改简历均运行；旧稿重启、局部改词、换模板、单页压缩尤其容易回退。既有 FEEDBACK_LOG 保存反馈历史，revision_state 保存当前有效的验收规则，两者不可互相替代。

1. 获取真实最新原件、确认的版本与历史反馈，先备份至新版本路径。不可访问的本地目录仅记为缺口；不得声称已打开。对反馈存在歧义的规则标 tentative，而非假称 locked。
2. 生成 prior snapshot（上轮已确认状态）和本轮 change set。每条规则使用稳定 ID、scope、rule、status、source、check_method、target_artifact。来源指向用户原话/明确确认的位置。区分事实、必要信息、章节归属、标点换行、强调语义、版面及交付格式。区分用户锁定与 Agent 自选方案，不能把后一项伪装为用户决策。
3. 将改动划分为「本轮改变」「必须保留」「潜在牵连」「待核」。局部编辑默认只触及前者；全局重构先锁定事实、照片、联系方式、链接及结构性约束。若同一范围的新明确决定与旧规则直接冲突，记录 before/after 和授权，明确 supersede；不涉及该范围的旧要求不得被自动解除。退役保留历史行，状态为 retired。
4. 在实际成品上复查**每条当前 locked 规则**，记录 PASS/FAIL/NOT_RUN 及证据（版本、页码、位置、正文摘录、实际链接目标、测量结果或视觉检查记录）。NA 仅用于不适用的非锁定检查；若锁定规则确实不再适用，必须先按授权退役。不得复用旧文件的通过凭据作为新版验收。
5. 运行校验（仅标准库）：

```bash
python scripts/revision_contract.py --previous prior.json --current current.json --changes changes.json --receipts receipts.json
```

模板见 `templates/revision_state.json`。changes 和 receipts 为独立 JSON 数组。两份快照使用相同 job_id，current.source_version 对应 prior.candidate_version，current.candidate_version 必须是新版标识；receipts 的 artifact_version 必须等于 current.candidate_version，并明确 reviewer。首次创建 prior 的 constraints 为空；不要伪造原版约束。脚本检查结构连续性、显式变化和记录的完整性，不验证用户授权是否真实，也不验证截图与文本是否符合规则；人工审稿仍必需。若失败，修复并再次检查全稿。无本地存储则在对话保留同等状态、诚实标注未运行工具。

## 必须捕获的典型回退

- 合并栏目后丢失独立经历、角色、奖项或正式题名。
- 减少加粗时只剩“任职/荣誉”泛标签，事实失去强调；同级角色/奖项强调不一致。
- 修正字距时重写段落导致超链接、run、照片或已批准的换行丢失。
- 一页目标掩盖小字号与关键事实删减；不得将“成功打印一页”等同于验收。
- 旧项目材料只读到 README，却把最新功能、独立开发、发布状态写成已核。

## 交付关口
同时满足：原始证据支持；目标读者排序成立；每项锁定约束有新版证据；实际输出文件存在、渲染全部页且核验内容/链接/隐私；独立审稿状态如实标注。用户最终确认、技术验收、发布授权分别记录，不能互相替代。只交付已请求的载体；未申请附页、作品集、ATS 或 HTML 时不擅自扩张。需要例外时，给用户明确取舍，未获授权可交草稿，不能称正式通过。
