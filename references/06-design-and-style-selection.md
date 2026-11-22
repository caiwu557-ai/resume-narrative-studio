# 06｜视觉设计与可混搭风格选择（v1.1）

**先读全局密度合同 `09-design-density-contract.md`，然后读 `11-structural-layout-patterns.md`；要查理论依据读 `10-design-theory-and-benchmarks.md`。** 所有布局都受同一质量规范约束，不允许以风格为由缩小正文或压缩间距。

## 场景优先

- ATS：`ats-clean`，单栏、清晰标题、自然顺序、无图标/照片/表格/文本框。按招聘系统规定导出 Word/PDF 并用纯文本复核。该预设锁定中性配色和通用字体；不承诺实际系统通过。
- 正式专业：`formal-split`、`research-ledger`、`experience-index`、`ivory-classic`。按读者扫读或深入阅读需求，选择章节索引、行内经历索引或常规单栏。
- 编辑式、人文、学术作品：`book-editorial`、`ivory-classic`。适当使用衬线标题、页首留白和比例控制。
- 项目/设计/数字作品：`studio-grid`、`product-feature`、`portfolio-rail`、`two-track`。从等宽模块、重点项目、身份栏、支持信息栏中选择，而非因“设计岗”选鲜艳色。
- 年轻/创意：`bold-poster`、`pop-blocks`。大字、色带、非对称配色允许更有辨识度，仍保留标准正文。若需机器投递再做清晰单栏。

## 操作流程

1. 已确认的内容架构是输入。向用户呈现3个真正不同的结构，解释适用项和限制。用中性令牌比较，别以配色变化充当差异。
2. `templates/design_tokens.json` 中选择布局、12组配色、7组字体、3种阅读节奏、A4/Letter。样式是语义角色、字体配对和结构，不是任意RGB、字号或高密度调参。`templates/themes.json` 是预设索引。
3. 若用户要混搭，打开可离线运行的 `style-gallery.html`；或用其批准的 JSON 重新运行 `scripts/build_gallery.py`。通过该界面设定、预览并导出 HTML / 配置。配置可交给 Agent 重现。字体实际可用性取决于系统，需检查回退和换行；不分发字体文件。
4. 按内容需要选择是否突出核心项目 `featured:true`，或将指定支持信息置入 `placement:"support"`（必须用户批准）。网格必须避免落单半行；长履历允许变为连续正文及增加页数。
5. 导出真实 PDF 并查看逐页结果。可选 `scripts/export_pdf.py` 做分页预检、尝试重排；若警报未消除，先修正而不是标成正式稿。所有字号、行距、段距仍遵守 09。
6. 视觉审批：让用户确认最像自身定位的设计，保持其批准结构/颜色/字体等记录。改版后整页复核，不只改局部。

## 图标、照片、字体授权

- Lucide：<https://lucide.dev/icons>；许可：<https://lucide.dev/license>（ISC，部分图标来自 MIT 许可 Feather）。
- Tabler Icons：<https://tabler.io/icons>；许可见 <https://github.com/tabler/tabler-icons>（MIT）。
- Heroicons：<https://heroicons.com/>；许可见 <https://github.com/tailwindlabs/heroicons>（MIT）。
- 开源字体候选：Noto Sans CJK / Noto Serif CJK（官方仓库 <https://github.com/notofonts/noto-cjk>）；Lato（<https://www.latofonts.com/>）；选取前核实当前发行许可和语言覆盖，不随 Skill 打包字体文件。可用系统字体及合规回退。
- 本版本预设不强制图标；用户选时只能辅助标题，不能取代信息。统一线宽、大小、对齐；保留适用许可证与来源。照片仅在目的、地区/机构要求及本人明确偏好下添加；不要求提供头像，不从照片推断敏感身份。现有 HTML 生成器不自动植入肖像，需 Agent 在获得授权后单独制作并渲染。
- 切勿复制商业模板、品牌图标或无授权字体。用户照片和真实简历保留在私有工作区。

## v1.2 扩展
照片与图像的真实位置/批准/附录遵循12，配色的独立定制与自适应遵循13，图标政策遵循14，遇旧规则冲突以09及12–14的更新规则为准。
