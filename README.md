# 🎙️ Gemini 批量语音合成 · TTS Batch

> 一份分镜文案表，一次跑出全套配音：指定音色、控制语气、自动避开 RPM 限流。

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Gemini-TTS-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**中文** | [English](#-english)

---

## 用途

做完分镜，配音是最后一道手工活：一条条念、一条条导出、命名、对齐。几十个镜头能耗一下午。

这个脚本把「文案字典」直接转成「按镜号命名的 WAV 文件」：

```python
scripts = {
    "01": "很多人不知道，提炼黄金其实是所有贵金属里门槛最低的！",
    "02": "不用大设备，核心就这5样东西，当天看完就能搞明白。",
    ...
}
```

跑完得到 `shot_01.wav` … `shot_08.wav`，直接拖进剪映/PR 对齐时间轴。

## 核心能力

| 能力 | 说明 |
|---|---|
| **音色可控** | 用自然语言描述音色（年龄、性别、共鸣、语气、咬字），比选预设音色更接近你想要的效果 |
| **批量合成** | 按镜号遍历，失败单独捕获，一条挂了不影响其他 |
| **限流保护** | 每段之间自动冷却 20 秒，避开免费配额 RPM 限制 |
| **24kHz 单声道 WAV** | 直接可用，无需再转格式 |
| **密钥走环境变量** | 不硬编码，可安全提交到 Git |

## 语气提示词是怎么写的

脚本里的 `STYLE_PROMPT` 是效果的关键。它没有用"男声"两个字了事，而是把音色拆成可描述的维度：

```python
"请以一名35岁成熟成年男性的声音发音，音色深沉稳重、富有胸腔共鸣与磁性。"
"语气要像硬核纪录片解说员，沉着笃定、节奏紧凑，重点字句咬字清晰有力，"
"不要出现女声调或轻浮播音腔："
```

**负面约束很重要**——"不要出现女声调"这类反向描述，比单纯堆正面形容词有效得多。换行业时照着这个结构改：年龄 + 音色质感 + 语气 + 职业参照 + 负面排除。

## 快速开始

```bash
git clone https://github.com/czh79/gemini-tts-batch.git
cd gemini-tts-batch
pip install -r requirements.txt
```

**设置密钥**

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="你的密钥"
# macOS / Linux
export GEMINI_API_KEY="你的密钥"
```

密钥在 [Google AI Studio](https://aistudio.google.com/apikey) 免费申请。

**运行**

```bash
python tts_batch.py
```

输出目录 `gold_extraction_voices/`，文件名 `shot_01.wav` 起。

## 配置项

| 变量 | 位置 | 说明 |
|---|---|---|
| `GEMINI_API_KEY` | 环境变量 | **必填**，代码中不保存任何密钥 |
| `scripts` | 代码字典 | 镜号 → 文案，直接替换成你的分镜 |
| `STYLE_PROMPT` | 代码常量 | 音色与语气描述 |
| `output_dir` | 代码常量 | 输出目录 |
| 冷却秒数 | 代码常量（`20`） | 免费配额建议保持 20s，付费可调小 |

## 免费配额注意事项

Gemini TTS 免费层有 RPM（每分钟请求数）限制。脚本默认每段间隔 20 秒，即每分钟 3 段。

- 段数很多（> 50）时，建议拆成几批跑，或者接付费 key 把冷却降到 3–5 秒
- 单段失败不会中断整体流程，最后可以只重跑失败的镜号

---

## 🇬🇧 English

> Turn a shot-by-shot script dictionary into a folder of numbered WAV voiceovers, with a described voice instead of a preset one.

### Why describe the voice in prose

`STYLE_PROMPT` doesn't just say "male voice". It decomposes timbre into dimensions a TTS model can act on:

```
age + timbre texture (deep, chest resonance) + delivery (measured, tight pacing)
+ occupational reference (documentary narrator) + negative constraints
```

The **negative constraints** are what make it work — "no female register, no breezy anchor tone" steers the output far more effectively than piling on positive adjectives.

### Features

- Batch synthesis keyed by shot number; one failure doesn't abort the run.
- 20-second cooldown between segments to stay under the free-tier RPM limit.
- 24kHz mono WAV output, ready to drop on a timeline.
- **No hardcoded credentials** — the API key is read from `GEMINI_API_KEY`.

### Usage

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-key"
python tts_batch.py
```

Get a free key at [Google AI Studio](https://aistudio.google.com/apikey). Output lands in `gold_extraction_voices/shot_XX.wav`.

---

<div align="center">

做短视频配音的朋友，**点个 Star** ⭐

</div>
