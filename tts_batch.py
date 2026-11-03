import os
import time
import wave
from google import genai
from google.genai import types

# 1. 填入你的 Gemini API Key
API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)

# 创建保存音频的文件夹
output_dir = "gold_extraction_voices"
os.makedirs(output_dir, exist_ok=True)

# 强化成熟男性解说风格的提示词（明确指定性别与胸腔共鸣感）
STYLE_PROMPT = (
    "请以一名35岁成熟成年男性的声音发音，音色深沉稳重、富有胸腔共鸣与磁性。"
    "语气要像硬核纪录片解说员，沉着笃定、节奏紧凑，重点字句咬字清晰有力，不要出现女声调或轻浮播音腔：\n"
)

# 8个分镜对应完整口播文案
scripts = {
    "01": "很多人不知道，提炼黄金其实是所有贵金属里门槛最低的！",
    "02": "不用大设备，核心就这5样东西，当天看完就能搞明白。",
    "03": "第一样：环保脱金粉。网上就能搞到，500克一包能用很久，专剥废料表面的镀金。",
    "04": "第二样：柠檬酸和片碱。这一步是关键！精准调节酸碱度，调不好黄金根本置换不出来。",
    "05": "第三样：锌丝。放进去用来置换黄金，只要看到锌丝迅速变黑，就证明黄金抓出来了！",
    "06": "第四样：电解液。浸泡氧化掉多余杂质，剩下的就是纯正的海绵金。",
    "07": "第五样：焊枪和坩埚。放入坩埚直接高温熔炼，一颗3个9的高纯度黄金直接到手！",
    "08": "成本极低、工序清晰。想了解更多贵金属回收与实操技巧，关注我，带你拆解更多实用干货！"
}

total_count = len(scripts)
for i, (idx, text) in enumerate(scripts.items(), 1):
    print(f"[{i}/{total_count}] 正在生成第 {idx} 镜音频 (稳重男声)...")

    # 每段生成前休眠 20 秒，避开免费配额 RPM 频率限制
    if i > 1:
        print("⏳ 冷却中，请稍候 20 秒...")
        time.sleep(20)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=STYLE_PROMPT + text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            # Fenrir 为纯正磁性成熟男声；若需更板正庄重的纪实音色可选 Charon
                            voice_name="Fenrir"
                        )
                    )
                ),
            ),
        )

        audio_bytes = response.candidates[0].content.parts[0].inline_data.data
        file_path = os.path.join(output_dir, f"shot_{idx}.wav")
        with wave.open(file_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(audio_bytes)
        print(f"✅ 已保存: {file_path}")

    except Exception as e:
        print(f"❌ 第 {idx} 镜生成失败: {e}")

print("🎉 全部 8 镜男声音频生成完成！")