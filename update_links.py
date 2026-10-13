import subprocess
import sys

# URL da live do SBT
YOUTUBE_URL = "https://www.youtube.com/@sbt/live"

print(f"Buscando link ao vivo de: {YOUTUBE_URL}")

try:
    # Usa o yt-dlp atualizado para extrair o link direto
    resultado = subprocess.run(
        ["yt-dlp", "--get-url", "--extractor-args", "youtube:player_client=android", YOUTUBE_URL],
        capture_output=True,
        text=True,
        check=True,
        timeout=40
    )
    
    linhas = resultado.stdout.strip().splitlines()
    url_final = None
    
    for l in linhas:
        if ".m3u8" in l or "manifest" in l:
            url_final = l
            break
            
    if not url_final and linhas:
        url_final = linhas[0]

    if url_final:
        print(f"Link encontrado com sucesso!")
        # Grava o arquivo lista.m3u perfeitamente formatado
        conteudo = f"""#EXTM3U

#EXTINF:-1 tvg-chno="28" tvg-logo="https://www.lineup.tv.br/canais/sbt.gif" group-title="TVRO", SBT Ao Vivo
{url_final}
"""
        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(conteudo)
        print("Arquivo lista.m3u gerado com sucesso!")
    else:
        print("Nenhum link de vídeo válido foi retornado.")
        sys.exit(0)

except Exception as e:
    print(f"Aviso na extração (ignorando para não quebrar o robô): {e}")
    sys.exit(0)
