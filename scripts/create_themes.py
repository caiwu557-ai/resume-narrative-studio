#!/usr/bin/env python3
"""Author original structural presets and independently selectable visual tokens."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
# Names describe content geometry, not industry or superficial color variants.
layouts=[
('ats-clean','01 · 清晰单栏','machine','plain','paper','neutral','balanced','标准电子投递；单栏自然阅读顺序、无装饰。','ATS / 正式招聘'),
('formal-split','02 · 横向身份区','professional','formal','navy','neutral','balanced','姓名与联系信息左右分置，主体整栏。','医疗 / 商务 / 导师'),
('research-ledger','03 · 学术索引','professional','ledger','forest','serif-head','balanced','章节名作为左侧索引，经历集中在右侧宽栏。','科研 / 高校 / 正式档案'),
('ivory-classic','04 · 象牙书信','editorial','ivory','ivory','serif','airy','居中姓名与分隔线，正文单栏，适合重视礼仪的阅读。','学术 / 人文 / 教育'),
('book-editorial','05 · 书卷编辑','editorial','book','copper','serif-head','balanced','大字号衬线姓名与右侧短简介，主体如书籍章节。','编辑 / 人文 / 学术'),
('studio-grid','06 · 工作室网格','editorial','studio','ink','modern','balanced','模块网格：较长经历跨栏，紧凑材料并排而不强行等长。','设计 / 建筑 / 作品'),
('product-feature','07 · 核心作品','portfolio','product','teal','modern','balanced','将经用户确认的核心项目置入跨栏重点区，其他履历保持连续。','产品 / 工程 / 创业'),
('portfolio-rail','08 · 作品集侧栏','portfolio','rail','plum','serif-head','balanced','左栏承载身份与联系方式，右侧是完整的经历主线。','创作者 / 独立顾问'),
('experience-index','09 · 经历索引','professional','index','steel','neutral','balanced','每条经历的日期或角色置于独立窄栏，便于比较；不假定时间顺序。','多段任职 / 项目履历'),
('bold-poster','10 · 大字海报','creative','poster','cobalt','display','balanced','大字姓名与高对比色块形成强入口，正文仍为标准单栏。','视觉传达 / 创意岗位'),
('pop-blocks','11 · 青年拼贴','creative','pop','coral','modern','balanced','有节奏的标签与横向色带，紧凑模块成对，较长经历跨栏。','新媒体 / 创意 / 年轻团队'),
('two-track','12 · 双轨档案','professional','tracks','butter','serif-head','balanced','页首统一身份；证据主轨与经批准的支持信息侧轨分开。','研究 / 产品 / 跨领域'),
]
# Semantic roles: ink for body, muted for secondary, accent for links/labels, band foreground/background, light surface, bright feature.
# All text on a given role must satisfy contrast checks; colors used in decoration alone are unrestricted.
palettes={
'paper':('黑白纸本','#FFFFFF','#17202B','#4E5764','#25364A','#E9EDF1','#142332','#FFFFFF','#E4E8EC','#17202B','#C4CBD2'),
'navy':('墨海蓝','#FFFFFF','#192638','#4C5C6D','#245483','#E9F0F7','#18324B','#FFFFFF','#BDD6F1','#172F4B','#BECAD6'),
'forest':('松柏绿','#F9FBF8','#1C302A','#52625A','#27614C','#E3EEE7','#203F35','#FFFFFF','#CDE2CB','#203B2C','#BCCFC1'),
'ivory':('象牙墨','#FFFCF4','#2C2823','#61584F','#795134','#F2E6D1','#3F3028','#FFFFFF','#E4C99E','#38271D','#D6C3A7'),
'copper':('陶土书页','#FFFCF8','#302923','#645A52','#8A442F','#F6E6DB','#572F25','#FFFFFF','#F1C7AB','#492B23','#DCC1B1'),
'ink':('雾白与炭黑','#FFFFFF','#1C2428','#536168','#3A4B56','#EEF1F0','#182529','#FFFFFF','#D3DEDD','#182529','#C0CCCB'),
 'teal':('孔雀青','#FBFEFD','#193039','#486169','#136466','#E0F1EF','#143F46','#FFFFFF','#B9E8DD','#153A3C','#B5D4D1'),
'plum':('墨紫','#FDFBFF','#2F263C','#64566C','#71436D','#EEE6F4','#3C294A','#FFFFFF','#E4C8ED','#372340','#D6C7DF'),
'steel':('钢蓝灰','#FFFFFF','#24313D','#536171','#405B77','#E7ECF2','#263D52','#FFFFFF','#CBD9E7','#263D52','#C1CBD7'),
'cobalt':('电光钴蓝','#FFFFFF','#202A40','#4E596D','#2749AB','#E5ECFF','#1E3689','#FFFFFF','#C6FF57','#182B39','#C6CFE6'),
'coral':('珊瑚与莓紫','#FFF9F6','#302335','#635466','#9B382C','#FFE5D9','#482D56','#FFFFFF','#FF9B7F','#41233A','#D8C3CD'),
'butter':('奶油黄与墨绿','#FFFDF6','#25332D','#556359','#47623B','#F0EDD6','#254138','#FFFFFF','#F4DC77','#25332D','#D2CDB4'),
}
keys=['title','paper','ink','muted','accent','panel','band','band_ink','highlight','highlight_ink','line']
palettes={k:dict(zip(keys,v)) for k,v in palettes.items()}
fonts={
'neutral':{'title':'现代无衬线','body':"'Noto Sans CJK SC','Microsoft YaHei','PingFang SC',Arial,sans-serif",'heading':"'Noto Sans CJK SC','Microsoft YaHei','PingFang SC',Arial,sans-serif",'weight':700},
'serif-head':{'title':'宋体标题 · 黑体正文','body':"'Noto Sans CJK SC','Microsoft YaHei','PingFang SC',sans-serif",'heading':"'Noto Serif CJK SC','Songti SC','SimSun',Georgia,serif",'weight':700},
'serif':{'title':'经典衬线','body':"'Noto Serif CJK SC','Songti SC','SimSun',Georgia,serif",'heading':"'Noto Serif CJK SC','Songti SC','SimSun',Georgia,serif",'weight':700},
'modern':{'title':'人文无衬线 · Lato/Noto','body':"Lato,'Noto Sans CJK SC','Microsoft YaHei',sans-serif",'heading':"Lato,'Noto Sans CJK SC','Microsoft YaHei',sans-serif",'weight':800},
'display':{'title':'粗体展示 · 黑体正文','body':"'Noto Sans CJK SC','Microsoft YaHei',Arial,sans-serif",'heading':"'DejaVu Sans','Noto Sans CJK SC','Microsoft YaHei',sans-serif",'weight':900},
'kai-head':{'title':'楷体题名 · 黑体正文','body':"'Noto Sans CJK SC','Microsoft YaHei',sans-serif",'heading':"'AR PL KaitiM GB','Kaiti SC','KaiTi','Noto Serif CJK SC',serif",'weight':700},
'western-serif':{'title':'西文衬线 · 中文宋体','body':"'Liberation Serif','Noto Serif CJK SC','Songti SC',Georgia,serif",'heading':"'Liberation Serif','Noto Serif CJK SC','Songti SC',Georgia,serif",'weight':700},
}
# These are local engineering guardrails, not measured universal optimums. No high-density mode.
rhythms={
'balanced':{'title':'舒展标准','body_pt':10.5,'line_height':1.55,'heading_pt':13,'section_gap_pt':16,'entry_gap_pt':8,'title_gap_pt':5,'bullet_gap_pt':2.8,'gutter_mm':7,'margin_mm':17},
'airy':{'title':'更多呼吸感','body_pt':11,'line_height':1.65,'heading_pt':14,'section_gap_pt':18,'entry_gap_pt':9,'title_gap_pt':6,'bullet_gap_pt':3.5,'gutter_mm':8,'margin_mm':18},
'large':{'title':'大字易读','body_pt':12,'line_height':1.6,'heading_pt':15,'section_gap_pt':18,'entry_gap_pt':9,'title_gap_pt':6,'bullet_gap_pt':3.5,'gutter_mm':8,'margin_mm':18},
}
styles=[dict(zip(['id','title','family','layout','palette_id','font_id','rhythm_id','description','recommended_for'],a),ats_candidate=a[0]=='ats-clean',ats_safe=a[0]=='ats-clean') for a in layouts]
manifest={'version':'1.1.0','palettes':palettes,'fonts':fonts,'rhythms':rhythms,'layouts':styles,'allowed_page_sizes':['A4','Letter'],'machine':{'layout':'plain','palette_id':'paper','font_id':'neutral','allowed_rhythm':['balanced','airy','large']}}
(ROOT/'templates/design_tokens.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'templates/themes.json').write_text(json.dumps(styles,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(styles),'structural presets',len(palettes),'palettes',len(fonts),'font systems',len(rhythms),'rhythms')
