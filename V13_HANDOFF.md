# Resume Narrative Studio v1.3｜头像布局审计整改交接

## 直接裁决

根据用户提供的12模板审评以及可核实的学校/设计指南，正式中文简历如需要照片，**身份区右上角独立式**作为默认；四款适合的现代版式另提供三栏。创意作品集可继续使用原有人物布局；ATS和无照简历保持无照片。

此结论仅限中国大陆、真人阅读、已明确需要/获准使用照片的场景。不是国际法定标准，也不意味着使用照片会增加录取概率。

## 本轮实际修改

1. 新增 `references/19-chinese-formal-photo-design.md`，说明理论来源、12款逐项裁决、失败例/反例及用户审批。
2. 新增 `templates/photo_policy.json`，对12主题保存原位置、正式评价等级与默认/可选方案。
3. 扩展 `scripts/personalization.py`，新增场景规则 `select_photo_mode` / `photo_recommendation`；修改 `recommend` 将面向国内学术/临床的有照正式简历优先推荐 `research-ledger`、`experience-index`、`formal-split`。
4. 升级 `scripts/render_resume.py`，正式版支持 `--audience-profile cn-formal`、`--photo-mode auto|header-right|three-column|editorial|none`。创意模式兼容v1.2原样式；绝对位置必须留出身份区空间。
5. 新增 `scripts/build_photo_policy_gallery.py` 和 `photo-policy-gallery.html`，用虚构图像生成真正的渲染对照；旧 `personalization-gallery.html` 增加场景说明与新页面入口。
6. `templates/personalization_contract.json` 增加照片语境、位置审批和锁定字段。
7. `tests/test_photo_policy_v13.py` 完成新规则、浏览器视觉几何、移动端和PDF烟雾测试。

## 用户可直接运行的示例

```bash
# 正式中文简历：已批准的照片自动放置于身份区右上
python scripts/render_resume.py --input examples/sample_resume_media.json --theme research-ledger --audience-profile cn-formal --output cn-formal.html

# 四款支持三栏头像布局
python scripts/render_resume.py --input examples/sample_resume_media.json --theme formal-split --audience-profile cn-formal --photo-mode three-column --output three-column.html

# 保留象牙书信的居中创意人物头像（用户自行选择用于作品集）
python scripts/render_resume.py --input examples/sample_resume_media.json --theme ivory-classic --audience-profile creative --output creative.html

# 无照片或用户明确拒绝照片
python scripts/render_resume.py --input examples/sample_resume_media.json --theme ivory-classic --photo-mode none --output no-photo.html

# 静态与浏览器回归
python tests/test_skill_package.py
python tests/test_personalization.py
python tests/test_photo_policy_v13.py --browser
```

## 本轮测试与发现的问题

- 12款主题策略与旧版创意模式、无头像回退、ATS无图、边栏宽度规则：全部静态通过。
- 浏览器实际执行15组有照模式（11款正式右上+4款三栏），桌面/移动端无横向溢出、无姓名与头像相交、图片加载成功、PDF仍含原始内容，均通过。
- 又执行15组长姓名、长头衔、超长邮箱、多条联系方式的增强几何检查，头像未覆盖姓名和联系信息。
- **实际发现并修复**：`bold-poster` 正式右上头像与标题区域重叠；`photo-mode=none` 仍错误生成图片。
- 没有验证真实头像照片效果、全部多页组合和跨平台DOCX，独立Agent审稿测试仍未运行。技术通过不代表美观一定被目标机构认可。

## 来源

- 湖南第一师范学院《2024届毕业生就业指南》：https://sim.hnfnu.edu.cn/info/1066/2622.htm
- NN/g 接近原则：https://www.nngroup.com/articles/gestalt-proximity/
- NN/g 视觉层级：https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
- UC San Diego Career Center 简历指导：https://career.ucsd.edu/resources/guides/resume.html
- Princeton Career Development 简历基本规范：https://careerdevelopment.princeton.edu/resume-guide/basic-principles-resume-writing

旧版本未被覆盖、删除或外部发布。本ZIP为可复制并由用户审核后安装的独立版本。
