# 08｜DBS 标准答案研究记录与适用边界

研究时间：2026-11-21。研究范围：简历/CV、医学学生CV、内容扫读、ATS以及开源图标许可。**不是对任何简历能否获得录取/面试的效果保证。**

## 研究命题

“怎样把未经整理的人类经历，通过多轮人机协作，转成专业、真实、有吸引力的简历？”

分解为：①读者要识别什么；②哪类经历能证明；③怎样组织文章提高扫读；④何时视觉设计有帮助/有害；⑤怎样让人类批评改变 AI 的策略。

## 主方法：面向读者的事实选择与表达

- MIT CAPD：项目/经历以 action → task → result/outcome 编写，并按投递目标确定关键词与内容；实践指标有帮助但必须有意义。
  https://capd.mit.edu/resources/resumes-writing-about-your-skills/
  https://capd.mit.edu/resources/career-toolkit-crafting-an-effective-resume/
- Yale OCS：以 Action + Project + Result 表达经历，重视具体贡献。
  https://ocs.yale.edu/resources/writing-impactful-resume-bullets/
- Harvard MCS：简历应易读、可扫读、有适当留白并按相关性选择信息；学术CV可以更长、结构更丰富。
  https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/
  https://careerservices.fas.harvard.edu/resources/gsas-cv-cover-letter-guide-2/
- Oxford Careers：学术与非学术CV在内容和篇幅不同，研究、教学、资助与服务要围绕申请领域组织。
  https://www.ox.ac.uk/careers/careers-guidance/job-search-and-applications/writing-applications/cvs
- AAMC（医学生 CV）：持续累积资历、科研、志愿经历和学术活动，随职业阶段更新，而不是临时凑项目。
  https://higherlogicdownload.s3.amazonaws.com/AAMCCOMM/5e803c51-f7b9-497e-8e2f-24e62f0fe952/UploadedImages/Building_a_Strong_Curriculum_Vitae.pdf

## 辅助机制：可扫读与版式分流

- Nielsen Norman Group 提倡简洁、意义明确的标题、简明段落和可扫读信息结构；此处引用网站信息设计研究作为辅助，**不能把它当成专门的简历录用率试验**。
  https://www.nngroup.com/articles/be-succinct-writing-for-the-web/
  https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/
- MIT 关于 ATS 的具体提醒：文本框、图像、复杂表格/花式排版可能妨碍解析；建议检查从简历复制到纯文本后的顺序。
  https://capd.mit.edu/resources/make-your-resume-ats-friendly/
- Broad Institute（MIT/Harvard）强调相关经历优先、标题顺序和留白。
  https://mitcommlab.mit.edu/broad/commkit/cvresume/
- 照片的要求有地域和岗位差异，默认不要求照片，先问地域/制度。
  https://career.ucla.edu/resources/resumes-cover-letters/
  https://studies.helsinki.fi/instructions/article/tips-job-search

## 历史与反例：我们实际经历的共创版本

1. **失败机制 A（项目报告式简历）**：早期版本努力保留所有审计、科研细节和产品限制，结果用户认为生硬、缺少吸引力。原因：原料层与投递层混淆。
2. **修复机制 B（叙事重组）**：依据 MIT/Yale 等的价值—行动—成果原则，调整内容后获得更高的用户认同；但这只是个体共创反馈，**没有独立面试成功率数据**。
3. **失败机制 C（视觉分裂）**：两页文档使用独立封面式标题、上紧下松，使人感到不正式；用户纠正后才通过统一续页、章节和留白改善。
4. **边界反例 D（ATS）**：图标/复杂多栏对真人可能有视觉价值，对自动筛选系统可能降低解析稳定性，因此“更美观”不能无条件最大化。
5. **边界反例 E（科研细节）**：初次给非专业导师不宜堆叠内部字段，但申请方法学岗位/正式论文CV时科研技术细节或论文清单是正当主要内容；不能一律“去技术化”。

## 条件性标准答案

**当读者有明确筛选目标且注意力有限时**，以完整素材库为底，先选择3条可信能力信号，再由贡献和结果生成文案，并在真人版/ATS版间分流视觉策略；人类在定位、架构、关键文案、最终视觉四处进行决策。这个过程可减少用户案例中反复出现的叙事和排版失误。

**失效条件**：严重缺少真实经历、材料存在不可化解的冲突、用户要求虚构经历、投递方有强制模板、文档系统格式限制、专业/国家惯例不同。

**证据强度**：来自职业中心的规范建议 + 一个真实迭代案例；没有对多用户录用结果的因果研究。它是可审查的**行业实践型流程规范**，不是已验证的招聘效能模型。

## 开源图标来源

- Lucide（ISC/个别MIT）：https://lucide.dev/license
- Tabler（MIT）：https://github.com/tabler/tabler-icons
- Heroicons（MIT）：https://github.com/tailwindlabs/heroicons

## 本地静态生成工具的边界

包中的示例 HTML 渲染器仅负责内容/排版映射；不做事实核查、网页信息采集或复杂 DOCX 编辑。不能因脚本能出16个主题便宣布每个模板都通过了真实字体和页面适配测试。
