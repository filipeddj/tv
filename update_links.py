import subprocess
from pathlib import Path

YOUTUBE_URL = "https://www.youtube.com/@sbt/live"
out_file = Path("lista.m3u")
url = None

print(f"Tentando extrair link de: {YOUTUBE_URL}")

try:
    # Executa o yt-dlp tratando o erro de forma segura
    resultado = subprocess.run(
        ["yt-dlp", "--get-url", "--extractor-args", "youtube:player_client=android", YOUTUBE_URL],
        capture_output=True,
        text=True,
        timeout=40
    )
    
    if resultado.returncode == 0:
        linhas = resultado.stdout.strip().splitlines()
        for l in linhas:
            if ".m3u8" in l or "manifest" in l:
                url = l
                break
        if not url and linhas:
            url = linhas[0]
except Exception as e:
    print(f"Aviso ao executar yt-dlp: {e}")

# Sempre garante que o arquivo lista.m3u vai existir para o GitHub não quebrar
if url:
    print("Link m3u8 obtido com sucesso!")
    conteudo = f"""#EXTM3U

#EXTINF:-1 tvg-chno="28" tvg-logo="https://www.lineup.tv.br/canais/sbt.gif" group-title="TVRO", SBT Ao Vivo
{url}
"""
    out_file.write_text(conteudo, encoding="utf-8")
else:
    print("Aviso: YouTube bloqueou ou a live está offline temporariamente. Mantendo/criando estrutura padrão.")
    if not out_file.exists():
        # Se o arquivo não existir, cria um modelo para não dar erro no git
        conteudo_padrao = """#EXTM3U

#EXTINF:-1 tvg-chno="28" tvg-logo="https://www.lineup.tv.br/canais/sbt.gif" group-title="TVRO", SBT Ao Vivo
https://www.youtube.com/watch?v=placeholder
"""
        out_file.write_text(conteudo_padrao, encoding="utf-8")
