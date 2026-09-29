---
name: regional-seo-opportunity-monitor
description: Discover regional Crypto and CEX SEO topics from local media, social channels and search evidence, deduplicate against previous issues, and produce concise matching Chinese and English Word briefs. Use for 区域SEO热点挖掘 or country-specific keyword monitoring, including Turkey and Azerbaijan; not a technical site audit or a generic crypto news feed.
---

# 区域 SEO 热点挖掘

将本地真实信号转为可评估的内容机会，不把报道量当搜索量。先读 [研究流程与证据](references/research.md)、[数据与交付](references/output.md)。

## 配置

复制 assets/tr.example.json 或 assets/az.example.json 及对应 sources 文件到用户工作目录。明确地区、时区、发现语言、对外内容语言和输出位置；新地区自行发现来源，不借用他国热度。示例默认对外英语、中英文各一份 Word；这是业务配置，不是法律结论。来源仅为待重核种子，既往可访问不代表本轮已读取。

## 执行

1. 冻结执行时刻，按每国时区计算上一完整自然周 [周一 00:00, 下周一 00:00)。读取本区历史 daily、reports、主题别名和来源库。一国失败不阻断另一国。
2. 检查本地媒体、Google Trends 地域信号以及经官网/可信互链核验的公开社媒。每日按来源 cadence 查核心入口；周报扩展来源并回补上周，回溯证据标为回溯，不伪造历史快照。
3. 保存原文、发布时间、抓取时间、地区依据和各类指标。媒体、社媒、本地语言搜索、本地英语需求与全球英语供给分开。未知/受限记录缺口，不写成无热点。
4. 按主题、同义词、译词及传播链去重。新词为本区首次监测发现，不等于本周首次出现；旧词最多一句，有真实事件阶段变化才列事件续篇，不计入新词。
5. 对有价值候选检查英语搜索意图、实际地域搜索结果、内容切口与业务承接。只有同一可比数据支持才写搜索增长；搜索待验证主题保持候选身份。
6. 从同一个事实数据集生成中英文精简 Word，按国家分章，每国候选五列表和至多三份短简报，不凑数。使用 assets/report-template.md 的结构，事实限定词和原文链接两版一致。
7. 在生成 Word 前运行 `python scripts/audit_report.py config.json report.json`，回读检查链接、日期和翻译，再渲染逐页检查。用文件工具在本区工作目录存档，不写进 skill 安装目录。

## 调度与交付

安装不建立自动任务。只有用户明确要求定时执行时，先查重再配置；示例为北京时间 15:00 开始，周一出周报。常规采集静默，只有失败、重大缺口、需用户处理或周报完成通知。默认仅在当前会话交付，不自动群发或发表文章。限制与覆盖缺口在交付消息中简短说明，不塞入精简 Word 正文，也不得删去影响事实真假的限定词。
