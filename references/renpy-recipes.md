# Ren'Py 落地配方

引擎版本以 8.5.x 为准。以下全部为可直接粘贴的片段。

## 一、角色与台词

```renpy
# 有名字 + 名牌颜色
define ye = Character("Ye")

# 主角不配音、不显示名牌
define mc = Character("我")

# 内心独白：自动包全角括号 + 转灰
define think = Character(None, what_prefix="（", what_suffix="）", what_color="#c6c9d0")
```

**踩坑**：不要在 `Character()` 里写 `who_color` 跟名牌底色同色——名牌会变成一块空胶囊。名牌文字颜色交给 style。

## 二、立绘：入场、呼吸、站位

```renpy
# 呼吸：4.8 秒一轮，幅度 ±4px（超过 5px 就假）
transform idle_breathe:
    yoffset 0
    block:
        ease 2.4 yoffset -4
        ease 2.4 yoffset 0
        repeat

# 入场：淡入 + 上浮，然后接呼吸
transform enter_up:
    alpha 0.0
    yoffset 20
    parallel:
        ease 0.7 alpha 1.0
    parallel:
        ease 0.7 yoffset 0
    block:
        ease 2.4 yoffset -4
        ease 2.4 yoffset 0
        repeat

# 站位槽
transform stand_left:
    xalign 0.0
    xoffset 240
    yalign 1.0
transform stand_center:
    xalign 0.5
    yalign 1.0
transform stand_right:
    xalign 1.0
    xoffset -240
    yalign 1.0
```

**踩坑**：ATL 变换和 `with` 过渡不能写在同一条 `show` 语句里（`show x at anim with dissolve` 会炸）。分开写：

```renpy
show ye jk at enter_up
with dissolve
```

## 三、说话方高亮

```renpy
# 非说话方压到 75%
transform dimmed:
    matrixcolor BrightnessMatrix(-0.15)

# 用法
show kendrick jk at stand_left
show scott jk at stand_right, dimmed

kendrick "小声点。"

show scott jk at stand_right          # 换人说话，把压暗撤掉
show kendrick jk at stand_left, dimmed
```

## 四、全屏图铺满不裁文件

```renpy
define CG = dict(fit="cover", xysize=(1920, 1080))
image bg store = Transform("images/bg/bg_store.jpg", **CG)
```

原图一律不裁不改，缩放裁切交给运行时——**素材永远可回溯**。

## 五、黑屏淡入（醒来 / 时间跳跃）

```renpy
scene black
pause 0.4
scene bg bedroom
with Dissolve(2.0)
```

## 六、推近镜头（同一张图做出"压迫感"）

```renpy
transform push_in:
    zoom 1.0
    ease 1.8 zoom 1.125

# 用法：改背景的 transform，不要重新 scene
show bg bedroom at push_in
```

## 七、震屏（引擎没有 shake API）

```renpy
transform shake_hard:
    block:
        linear 0.02 xoffset 8
        linear 0.02 xoffset -8
        linear 0.02 xoffset 5
        linear 0.02 xoffset 0
        repeat

# 用法
show layer master at shake_hard
```

`renpy.shake()` 不存在，别调。

## 八、选项只改变量

```renpy
menu:
    "（老实承认醒了）":
        $ aff(1)
        mc "……醒了。抱歉。"
    "（继续装睡）":
        $ edge += 1
        think "再撑三秒。"
```

首行缩进不要用 `menu` 里的 `$` 做剧情跳转——跳转放在汇合点之后。

## 九、好感度唯一入口

```renpy
init python:
    def aff(n):
        store.trust = max(0, min(11, store.trust + n))
```

每次调用顺手可以加一个浮动提示，但**不要**在别处直接写 `trust += 1`。

## 十、语音

```renpy
voice "audio/voice/ye_001.ogg"
ye "你就是那个龙国来的留学生？"
```

挂了 voice 的台词**文字钉死**——改字必须重新生成音频。

## 十一、UI 改三处就够

```renpy
# 1) 对话框：自定义底图，别改生成器的文件（会被 init 阶段重写）
style window:
    xpos 120
    ypos 744
    xsize 1680
    ysize 260
    background "gui/textbox_custom.png"

# 2) 名牌：固定尺寸，否则两个字会缩成一块小方糖
define gui.namebox_width = 130
define gui.namebox_height = 72

# 3) 快速菜单：默认关掉，右键/ESC 仍可开菜单
default quick_menu = False
```

