import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(
    page_title="📜 墨影文魁：國中成語會考封神榜",
    page_icon="⚔️",
    layout="centered"
)

# 瀏覽器原生 Web Audio API 音效播放
def play_sound(sound_type):
    if not st.session_state.get("sound_on", True):
        return
    
    if sound_type == "correct":
        js = """
        <script>
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        function playTone(freq, delay, dur) {
            setTimeout(() => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(freq, ctx.currentTime);
                gain.gain.setValueAtTime(0.15, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + dur);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + dur);
            }, delay);
        }
        playTone(523.25, 0, 0.2);
        playTone(659.25, 120, 0.2);
        playTone(783.99, 240, 0.4);
        </script>
        """
    elif sound_type == "wrong":
        js = """
        <script>
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(160, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(90, ctx.currentTime + 0.35);
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.35);
        </script>
        """
    elif sound_type == "win":
        js = """
        <script>
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        [523.25, 659.25, 783.99, 1046.5].forEach((f, i) => {
            setTimeout(() => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(f, ctx.currentTime);
                gain.gain.setValueAtTime(0.18, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.4);
            }, i * 160);
        });
        </script>
        """
    components.html(js, height=0, width=0)

# 玄青科技風格樣式
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #090e17 0%, #101c2e 45%, #192a45 80%, #060b12 100%);
        color: #f1f5f9;
    }

    @keyframes gold-glow {
        0% { border-color: #38bdf8; box-shadow: 0 0 25px rgba(56, 189, 248, 0.4); }
        50% { border-color: #fbbf24; box-shadow: 0 0 35px rgba(251, 191, 36, 0.6); }
        100% { border-color: #38bdf8; box-shadow: 0 0 25px rgba(56, 189, 248, 0.4); }
    }

    .hero-banner {
        background: rgba(15, 23, 42, 0.85);
        border: 3px solid #fbbf24;
        animation: gold-glow 5s infinite ease-in-out;
        border-radius: 20px;
        padding: 22px;
        text-align: center;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        margin-bottom: 6px;
    }

    .hero-sub {
        color: #94a3b8;
        font-size: 1.1rem;
        letter-spacing: 2px;
    }

    .mode-badge {
        display: inline-block;
        background: #0284c7;
        color: #ffffff;
        font-weight: 800;
        padding: 5px 14px;
        border-radius: 12px;
        font-size: 1rem;
        margin-bottom: 12px;
        box-shadow: 0 0 10px rgba(2, 132, 199, 0.5);
    }

    .rune-container {
        background: radial-gradient(circle, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 2px dashed #fbbf24;
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        font-size: 2.4rem;
        font-weight: 900;
        color: #f8fafc;
        text-shadow: 0 0 15px rgba(251, 191, 36, 0.5);
        margin: 16px 0;
    }

    [data-testid="stMetricValue"] {
        color: #fbbf24 !important;
        font-size: 2.2rem !important;
        font-weight: 900 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #38bdf8 !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
    }

    div.stButton > button {
        height: 80px !important;
        font-size: 1.55rem !important;
        font-weight: 800 !important;
        border-radius: 16px !important;
        border: 2px solid #38bdf8 !important;
        background: #1e293b !important;
        color: #f8fafc !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        border-color: #fbbf24 !important;
        box-shadow: 0 8px 20px rgba(251, 191, 36, 0.5) !important;
        background: #334155 !important;
    }

    .magic-scroll {
        background: rgba(30, 41, 59, 0.85);
        border: 2px solid #38bdf8;
        border-radius: 14px;
        padding: 14px;
        font-size: 1.15rem;
        font-weight: 700;
        text-align: center;
        color: #f8fafc;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 國中會考核心成語三組題庫
ALL_QUEST_SETS = [
    {
        "set_name": "⚔️ 第一卷：鐵血智略與歷史篇",
        "questions": [
            {
                "mode": "📜 語境字形檢驗",
                "prompt": "買 【 ❓ 】 還 珠",
                "target": "櫝",
                "options": ["盒", "櫝", "犢", "贖"],
                "meaning": "【買櫝還珠】：買了木盒子卻退還寶珠。比喻缺乏眼光，捨本逐末。"
            },
            {
                "mode": "💡 文史語意推理",
                "prompt": "項羽渡江後鑿沉船隻、砸破飯鍋，誓與秦軍決一死戰 ➔ 【 ❓ ❓ ❓ ❓ 】",
                "target": "破釜沉舟",
                "options": ["破釜沉舟", "背水一戰", "紙上談兵", "臥薪嘗膽"],
                "meaning": "【破釜沉舟】：形容做事抱持必死決心，誓不回頭。"
            },
            {
                "mode": "🔗 名人典故接軌",
                "prompt": "越王勾踐刻苦自勵、雪恥復仇 ➔ 【 ❓ ❓ ❓ ❓ 】",
                "target": "臥薪嘗膽",
                "options": ["臥薪嘗膽", "投筆從戎", "聞雞起舞", "懸樑刺股"],
                "meaning": "【臥薪嘗膽】：形容人發憤圖強，刻苦自立以求成功。"
            }
        ]
    },
    {
        "set_name": "🌟 第二卷：世態洞察與情操篇",
        "questions": [
            {
                "mode": "📜 語境字形檢驗",
                "prompt": "名 落 【 ❓ 】 山",
                "target": "孫",
                "options": ["孫", "泰", "南", "華"],
                "meaning": "【名落孫山】：宋代孫山榜上最後一名，比喻投考或評選未被錄取。"
            },
            {
                "mode": "💡 文史語意推理",
                "prompt": "陶淵明《桃花源記》中環境優美、遠離紛擾的理想安寧之所 ➔ 【 ❓ ❓ ❓ ❓ 】",
                "target": "世外桃源",
                "options": ["世外桃源", "海市蜃樓", "空中樓閣", "別有洞天"],
                "meaning": "【世外桃源】：比喻風景優美而人跡罕至的地方，或不受外界干擾的理想世界。"
            },
            {
                "mode": "🔗 名人典故接軌",
                "prompt": "劉備放下身段，三次前往隆中拜訪隱士 ➔ 【 ❓ ❓ ❓ ❓ 】",
                "target": "三顧茅廬",
                "options": ["三顧茅廬", "程門立雪", "負荊請罪", "倒屣相迎"],
                "meaning": "【三顧茅廬】：比喻真心誠意地一再邀請賢才。"
            }
        ]
    },
    {
        "set_name": "🖋️ 第三卷：文章才思與百態篇",
        "questions": [
            {
                "mode": "📜 語境字形檢驗",
                "prompt": "洛 陽 【 ❓ 】 貴",
                "target": "紙",
                "options": ["紙", "筆", "墨", "玉"],
                "meaning": "【洛陽紙貴】：晉代左思寫成《三都賦》，眾人爭相傳抄致使紙價飛漲。比喻著作極受歡迎。"
            },
            {
                "mode": "💡 文史語意推理",
                "prompt": "趙括只懂空談兵法書本，不懂臨機應變，長平之戰慘敗 ➔ 【 ❓ ❓ ❓ ❓ 】",
                "target": "紙上談兵",
                "options": ["紙上談兵", "管窺蠡測", "南轅北轍", "掩耳盜鈴"],
                "meaning": "【紙上談兵】：比喻只憑書本空談理論，不能解決實際問題。"
            },
            {
                "mode": "🔗 名人典故接軌",
                "prompt": "廉頗背負荊條向藺相如誠懇登門認錯 ➔ 【 ❓ ❓ ❓ ❓ 】",
                "target": "負荊請罪",
                "options": ["負荊請罪", "刎頸之交", "化干戈為玉帛", "握手言和"],
                "meaning": "【負荊請罪】：形容主動向對方承認錯誤並請求責罰與原諒。"
            }
        ]
    }
]

def start_new_game(prev_idx=None):
    available = [i for i in range(len(ALL_QUEST_SETS)) if i != prev_idx]
    chosen_set_idx = random.choice(available)
    selected_set = ALL_QUEST_SETS[chosen_set_idx]
    
    st.session_state.current_set_idx = chosen_set_idx
    st.session_state.current_set_name = selected_set["set_name"]
    quest_list = []
    for q in selected_set["questions"]:
        q_copy = dict(q)
        shuffled_options = list(q["options"])
        random.shuffle(shuffled_options)
        q_copy["options"] = shuffled_options
        quest_list.append(q_copy)
    st.session_state.quests = quest_list
    st.session_state.quest_idx = 0
    st.session_state.exp = 0
    st.session_state.feedback = ""
    st.session_state.feedback_type = "info"
    st.session_state.trigger_sound = None

if "quests" not in st.session_state:
    start_new_game()
    st.session_state.sound_on = True

if st.session_state.get("trigger_sound"):
    play_sound(st.session_state.trigger_sound)
    st.session_state.trigger_sound = None

# 控制列
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2.5, 1, 1.2])
with col_ctrl2:
    sound_btn = "🔊 音效開啟" if st.session_state.sound_on else "🔇 靜音"
    if st.button(sound_btn, use_container_width=True):
        st.session_state.sound_on = not st.session_state.sound_on
        st.rerun()

with col_ctrl3:
    if st.button("🔄 換卷重試", use_container_width=True):
        start_new_game(st.session_state.current_set_idx)
        st.rerun()

# 標題橫幅
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">📜 墨影文魁：國中成語會考封神榜 ⚔️</div>
    <div class="hero-sub">✦ 語境鑑別 · 典故推理 · 歷史鏈接 三階素養試煉 ✦</div>
</div>
""", unsafe_allow_html=True)

# 顯示卷名
st.markdown(f"<div style='text-align:center; font-size:1.15rem; color:#fbbf24; font-weight:800; margin-bottom:12px;'>📖 當前考核卷：{st.session_state.current_set_name}</div>", unsafe_allow_html=True)

# 儀表狀態
quests = st.session_state.quests
total_q = len(quests)
col1, col2, col3 = st.columns(3)
col1.metric("⚡ 答題修為 EXP", f"{st.session_state.exp} 點")
col2.metric("🗺️ 會考進度", f"第 {min(total_q, st.session_state.quest_idx + 1)} / {total_q} 題")

if st.session_state.exp >= 60:
    rank = "🌟 殿試文魁狀元"
elif st.session_state.exp >= 20:
    rank = "🗡️ 國子監解元"
else:
    rank = "🌱 應試秀才生"
col3.metric("🏆 國文位階", rank)

st.progress(min(1.0, max(0.0, st.session_state.exp / (total_q * 20.0))))
st.markdown("---")

# 通關判定
if st.session_state.quest_idx >= total_q:
    play_sound("win")
    st.balloons()
    st.snow()
    st.markdown("""
    <div class="hero-banner">
        <h2 style="color:#fbbf24; font-size:2.2rem; margin:0;">🎉 考核通關！文魁封神！🏆</h2>
        <p style="color:#94a3b8; font-size:1.15rem; margin-top:8px;">國中會考核心成語精熟達成！可點右上角換卷繼續磨練。</p>
    </div>
    """, unsafe_allow_html=True)
    st.success(f"🏅 最終修為：滿分 **{st.session_state.exp} EXP**，榮登【{rank}】寶座！")
else:
    curr = quests[st.session_state.quest_idx]
    
    st.markdown(f'<div style="text-align:center;"><span class="mode-badge">{curr["mode"]}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rune-container">{curr["prompt"]}</div>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#38bdf8;'>👇 請審慎判斷正解：</h4>", unsafe_allow_html=True)

    cols = st.columns(len(curr["options"]))
    for i, opt in enumerate(curr["options"]):
        if cols[i].button(opt, key=f"q_{st.session_state.current_set_idx}_{st.session_state.quest_idx}_{i}", use_container_width=True):
            if opt == curr["target"]:
                st.session_state.exp += 20
                st.session_state.feedback = f"✨【答對了！】{curr['meaning']}"
                st.session_state.feedback_type = "success"
                st.session_state.trigger_sound = "correct"
            else:
                st.session_state.feedback = f"💥【判斷失誤】正解為【{curr['target']}】。{curr['meaning']}"
                st.session_state.feedback_type = "warning"
                st.session_state.trigger_sound = "wrong"
            
            st.session_state.quest_idx += 1
            st.rerun()

    if st.session_state.feedback:
        color = "#10b981" if st.session_state.feedback_type == "success" else "#f43f5e"
        st.markdown(f'<div class="magic-scroll" style="border-color:{color};">{st.session_state.feedback}</div>', unsafe_allow_html=True)