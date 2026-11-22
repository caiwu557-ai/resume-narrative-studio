# Resume Narrative Studio — 开源 Skill / Open Source

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

**Human-led, evidence-grounded resume writing and adaptive layout design.**

使用自然语言与已授权资料，完成事实整理、目标读者定位、分阶段访谈、简历文案编辑、12种版面结构以及排版审查；用户仍掌握个人定位、照片使用、事实判断与公开发布决策。

**Quick links:** [Interactive Design Lab](style-gallery.html) · [Photo Layout Comparison](photo-policy-gallery.html) · [Skill Guide](SKILL.md) · [License](LICENSE) · [Security](SECURITY.md) · [Contribution Guide](CONTRIBUTING.md)

> **重要**：本仓库中的示例人物、邮箱、作品均为虚构。不要提交真实用户的简历、证件、患者信息、私有仓库、授权受限图片或密钥。MIT 许可不自动授予第三方材料、商标和字体文件的权利。

## GitHub Pages（可选）

发布为公开仓库后，可在仓库 Settings → Pages 中选择 Deploy from a branch → `main` / `(root)`。站点首页是 `index.html`，无需构建工具。GitHub Pages 是否启用需要由仓库所有者自行核验；仓库公开不等于网站已经上线。

---

# Resume Narrative Studio v1.3.0 · Design Lab

在 v1.0 的八阶段共创工作流基础上，重构视觉子系统。保留访谈、事实审计、定位、内容编译、用户审批和反馈机制；不改变用户已有内容资产。

## 使用

- `SKILL.md`：Agent 入口；按阶段读取 references。
- `style-gallery.html`：离线打开，12套实际A4预览，实时选择布局/配色/字体/阅读节奏/纸张，导出HTML或JSON配置。
- `templates/design_tokens.json`：12个结构、12套配色、7组字体搭配、3个阅读节奏；取消高密度方案。
- `references/09-design-density-contract.md`：所有风格遵守的阅读密度、可读性及分页规则。
- `references/10-design-theory-and-benchmarks.md`：DBS理论与历史同构研究、来源与反例。
- `references/11-structural-layout-patterns.md`：布局与混搭决策，以及旧16个预设的合并、退役依据。
- `tests/`：自动结构检查、实际浏览器/PDF测试、历史Agent行为压力场景（需独立Agent实测）。

解压到目标 Agent 支持的私有 skill 工作区，或把整个目录交给能读附属文件的 Agent。**不自动安装与覆盖旧版**。用户信息只在其授权工作区流转。例：

> 使用 Resume Narrative Studio v1.3，先了解我要把简历给谁看，挖掘已有经历，帮我确认定位。到视觉阶段用三种互有区别的结构，不要先限制单页；按密度规范给我选择颜色、字体和留白。

## 无需安装即可预览

双击 `style-gallery.html`；可断网工作。所有预览资料为虚构数据。该文件不请求外部资源；不会上传数据。实际字体由设备决定。Gallery中的「灰度比较」帮助检查构图，但最终仍需真实纸本渲染。

## 代码使用

```bash
python scripts/render_resume.py --input examples/sample_resume.json --theme book-editorial --palette ivory --font serif-head --rhythm airy --page A4 --output demo.html
python scripts/build_gallery.py --input examples/sample_resume.json --output style-gallery.html
python tests/test_skill_package.py
```

可选安装浏览器/PDF测试依赖（须由用户自行按平台确认安装）：`playwright`、`PyMuPDF` 及 Chromium。使用已安装浏览器的路径：

```bash
python scripts/export_pdf.py --input examples/sample_resume.json --theme studio-grid --palette coral --font serif-head --rhythm large --output demo.pdf --chromium /path/to/chromium
python tests/test_rendering.py --out render-qa --chromium /path/to/chromium
```

Export生成PDF和 `.preflight.json`；自动测量多页稀疏警报并尝试以固定字号分组分页。若返回 `review-required` 则需要手工修订，不能声称通过。`preflight-ok` 也不等于最终视觉验收。`--no-reflow` 关闭自动重分组。自然语言用户可让Agent完成这些工作。

自有履历请另存私有JSON，不修改公开演示数据。`featured:true` / `placement:"support"` 只有用户批准后才放置；不能凭空制造结果或重点。未自动植入照片，图标库以引用与授权规范提供。

## 兼容边界

多页打印、任何字体回退、ATS、Word和HTML均须分别实际检验。12种默认预设并非12种录用效果理论；混搭支持所有角色合法的令牌，但未穷举所有组合及平台。已有行为压力场景未由独立Agent执行，详见 `VALIDATION_REPORT.md`。此生成器不替代证据核验或完整Word排版，也不保证ATS系统解析。

2026-11-21 · v1.3.0

## v1.2 个性化扩展

保留 v1.1 的12种版式及全部视觉令牌。新增12种照片适配（含ATS明确禁用）、多链接、精选证据图、单独作品附录、开放图标仓库目录、自定义角色调色与自然语言意图的结构化推荐。现有渲染器支持 `--custom-palette`；`import_asset.py` 需要 Pillow。新演示使用虚构几何资产，不包含真实人像。

- `personalization-gallery.html`：12种带头像/作品图的真实样例预览，含ATS图像自动省略对照。
- `references/12` 至 `18`：新增完整理论和执行协议，入口SKILL已接入。
- `tests/test_personalization.py` 与 `tests/results/personalization-results.json`：本次新能力实测。
- `tests/agent-pressure-scenarios.md`：交互压力案例，须用真实独立Agent运行，静态测试不能证明行为能力。

参阅 `SKILL.md` 的新命令。图像授权、真实事实、模板选择与独立审稿仍需Agent按协议执行，程序不会代替人类批准。

## v1.3 头像场景规范（新增）

- [v1.3 头像位置实际比较](photo-policy-gallery.html)；旧 `personalization-gallery.html` 保留v1.2的原创意照片构图并加入显著提示。

- 中国大陆**正式真人阅读**简历：在用户/收件方确定需要照片且已授权使用素材时，默认头像在**页眉右上**；`formal-split`、`studio-grid`、`product-feature`、`two-track` 可选三栏式。
- 创意作品集：保留原先各版式的居中、左栏、彩色人像布局。
- ATS：永远不放头像；没有照片时没有占位。身份地区通过用户申请场景明确，不通过中文、外貌推断。
- 12款裁决、引用和风险见 `references/19-chinese-formal-photo-design.md`；新规则和可用位置见 `templates/photo_policy.json`。
- 实际渲染测试 `python tests/test_photo_policy_v13.py --browser`。本增量旧版 v1.2 不被覆盖。
