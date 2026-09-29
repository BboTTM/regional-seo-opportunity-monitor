# 数据和双语交付

配置以 assets 下示例为准。stateDir、sourceFile 相对配置文件解析；运行数据保存在 stateDir/region.id，国家间不共享主题计数。周报开始前调用 scripts/audit_report.py 的 week_window(config, aware_datetime) 可得到本地时区上一完整自然周边界；周一之后新发布的前瞻不混入上周。

daily/YYYY-MM-DD.json 保存 region_id、fetched_at、coverage、queries、observations。每条 observation 保存稳定 id（原文 URL/帖子 ID）、topic_id、原词、中文含义、source_url、source_owner、published_at、fetched_at、event_at、locale_evidence、summary、signal_type、metrics（值/单位/窗口）、evidence_status、limitation。重跑按稳定 ID 更新并保留历史观察，原始证据另存本区 evidence；写入先临时文件再原子替换。

周报在同一个 report.json 内维护：

```json
{
  "region_id": "tr",
  "history_topic_ids": [],
  "topics": [{
    "topic_id": "example-topic",
    "kind": "new",
    "source_urls": ["https://example.org/source"],
    "evidence_status": "candidate",
    "facts": {"published_at": "2026-09-27T12:00:00+03:00", "metrics": []},
    "zh": {"topic_id": "example-topic", "evidence_status": "candidate", "facts": {"published_at": "2026-09-27T12:00:00+03:00", "metrics": []}, "local_term": "原词", "meaning": "中文含义", "target_keywords": ["English keyword"], "headline": "English proposed headline", "summary": "候选摘要"},
    "en": {"topic_id": "example-topic", "evidence_status": "candidate", "facts": {"published_at": "2026-09-27T12:00:00+03:00", "metrics": []}, "local_term": "原词", "meaning": "English meaning", "target_keywords": ["English keyword"], "headline": "English proposed headline", "summary": "Candidate summary"}
  }]
}
```

kind 为 new、old、continuation、watch。已有历史 ID 不得标 new；continuation 另需 previous_stage、stage、new_evidence_urls，必须属于历史主题且阶段不同。facts 是两版共享的机器可比事实块，不能在翻译时改变；原文链接和选题状态共享。脚本只检查结构和一致性，不替代阅读原文、语义去重或翻译审校。

报告模板见 assets/report-template.md。中英文均按国家分章，使用同一主题集合、排序、数字、证据状态和来源。正文每国只保留国家/期号/日期、统计窗口和简短采集说明、本周值得做什么、五列候选表，以及至多三份短简报。候选表列顺序、原词及含义→英语目标词、类型（热门 FAQ/热点关键词/事件续篇）、本地关联与证据类别、内容简介与热点时间。简报保留新增事实、意图、必要英语关键词/标题/H2/读者问题、英语结果核查和原文链接。

旧词最多一句且无变化不列；事件续篇标明阶段变化与前期关联。候选限定词在正文保留；核验日志、来源缺口和英语需求待验证细节放外部交付说明。Word 使用可用文档工具生成并渲染，两份一起交付。没有工具时保留 JSON/Markdown 并明确 Word 尚未生成，不能把改扩展名的文本当 Word。
