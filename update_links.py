import subprocess
from pathlib import Path

# URL direta do vídeo da live do SBT extraída do player do site
YOUTUBE_URL = "https://www.youtube.com/watch?v=R0ZJ4uevOd4"
out_file = Path("lista.m3u")
url = None

print(f"Tentando extrair link m3u8 direto do ID do SBT: {YOUTUBE_URL}")

try:
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

# Atualiza ou gera o arquivo lista.m3u
if url:
    print("Sucesso! Link m3u8 do SBT encontrado.")
    conteudo = f"""#EXTM3U

#EXTINF:-1 tvg-chno="28" tvg-logo="https://www.lineup.tv.br/canais/sbt.gif" group-title="TVRO", SBT Ao Vivo
{url}
"""
    out_file.write_text(conteudo, encoding="utf-8")
else:
    print("Não foi possível atualizar nesta tentativa.")
    if not out_file.exists():
        conteudo_padrao = """#EXTM3U

#EXTINF:-1 tvg-chno="28" tvg-logo="https://www.lineup.tv.br/canais/sbt.gif" group-title="TVRO", SBT Ao Vivo
https://www.youtube.com/watch?v=R0ZJ4uevOd4
"""
        out_file.write_text(conteudo_padrao, encoding="utf-8")
