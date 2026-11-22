# 14｜图标库、语义和授权清单

适用阶段4/6/7。正文文字已能识别栏目时，图标仅增强定位与风格；依据 W3C 装饰图规则 [P6]，不增加无必要读屏噪声。MIT ATS 指南 [P2] 提醒图形影响解析，因此机器版无图标。视觉版非必须；不要为了实现12个不同小标题就硬塞12个图标。

| 图标库 | 浏览 | 开源仓库及许可证 | 推荐使用 |
|---|---|---|---|
| Lucide | https://lucide.dev/icons | https://github.com/lucide-icons/lucide · https://lucide.dev/license（ISC，部分 Feather 派生图标 MIT） | 医学、学术、通用线性首选 |
| Tabler Icons | https://tabler.io/icons | https://github.com/tabler/tabler-icons · https://github.com/tabler/tabler-icons/blob/master/LICENSE（MIT） | 丰富专业细分主题，统一24单位网格/线性绘制 |
| Heroicons | https://heroicons.com | https://github.com/tailwindlabs/heroicons（MIT） | 通用界面与现代专业设计，少量标签图标 |
| Phosphor | https://phosphoricons.com | https://github.com/phosphor-icons/core · https://github.com/phosphor-icons/core/blob/main/LICENSE（MIT） | 年轻、创意、轻重不同风格；同稿只选一种线宽/重量 |

来源 P13–P16 已核对官方许可；版本变化时重新检查。开源许可不自动授权商标或第三方品牌。不要依赖图标 CDN、远程字体，也不要直接嵌入用户提供的未清理 SVG。需要官方图标时，取得实际指定版本原件，仅复制所需静态路径，保留许可与来源于交付附件；没有外部访问能力时使用安全的原创几何图标或纯文本，不能假称获取官方原件。对外简历不应为许可说明增加大块正文，可另保留 LICENSES。此包不捆绑上述第三方图标。

## 语义与风格
- 教育→毕业帽/书；科研→实验瓶/显微镜；临床→听诊器；工作→公文包；项目→模块/窗口；荣誉→奖项；服务→人群/爱心；技能→工具/列表；目标→标靶。具体库需核对图标名称是否存在。
- 每稿一个家族、同线重、同一尺寸（建议约1em–1.25em）、邻近标题、统一光学对齐，采用 accent 或正文色；不可用过细浅灰遮蔽文字。
- 章节统一策略：无图标、少量导航图标、或全部同层级章标题图标；用户已批准方案继承。不要随机混合实心、拟物、emoji 和线描。
- 实现：`sections[].icon` 允许 `education/research/work/award/portfolio/service/skills/target`，内嵌八种包内原创 SVG 字形，文字始终存在；用户未选则默认不显示。官方库由 Agent 在有权限时择取并做静态清理，当前脚本不自动下载官方图库。ATS 强制关闭。
