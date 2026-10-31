# galgame-craft

**视觉小说 / Galgame 的制作与呈现方法论**——一个兼容 [Agent Skills](https://agentskills.io/) 标准的可移植技能，也是一份不需要任何工具、人可以直接读的 VN 创作手艺手册。

[![format](https://img.shields.io/badge/format-Agent_Skills-blue)](https://agentskills.io/)
[![python](https://img.shields.io/badge/check_script-python_3.8+-yellow)](scripts/check_script.py)
[![renpy](https://img.shields.io/badge/recipes-Ren'Py_8.5.x-red)](references/renpy-recipes.md)
[![works with](https://img.shields.io/badge/works_with-Claude_Code_·_Trae_·_Cursor-green)](#快速开始)

写 VN 剧本、设计选项与分支、排立绘/CG/转场演出、规划变量与结局、判断一部作品为什么"读起来廉价"——每一条都给出**可直接检查的规则**，而不是空泛的"多写多练"。

> **底线**：搞怪剧情的写作权归作者本人。技能提供结构与手艺，不代笔人物腔调——人物的说话方式一旦由工具生成，整部作品就失去唯一的辨识度。

## 目录

- [工作原理](#工作原理)
- [快速开始](#快速开始)
- [30 秒看效果](#30-秒看效果)
- [十条铁律](#十条铁律)
- [目录结构](#目录结构)
- [名作机制库](#名作机制库)
- [FAQ](#faq)
- [Roadmap](#roadmap)
- [贡献](#贡献)
- [致谢](#致谢)
- [License](#license)

## 工作原理

装好之后，你的编码代理在 VN 相关任务上会按一条固定的工作流干活，而不是上来就堆字：

1. **先定角色，再画结构，再写一个字**——每个主要角色填满"表面 / 私下 / 好感反应"三层；多角色作品先画共通线→个人线的宏观结构图，没有这张表不开写
2. **按"话语层"排演出**——每句台词五层同时成立：文本 / 视觉 / 听觉 / 交互 / 系统
3. **写台词**——单句超 45 字拆句、四种句子轮换、潜台词优先，每场写完三条自检
4. **排分支**——折回结构（分叉→2–4 句回应→立刻汇合），选项只改变量不改走向
5. **落地 Ren'Py 并验收**——16 个可粘贴配方 + 两条硬标准：`lint` 零 error、`check_script.py` 零问题。**不验证不算完成**

代理会按任务自动加载对应参考文档：写角色卡时读 `character-design.md`，排演出时读 `presentation.md`，写代码时抄 `renpy-recipes.md`。

## 快速开始

### Claude Code / 其他兼容 Agent Skills 的代理

把整个文件夹放进技能目录（或你的插件市场结构里）：

```
~/.claude/skills/galgame-craft/
```

然后直接说需求即可触发，例如：

- "帮我设计一个 galgame 的分支结构和变量表"
- "这一场戏的立绘、CG 和转场怎么排？"
- "为什么我这部 VN 读起来很廉价？"

### Trae / WorkBuddy

```
~/.workbuddy/skills/galgame-craft/
```

### Cursor / 其他工具

没有技能系统的工具也能用：把本仓库克隆到项目旁，在对话里让代理"读取 galgame-craft/SKILL.md 并按其工作流执行"。

### 不用任何 AI

所有文档自包含，顺序建议：`SKILL.md`（铁律+工作流）→ 按需查 `references/` 五份手册。

## 30 秒看效果

对一个故意埋满硬伤的剧本跑静态检查：

```bash
$ python scripts/check_script.py examples/broken

扫描 1 个 .rpy，1 个 label
 - [台词过长] test.rpy:3 共 60 字（上限 45）：这是一句特别特别特别…
 - [重复 label] start 在 test.rpy:11，首次出现于 test.rpy:1
 - [选项白给] test.rpy:4 的 menu 里没有任何变量修改
 - [悬空跳转] test.rpy:9 跳到不存在的 label: nowhere
 - [缺音频] test.rpy:2 引用不存在的文件: audio/voice/missing.ogg

共 5 条问题
```

五类硬伤：悬空跳转、voice 缺音频、单句过长（默认 45 个中文字）、menu 块无变量修改（选项白给）、重复 label。有错误退出码 1，可接 CI。发布前配套跑 `renpy.exe <project> lint`——lint 看引擎层，check_script 看叙事层。

## 十条铁律

1. **一个文本框只放一个念头。** 超过 45 个中文字就拆。人不是一次读完三行的生物。
2. **信任美术，别复述画面。** 立绘已经皱着眉，就别写"她看起来很生气"。
3. **节奏要有起伏。** 连着五句同样长度的台词，读起来像点名。
4. **潜台词优先于台词。** 没说出口的那半句更值钱。
5. **选项必须两条都成立。** 一眼看出对错的选项叫确认按钮。
6. **选项只改变量，不改走向。** 否则分支数指数爆炸。
7. **用折回结构。** 分叉→各自一小段回应→立刻汇合。
8. **决策要有间隔。** 十分钟弹三次选项，玩家在做问卷。
9. **情绪高点才给 CG。** 插多了就不值钱。
10. **便利功能不自己做。** Ren'Py 自带存档/回溯/历史/跳过/自动，只调样式。

每条的展开版与"廉价八查"（台词太长 / 立绘不动 / 转场单一 / 没有停顿 / 选项白给 / BGM 硬切 / UI 抢戏 / 角色同质）见 [SKILL.md](SKILL.md)。

## 目录结构

```
galgame-craft/
├── SKILL.md                        # 主入口：铁律、工作流、廉价八查、学习循环
├── references/
│   ├── character-design.md         # 角色三层设计 / 反差公式 / 表情差分 / CG 指示书
│   ├── text-and-rhythm.md          # 单句长度 / 句子轮换 / 潜台词 / 主题句螺旋
│   ├── branch-design.md            # 四种宏观结构 / 六种选项 / 变量铁律 / 结局表 / 路线锁
│   ├── presentation.md             # 立绘 / 转场 / CG / 声音 / UI / 便利功能 / 极简的合法性
│   └── renpy-recipes.md            # 16 个 Ren'Py 8.5.x 配方，含踩坑注记
└── scripts/
    └── check_script.py             # 剧本静态检查（零依赖，退出码可接 CI）
```

## 名作机制库

技能内含一个可复用的"学习循环"（五步拆解法），从公认名作提炼机制并回写成规则，目前已固化 18 条：

| 来源 | 机制 |
|---|---|
| 命运石之门 | 世界线收敛；把分支结构做成主题 |
| Muv-Luv | 三段式铺垫回收——日常是给终章存的弹药 |
| 白色相簿2 | 双重语义选项；勇气型 TRUE END |
| Fate/stay night | 顺序锁锁的是信息顺序，不是难度 |
| YU-NO | 分歧图做成玩家界面；存档点是世界内道具 |
| 交响乐之雨 | 主题歌歌词即剧透；角色专属曲 |
| 素晴日 | 多视点轮转——同一事件被不同认知重述 |
| CLANNAD | 光玉跨线收集解锁 TRUE 线 |
| Ever17 | 玩家视点即剧情装置 |
| 寒蝉 / 海猫 | 出题/解答二段式；公平性契约红字 |
| Narcissu | 极简的合法性——缺席可以是叙事工具 |
| 樱之诗 | 主题句螺旋（字面→反讽→救赎） |
| 车轮之国 | 把枷锁做成规则；一本道极限折回 |
| Chaos;Head | 心理型选项——不改剧情改人设 |

## FAQ

**只支持 Ren'Py 吗？**
方法论（结构/选项/演出/文本）引擎无关；`renpy-recipes.md` 与检查脚本是 Ren'Py 专用的。其他引擎（Godot、Ink、Unity+_naninovel 等）可参考方法论部分自行落地。

**会替我写剧情吗？**
不会。技能管结构与手艺：分支怎么折、演出怎么停、变量怎么记账。人物的说话腔调必须由你自己写——那是作品的辨识度。

**中文规则能用于日语/英语项目吗？**
可以，字数阈值需换算（45 中文字约为 90–120 日文字符 / 25–35 英文单词），`--max` 参数可调。

**检查脚本会误报吗？**
会。它是启发式工具：正则解析 `.rpy`，不执行引擎。误报比漏报好——每条输出都带文件与行号，人工过一眼很快。

## Roadmap

- [ ] `examples/` 目录：一个最小可跑的 Ren'Py 示例项目（含故意埋错的反例）
- [ ] 检查脚本：BGM 硬切检测、转场单一检测、立绘表情差分数量统计
- [ ] 多语言 README（English / 日本語）
- [ ] 更多名作拆解（428、G 线上的魔王、Kara no Shōjo）——待出现新的机制族再回写

## 贡献

欢迎 PR。改规则前请先读 `SKILL.md` 的"学习循环"一节——新法则必须给出可检查的判据，不接受"多写多练"式的空话。

## 致谢

- [gamedev-skills/awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills)（6k★）—— 系统层设计旋钮与存档/打字机实现细节
- [galgame-master](https://www.skillmd.ai/ja/skills/galgame-master/SKILL.md)（claude-domain-skills）—— 角色类型库与三层设计思路
- 名作拆解依据的各家分析文章，已标注在各参考文档的案例处

## License

暂未指定，发布前会补齐（计划：代码 MIT + 文档 CC BY 4.0）。

## 适用范围

- 适用于：视觉小说、galgame、dating sim、有美术层的分支叙事游戏
- 不适用于：纯线性小说、无美术层的纯文字交互小说