**踩坑**：`gui/textbox.png` / `namebox.png` 这些是 GUI 生成器托管的，跑 lint 会被重写。自定义文件名 + `style` 指过去。

## 十二、截图验证（无人值守）

```renpy
label shot_demo:
    scene bg corridor
    show kendrick jk at stand_left
    $ renpy.say(kendrick, "小声点。", interact=False)
    $ renpy.pause(0.4, hard=True)
    $ renpy.screenshot(r"D:\proj\_shot.png")
    $ renpy.quit()
```

```bash
renpy.exe . run --warp game/_shot.rpy:2
```

需要"真实交互态"才画得出来的界面（推进后才出现的 UI），改用 `config.periodic_callbacks` 里判断 `renpy.get_screen("say")` 再截图。验证完把 `_shot.rpy` / `_shot.png` / `traceback.txt` 一起删。

## 十三、故事变量用 default，常量用 define

```renpy
# 会存档的变量：一律 default（缺省值 + 自动进存档）
default trust = 5
default gift = "none"
default ws_soft = False

# 常量：一律 define（不进存档，改了也不坏旧档）
define ye = Character("Ye")
define CG = dict(fit="cover", xysize=(1920, 1080))
```

**踩坑**：用 `define` 声明故事变量，旧档加载时会被重置回初始值；用 `default` 声明角色和常量，白白撑大每个存档。**同一变量写两次 `default` 直接抛异常**（`store.trust is being given a default a second time`）——变量只允许一个文件声明，其他文件直接引用。另一个坏档主因是**修改玩家存档点附近的台词**——旧档从半句话中间恢复会错乱，发布前冻结剧本比什么都管用。

## 十四、文字速度：必须能到"瞬间"

```renpy
define gui.text_cps = 40   # 默认逐字速度；0 = 瞬间显示，玩家设置里要能拉到 0
```

打字机效果引擎已内置，**不要自己用字符串切片做逐字显示**——切片会把标签切半、每帧重排版，字会跳行。Ren'Py 的 CPS 按显示字符计数，标签安全。

## 十五、本地化就绪

- 台词、选项、UI 字符串全部走脚本与翻译文件，**不许烘进图片**——图里带字，那句话就永远只有一种语言
- 对话框宽度预留约 30% 余量：译成英文普遍比中文长，写死必炸
- Ren'Py 原生多语言（`translations` 目录 + 语言切换），立项时留好结构，别写完再抠

## 十六、好感度浮字（改值 + 反馈必须绑死）

```renpy
init python:
    def aff(d):
        store.trust = max(0, min(11, store.trust + d))
        renpy.show_screen("aff_flash", delta=d)

transform aff_float:
    alpha 0.0
    yoffset 0
    ease 0.25 alpha 1.0 yoffset -18
    pause 0.55
    ease 0.5 alpha 0.0 yoffset -52

screen aff_flash(delta):
    zorder 150                      # 压在立绘之上、菜单之下
    $ _txt = ("+%d" % delta) if delta > 0 else ("−%d" % -delta)
    $ _col = "#F27FB2" if delta > 0 else "#9B7CFF"
    text _txt:
        at aff_float
        xalign 0.78
        yalign 0.26
        color _col
        size 46
        outlines [(2, "#00000099", 0, 0)]
    timer 1.4 action Hide("aff_flash")   # 不写 timer 浮字永远挂着
```

- 加减分**必须走 `aff()`**：任何一处裸写 `trust += 1`，那次就不弹字，玩家觉得"选了没反应"
- 颜色分正负用**粉/紫，不要红绿**——中国玩家把红色当警告
- **不是所有变量都该被玩家看见**：刀值 `edge` 刻意不走浮字——藏起来的数值才有后劲

## 十七、成就系统（persistent + toast）

