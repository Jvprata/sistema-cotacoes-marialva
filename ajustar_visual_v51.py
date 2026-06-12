from pathlib import Path
from datetime import datetime

app = Path("app.py")
texto = app.read_text(encoding="utf-8")

marcador = "MARIALVA_HIDE_STREAMLIT_HEADER_V51"

css = '''
# Ajuste visual V5.1 — esconder barra superior do Streamlit
st.markdown("""
<style>
/* MARIALVA_HIDE_STREAMLIT_HEADER_V51 */

[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden !important;
}

footer {
    visibility: hidden !important;
}

.block-container {
    padding-top: 0.8rem !important;
}
</style>
""", unsafe_allow_html=True)

'''

if marcador in texto:
    print("O ajuste visual V5.1 já foi aplicado. Nenhuma alteração feita.")
else:
    backup = Path(f"app_backup_antes_v51_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")
    backup.write_text(texto, encoding="utf-8")

    linhas = texto.splitlines(True)
    inicio = None

    for i, linha in enumerate(linhas):
        if "st.set_page_config" in linha:
            inicio = i
            break

    if inicio is None:
        raise Exception("Não encontrei st.set_page_config no app.py.")

    contador = 0
    fim = inicio

    for j in range(inicio, len(linhas)):
        contador += linhas[j].count("(")
        contador -= linhas[j].count(")")
        if contador <= 0:
            fim = j
            break

    linhas.insert(fim + 1, css)
    novo_texto = "".join(linhas)

    app.write_text(novo_texto, encoding="utf-8")

    print("Ajuste visual V5.1 aplicado com sucesso!")
    print(f"Backup criado em: {backup}")
    print("Agora rode novamente: python -m streamlit run app.py")
