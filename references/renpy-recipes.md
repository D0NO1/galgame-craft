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

**踩坑**：用 `define` 声明故事变量，旧档加载时会被重置回初始值；用 `default` 声明角色和常量，白白撑大每个存档。另一个坏档主因是**修改玩家存档点附近的台词**——旧档从半句话中间恢复会错乱，发布前冻结剧本比什么都管用。

## 十四、文字速度：必须能到"瞬间"

```renpy
define gui.text_cps = 40   # 默认逐字速度；0 = 瞬间显示，玩家设置里要能拉到 0
```

打字机效果引擎已内置，**不要自己用字符串切片做逐字显示**——切片会把标签切半、每帧重排版，字会跳行。Ren'Py 的 CPS 按显示字符计数，标签安全。

## 十五、本地化就绪

- 台词、选项、UI 字符串全部走脚本与翻译文件，**不许烘进图片**——图里带字，那句话就永远只有一种语言
- 对话框宽度预留约 30% 余量：译成英文普遍比中文长，写死必炸
- Ren'Py 原生多语言（`translations` 目录 + 语言切换），立项时留好结构，别写完再抠

## 十六、验收命令

```bash
renpy.exe . lint
python <skill>/scripts/check_script.py .
```

lint 看引擎层（图片/音频引用是否正确），check_script 看叙事层（台词长度、选项白给、悬空跳转）。