```renpy
default persistent.achievements = set()     # 跨存档；set 天然免疫重复解锁

init python:
    def ach(key, name, kind="normal"):
        if key in persistent.achievements:
            return                          # 必须提前返回，否则读档就弹一次
        persistent.achievements.add(key)
        renpy.show_screen("ach_toast", name=name, kind=kind)

define ACH_LIST = [
    ("p_clear",   "被叫醒的早上", "读完序章。", "normal"),
    ("aff_max",   "她先开的口",   "好感度达到 11。", "challenge"),
    ("gift_milk", "热的比凉的好", "在便利店买了热牛奶。", "normal"),
    ("all_gift",  "便利店常客",   "四种礼物全部见过。", "hidden"),
]
# 四列：key（唯一标识）/ 显示名 / 说明 / 类型（normal 金、challenge 紫、hidden 暗金）

transform toast_slide:
    xoffset 420                     # 位移要比 toast 宽度大，才能完全滑出屏外
    alpha 0.0
    ease 0.35 xoffset 0 alpha 1.0
    pause 2.8
    ease 0.4 xoffset 420 alpha 0.0

screen ach_toast(name, kind="normal"):
    zorder 210
    $ _head = "挑战完成！" if kind == "challenge" else "成就达成！"
    $ _accent = "#C79BFF" if kind == "challenge" else "#E8C36A"
    frame:
        at toast_slide
        xalign 1.0
        yalign 0.0
        xoffset -36
        yoffset 36
        padding (18, 14)
        background "#12111488"      # 直接写死半透明，不依赖 gui. 变量，换主题不崩
        vbox:
            spacing 6
            text _head size 16 color _accent
            text name size 24 color "#F7F6F1"
    timer 3.7 action Hide("ach_toast")   # 略大于动画总时长 3.55，留 0.15s 余量
```

图鉴界面（`use game_menu` 挂进菜单）里，未解锁条目**只显名字、隐藏说明**——玩家知道还有货，但不被剧透。挂载入口：`screen navigation()` 里加 `textbutton _("Achievements") action ShowMenu("achievements")`，主菜单和游戏内菜单一次全有。

## 十八、剧情线地图（AST 现场推导，不手画）

手画的分支图在第一次改剧本后就过期了。正确做法：每次打开界面时遍历 Ren'Py 已加载的 AST（`renpy.game.script.namemap`），纯静态读、不执行剧本——剧本一改，图自动跟着变。

```renpy
init python:
    import renpy.ast as _ast

    def _route_src(node):
        try:
            return (node.code.source or "").strip()
        except Exception:
            return ""

    def _route_walk(block, out):
        for node in block:
            if isinstance(node, _ast.Menu):
                opts = []
                for cap, cond, blk in node.items:
                    fx, hop = [], None
                    for s in blk:
                        if isinstance(s, _ast.Python):
                            fx.append(_route_src(s))
                        elif isinstance(s, _ast.Jump) and isinstance(s.target, str):
                            hop = s.target
                        elif isinstance(s, _ast.Return):
                            hop = "（结束）"
                    opts.append(dict(cap=cap, cond=cond, fx=fx, hop=hop))
                out.append(dict(kind="menu", opts=opts))
            elif isinstance(node, _ast.If):
                for _c, blk in node.entries:
                    _route_walk(blk, out)
            elif isinstance(node, _ast.While):
                _route_walk(node.block, out)

    def route_scan():
        res = []
        for _name, node in renpy.game.script.namemap.items():
            if not isinstance(node, _ast.Label) or not isinstance(node.name, str):
                continue
            if node.name.startswith("_"):                     # 过滤一：引擎内部 label
                continue
            if "renpy/common" in (node.filename or "").replace("\\", "/"):
                continue                                      # 过滤二：common 目录
            ev = []
            _route_walk(node.block, ev)
            res.append(dict(label=node.name,
                            file=(node.filename or "").split("/")[-1].split("\\")[-1],
                            line=node.linenumber,
                            seen=renpy.seen_label(node.name),
                            events=ev))
        res.sort(key=lambda d: (d["file"], d["line"]))
        return res
```

界面里 `textbutton r["label"]: action Start(r["label"])` 可从任意段落直接开局试演出（变量是默认值，复现真实状态请用存档）。**踩坑**：屏幕语言里不要写 `"[r[file]]"` 这类嵌套插值（会炸 `NameError: name 'file' is not defined`），改用 Python 表达式拼接：`(r["file"] + " : " + str(r["line"]))`。● / ○ 用 `renpy.seen_label()` 区分读没读过；变量改动金色、跳转紫色——颜色即语义。

## 十九、验收命令

```bash
renpy.exe . lint
python <skill>/scripts/check_script.py .
```

lint 看引擎层（图片/音频引用是否正确），check_script 看叙事层（台词长度、选项白给、悬空跳转）。
