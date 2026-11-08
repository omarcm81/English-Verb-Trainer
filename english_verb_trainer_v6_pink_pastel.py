
import random
import time
from io import BytesIO
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from gtts import gTTS

st.set_page_config(page_title="My English Space", page_icon="🌸", layout="centered")

VERBOS = [
    ("be", "was / were", "been", "ser / estar"),
    ("become", "became", "become", "llegar a ser"),
    ("begin", "began", "begun", "empezar, comenzar"),
    ("bite", "bit", "bitten", "morder"),
    ("break", "broke", "broken", "romper"),
    ("bring", "brought", "brought", "traer / llevar"),
    ("build", "built", "built", "construir"),
    ("burn", "burnt / burned", "burnt / burned", "quemar / arder"),
    ("buy", "bought", "bought", "comprar"),
    ("can", "could", "—", "poder"),
    ("catch", "caught", "caught", "coger, atrapar"),
    ("choose", "chose", "chosen", "elegir, escoger"),
    ("come", "came", "come", "venir, llegar"),
    ("cost", "cost", "cost", "costar"),
    ("cut", "cut", "cut", "cortar"),
    ("do", "did", "done", "hacer"),
    ("draw", "drew", "drawn", "dibujar"),
    ("dream", "dreamt", "dreamt", "soñar"),
    ("drink", "drank", "drunk", "beber"),
    ("drive", "drove", "driven", "conducir"),
    ("eat", "ate", "eaten", "comer"),
    ("fall", "fell", "fallen", "caerse"),
    ("feed", "fed", "fed", "alimentar"),
    ("feel", "felt", "felt", "sentir"),
    ("fight", "fought", "fought", "luchar"),
    ("find", "found", "found", "encontrar"),
    ("fly", "flew", "flown", "volar"),
    ("forget", "forgot", "forgotten", "olvidar"),
    ("freeze", "froze", "frozen", "helar, congelar"),
    ("get", "got", "got", "conseguir, obtener"),
    ("give", "gave", "given", "dar"),
    ("go", "went", "gone", "ir"),
    ("grow", "grew", "grown", "crecer / cultivar"),
    ("have", "had", "had", "tener / haber"),
    ("hear", "heard", "heard", "oír"),
    ("hide", "hid", "hidden", "esconder"),
    ("hit", "hit", "hit", "golpear / chocar"),
    ("hold", "held", "held", "sostener / aguantar"),
    ("hurt", "hurt", "hurt", "herir / doler"),
    ("keep", "kept", "kept", "conservar / mantener"),
    ("know", "knew", "known", "saber, conocer"),
    ("learn", "learnt / learned", "learnt / learned", "aprender"),
    ("leave", "left", "left", "dejar (abandonar)"),
    ("lend", "lent", "lent", "prestar"),
    ("let", "let", "let", "dejar (permitir)"),
    ("lose", "lost", "lost", "perder"),
    ("make", "made", "made", "hacer, fabricar"),
    ("mean", "meant", "meant", "significar"),
    ("meet", "met", "met", "encontrarse / quedar con"),
    ("pay", "paid", "paid", "pagar"),
    ("put", "put", "put", "poner, colocar"),
    ("read", "read", "read", "leer"),
    ("ride", "rode", "ridden", "montar"),
    ("ring", "rang", "rung", "sonar"),
    ("run", "ran", "run", "correr"),
    ("say", "said", "said", "decir"),
    ("see", "saw", "seen", "ver"),
    ("sell", "sold", "sold", "vender"),
    ("send", "sent", "sent", "enviar"),
    ("shine", "shone", "shone", "brillar"),
    ("shoot", "shot", "shot", "disparar"),
    ("shut", "shut", "shut", "cerrar (fuertemente)"),
    ("sing", "sang", "sung", "cantar"),
    ("sit", "sat", "sat", "sentarse"),
    ("sleep", "slept", "slept", "dormir"),
    ("speak", "spoke", "spoken", "hablar"),
    ("spell", "spelt", "spelt", "deletrear"),
    ("spend", "spent", "spent", "gastar"),
    ("stand", "stood", "stood", "estar de pie / colocar"),
    ("steal", "stole", "stolen", "robar"),
    ("swim", "swam", "swum", "nadar"),
    ("swing", "swung", "swung", "balancearse"),
    ("take", "took", "taken", "llevarse / coger"),
    ("teach", "taught", "taught", "enseñar"),
    ("tell", "told", "told", "decir (contar)"),
    ("think", "thought", "thought", "pensar"),
    ("throw", "threw", "thrown", "arrojar, lanzar"),
    ("understand", "understood", "understood", "entender, comprender"),
    ("wake", "woke", "woken", "despertar"),
    ("wear", "wore", "worn", "llevar puesto"),
    ("win", "won", "won", "ganar"),
    ("write", "wrote", "written", "escribir"),
]

