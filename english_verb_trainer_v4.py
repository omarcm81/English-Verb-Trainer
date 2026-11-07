
import random
import time
from io import BytesIO
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from gtts import gTTS

st.set_page_config(page_title="English Verb Trainer", page_icon="📘", layout="centered")

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
.block-container {max-width: 900px; padding-top: 2rem;}
div.stButton > button {min-height: 3rem; border-radius: 12px; font-weight: 600;}
.study-card {padding: 1rem; border: 1px solid #d9dce3; border-radius: 14px; margin: .5rem 0 1rem;}
.big-word {font-size: 1.6rem; font-weight: 750; text-align: center; padding: .35rem;}
.timeline {display:flex; align-items:center; justify-content:space-around; gap:8px; flex-wrap:wrap; text-align:center;}
.timeline-step {flex:1; min-width:130px; padding:10px; background:#f0f4fa; border-radius:12px;}
.timeline-label {font-size:.75rem; color:#536176; font-weight:700;}
.timeline-arrow {font-size:1.5rem; font-weight:700;}
</style>
""", unsafe_allow_html=True)

st.title("📘 English Verb Trainer")
st.caption("Relaciona infinitivo → pasado simple → participio, y aprende el significado en español.")
st.caption(f"Material de estudio: {len(VERBOS)} verbos de las dos hojas.")


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
    st.subheader("¡Vamos a practicar!")
    st.write("Aparecerá un verbo y tendrás que relacionar sus formas y su significado.")
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
        st.success("¡Práctica terminada!")
        possible = total * 3
        percentage = round(st.session_state.score / possible * 100) if possible else 0
        st.metric("Resultado", f"{st.session_state.score} / {possible}")
        st.progress(percentage / 100, text=f"{percentage}% de respuestas correctas")
        if percentage >= 90:
            st.write("¡Excelente dominio!")
        elif percentage >= 70:
            st.write("¡Muy bien! Repasa los verbos que fallaste.")
        else:
            st.write("Conviene repetir la práctica para reforzar las relaciones.")
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
