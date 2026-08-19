import streamlit as st

# Frecuencias de letras en español para el análisis de Al-Kindi
FREQ_MAP = {
    'a': 12.5, 'e': 13.6, 'o': 8.6, 's': 7.9, 'r': 6.8,
    'n': 6.7, 'i': 6.2, 'd': 5.8, 'l': 4.9, 't': 4.6,
    'c': 4.6, 'u': 3.9, 'm': 3.1, 'p': 2.5, 'b': 1.4, ' ': 15.0
}

st.set_page_config(page_title="Cifrado Clásico y Al-Kindi", layout="centered")

st.title("🔐 Sistema de Cifrado y Criptoanálisis Inteligente")
st.markdown("Implementación basada en los principios históricos de **أبو يوسف يعقوب بن إسحاق الكندي**.")

# 1. Configuración del Alfabeto
st.subheader("1. Configuración del Alfabeto")
alphabet_default = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 0123456789.,!?"
alphabet = st.text_input("Conjunto de caracteres (ASCII o símbolos) para el cifrado:", value=alphabet_default)

# 2. Cifrado
st.subheader("2. Cifrar un Mensaje")
plain_text = st.text_area("Mensaje a cifrar:", "Hola mundo 2026")
cipher_type = st.selectbox("Método de Cifrado:", ["César", "Atbash"])

shift = 3
if cipher_type == "César":
    shift = st.number_input("Módulo (Desplazamiento):", min_value=1, max_value=len(alphabet) - 1, value=3)


def encrypt_text(text, alpha, method, mod):
    result = ""
    for char in text:
        if char not in alpha:
            result += char
            continue
        idx = alpha.index(char)
        if method == "César":
            new_idx = (idx + mod) % len(alpha)
            result += alpha[new_idx]
        elif method == "Atbash":
            new_idx = len(alpha) - 1 - idx
            result += alpha[new_idx]
    return result


if st.button("Cifrar Mensaje"):
    if alphabet:
        encrypted = encrypt_text(plain_text, alphabet, cipher_type, shift)
        st.success(f"**Mensaje Cifrado:**\n`{encrypted}`")
    else:
        st.error("El alfabeto no puede estar vacío.")

# 3. Descifrado Automático (Al-Kindi)
st.subheader("3. Descifrado Automático (Análisis de Frecuencias)")
cipher_input = st.text_area("Mensaje cifrado a hackear:")


def score_text(text):
    score = 0
    lower_text = text.lower()
    for char in lower_text:
        score += FREQ_MAP.get(char, 0.1)  # Pequeño valor por defecto para evitar ceros absolutos
    return score / (len(text) if len(text) > 0 else 1)


if st.button("Hackear y Descifrar Automáticamente"):
    if cipher_input and alphabet:
        best_score = -1
        best_text = ""
        detected_method = ""

        # Probar Atbash
        atbash_text = ""
        for char in cipher_input:
            if char not in alphabet:
                atbash_text += char
                continue
            idx = alphabet.index(char)
            new_idx = len(alphabet) - 1 - idx
            atbash_text += alphabet[new_idx]

        best_score = score_text(atbash_text)
        best_text = atbash_text
        detected_method = "Atbash"

        # Probar César con todos los módulos posibles
        for s in range(1, len(alphabet)):
            cesar_text = ""
            for char in cipher_input:
                if char not in alphabet:
                    cesar_text += char
                    continue
                idx = alphabet.index(char)
                new_idx = (idx - s) % len(alphabet)
                cesar_text += alphabet[new_idx]

            c_score = score_text(cesar_text)
            if c_score > best_score:
                best_score = c_score
                best_text = cesar_text
                detected_method = f"César (Módulo: {s})"

        st.info("¡Sistema analizado mediante Criptoanálisis Estadístico!")
        st.write(f"**Algoritmo Detectado:** {detected_method}")
        st.success(f"**Mensaje Original Descifrado:** {best_text}")
    else:
        st.warning("Por favor ingresa un texto cifrado y asegúrate de tener un alfabeto definido.")