st.markdown("""
<style>
:root {
  --pink: #f7c9dc;
  --pink-dark: #9b456b;
  --lavender: #e9e2fa;
  --mint: #dff3e9;
  --peach: #ffeadf;
  --ink: #342633;
}
.stApp {
  background: linear-gradient(145deg, #fff8fb 0%, #fffafd 48%, #f8f5ff 100%);
  color: var(--ink);
}
.block-container {max-width: 900px; padding-top: 1.6rem; padding-bottom: 3rem;}
h1, h2, h3 {color: #8f4268 !important; letter-spacing: -.02em;}
p, label, .stCaption, [data-testid="stMarkdownContainer"] {color: #493746;}
[data-testid="stHeader"] {background: rgba(255,248,251,.88);}
div.stButton > button, div.stFormSubmitButton > button {
  min-height: 3.15rem;
  border-radius: 16px;
  border: 1px solid #e8b5cb;
  background: #f7c9dc;
  color: #342633 !important;
  font-weight: 750;
  box-shadow: 0 3px 10px rgba(155,69,107,.08);
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {
  border-color: #c77c9e;
  background: #f3b8d0;
  color: #342633 !important;
}
div.stButton > button[kind="primary"], div.stFormSubmitButton > button[kind="primary"] {
  background: #f4bfd4 !important;
  color: #2e2029 !important;
  border: 1px solid #df9fba !important;
}
.stRadio [role="radiogroup"] {gap: .55rem;}
.stRadio label, [data-baseweb="select"] > div {
  border-radius: 13px !important;
}
[data-testid="stProgressBar"] > div > div {
  background: linear-gradient(90deg, #efabc9, #c9b8ee, #a9ddc5);
}
.study-card {
  padding: 1.1rem;
  background: rgba(255,255,255,.88);
  border: 1px solid #f0d5e2;
  border-radius: 20px;
  margin: .6rem 0 1rem;
  box-shadow: 0 5px 18px rgba(155,69,107,.07);
}
.big-word {font-size: 1.55rem; font-weight: 800; text-align: center; padding: .4rem; color:#57334a;}
.timeline {display:flex; align-items:center; justify-content:space-around; gap:8px; flex-wrap:wrap; text-align:center;}
.timeline-step {flex:1; min-width:130px; padding:12px 8px; background:#fff0f6; border:1px solid #f3d4e1; border-radius:16px;}
.timeline-step:nth-child(3) {background:#f1edfb; border-color:#e3dcf6;}
.timeline-step:nth-child(5) {background:#eaf7f0; border-color:#d5eee0;}
.timeline-label {font-size:.75rem; color:#79566c; font-weight:800; letter-spacing:.04em;}
.timeline-arrow {font-size:1.35rem; font-weight:800; color:#b56d91;}
[data-testid="stMetric"] {
  background:#fff0f6; border:1px solid #f1d2e0;
  padding: .8rem; border-radius:16px;
}
[data-testid="stAlert"] {border-radius:15px;}
audio {width:100%;}
@media (max-width: 600px) {
  .block-container {padding-left: 1rem; padding-right: 1rem; padding-top: 1rem;}
  .big-word {font-size:1.3rem;}
  .timeline-step {min-width:100px;}
}
</style>
""", unsafe_allow_html=True)


st.title("🌸 My English Space")
st.caption("✨ Aprende, practica y descubre cuánto sabes. ¡You can do it!")
st.caption(f"💗 Tu espacio de inglés · {len(VERBOS)} verbos para dominar.")


@st.cache_data(show_spinner=False)
def generate_audio(text):
    """Genera un MP3 en inglés y lo guarda en caché para no repetir la descarga."""
    audio_buffer = BytesIO()
    gTTS(text=text, lang="en", slow=False).write_to_fp(audio_buffer)
    return audio_buffer.getvalue()


def speak_button(word, key, language="en-US"):
    """Muestra el reproductor de audio nativo, compatible con Safari/iPhone."""
    if word == "—":
        st.caption("Este verbo modal no tiene past participle.")
        return
    st.audio(generate_audio(word), format="audio/mp3")



def start_round(size, seconds):
    indices = list(range(len(VERBOS)))
    random.shuffle(indices)
    st.session_state.round = indices[:size]
    st.session_state.pos = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.answer_ok = (False, False, False)
    st.session_state.last_selected = ("", "", "")
    st.session_state.started = True
    st.session_state.time_limit = seconds
    st.session_state.question_started_at = time.time()

def choices_for(column, correct, question_index):
    values = sorted({row[column] for row in VERBOS})
    distractors = [v for v in values if v != correct]
    rng = random.Random(2026 + question_index * 31 + column)
    rng.shuffle(distractors)
    options = [correct] + distractors[:3]
    rng.shuffle(options)
    return options

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.subheader("🌷 ¡Let’s practice!")
    st.write("Relaciona las formas del verbo y su significado. ¡Cada respuesta te acerca a tu meta!")
    size = st.radio("¿Cuántos verbos quieres practicar?", [5, 10, 15, 20, 82], index=1, horizontal=True)
    seconds = st.radio(
        "Tiempo para responder cada verbo",
        [60, 90, 120, 180, 0],
        index=2,
        format_func=lambda x: "Sin límite" if x == 0 else f"{x} segundos",
        horizontal=True
    )
    if st.button("🚀 Comenzar práctica", type="primary", use_container_width=True):
        start_round(size, seconds)
        st.rerun()
