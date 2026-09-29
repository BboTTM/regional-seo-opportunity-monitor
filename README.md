# 区域 SEO 热点挖掘

从本地媒体、社媒和搜索信号发现新主题，生成精简双语 SEO 内容简报。

## 安装

将本仓库克隆到 Codex 的 skills 目录：

```sh
git clone https://github.com/BboTTM/regional-seo-opportunity-monitor.git ~/.codex/skills/regional-seo-opportunity-monitor
```

阅读 [SKILL.md](SKILL.md) 使用；运行环境和输入说明见其中链接。

仓库只包含可复用流程、脚本和模板；业务运行数据保存在仓库之外。安装不会创建定时任务、发送消息或自动写入业务系统。

## 运行环境

审核脚本使用 Python 3.9+ 标准库；研究需要可用的网页检索工具，Word 生成需要可用的文档工具和渲染器。运行 `python tests/test_audit.py` 验证地区隔离和事实一致性。