else:
    total = len(st.session_state.round)
    pos = st.session_state.pos

    if pos >= total:
        st.balloons()
        st.success("🎉 ¡Practice complete! ¡Lo hiciste genial!")
        possible = total * 3
        percentage = round(st.session_state.score / possible * 100) if possible else 0
        st.metric("Resultado", f"{st.session_state.score} / {possible}")
        st.progress(percentage / 100, text=f"{percentage}% de respuestas correctas")
        if percentage >= 90:
            st.write("🏆 ¡Increíble! ¡Eres una estrella del inglés!")
        elif percentage >= 70:
            st.write("🌟 ¡Muy bien! Un poquito más de práctica y lo dominarás.")
        else:
            st.write("💪 ¡Tú puedes! Repite la práctica y verás cuánto mejoras.")
        if st.button("🔁 Practicar otra ronda", type="primary", use_container_width=True):
            st.session_state.started = False
            st.rerun()
    else:
        infinitive, past, participle, meaning = VERBOS[st.session_state.round[pos]]
        st.progress(pos / total, text=f"Verbo {pos + 1} de {total}")

        st.markdown(
            f"""
            <div class="study-card">
              <div class="timeline">
                <div class="timeline-step">
                  <div class="timeline-label">INFINITIVE</div>
                  <div class="big-word">{infinitive}</div>
                </div>
                <div class="timeline-arrow">→</div>
                <div class="timeline-step">
                  <div class="timeline-label">PAST SIMPLE</div>
                  <div class="big-word">¿ ?</div>
                </div>
                <div class="timeline-arrow">→</div>
                <div class="timeline-step">
                  <div class="timeline-label">PAST PARTICIPLE</div>
                  <div class="big-word">¿ ?</div>
                </div>
              </div>
              <div style="text-align:center;margin-top:12px;">
                <b>MEANING:</b> {meaning}
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        speak_button(infinitive, f"inf-{pos}")

        if st.session_state.time_limit > 0 and not st.session_state.answered:
            st_autorefresh(interval=1000, key=f"refresh_{pos}")
            elapsed = int(time.time() - st.session_state.question_started_at)
            remaining = max(0, st.session_state.time_limit - elapsed)
            st.progress(remaining / st.session_state.time_limit, text=f"Tiempo restante: {remaining} segundos")
            if remaining == 0:
                st.session_state.answered = True
                st.session_state.answer_ok = (False, False, False)
                st.session_state.last_selected = ("Se agotó el tiempo", "Se agotó el tiempo", "Se agotó el tiempo")
                st.rerun()
        elif st.session_state.time_limit == 0:
            st.caption("⏳ Tiempo sin límite.")

        if not st.session_state.answered:
            with st.form(key=f"form_{pos}"):
                selected_past = st.selectbox("Past simple", choices_for(1, past, pos))
                selected_part = st.selectbox("Past participle", choices_for(2, participle, pos))
                selected_meaning = st.selectbox("Significado en español", choices_for(3, meaning, pos))
                submitted = st.form_submit_button("Comprobar respuestas", type="primary", use_container_width=True)

            if submitted:
                results = (
                    selected_past == past,
                    selected_part == participle,
                    selected_meaning == meaning
                )
                st.session_state.score += sum(results)
                st.session_state.answer_ok = results
                st.session_state.last_selected = (selected_past, selected_part, selected_meaning)
                st.session_state.answered = True
                st.rerun()
        else:
            ok_past, ok_part, ok_meaning = st.session_state.answer_ok
            selected = st.session_state.last_selected
            results = [
                ("Past simple", selected[0], past, ok_past),
                ("Past participle", selected[1], participle, ok_part),
                ("Significado", selected[2], meaning, ok_meaning),
            ]
            for label, chosen, correct, ok in results:
                if ok:
                    st.success(f"{label}: {chosen} ✓")
                else:
                    st.error(f"{label}: elegiste «{chosen}». Correcto: **{correct}**")

            st.markdown("**🔊 Escucha las tres formas del verbo**")
            audio_cols = st.columns(3)
            with audio_cols[0]:
                st.caption("Infinitive")
                speak_button(infinitive, f"review-inf-{pos}")
            with audio_cols[1]:
                st.caption("Past simple")
                speak_button(past, f"review-past-{pos}")
            with audio_cols[2]:
                st.caption("Past participle")
                speak_button(participle, f"review-part-{pos}")

            st.write(f"**Puntos acumulados: {st.session_state.score} de {(pos + 1) * 3} posibles**")
            if st.button("Siguiente verbo ➜", type="primary", use_container_width=True):
                st.session_state.pos += 1
                st.session_state.answered = False
                st.session_state.question_started_at = time.time()
                st.rerun()

        st.divider()
        st.caption("Consejo: pronuncia en voz alta las cuatro formas para recordarlas.")
        if st.button("Terminar práctica", use_container_width=True):
            st.session_state.pos = total
            st.rerun()
