import subprocess
import re

# URL da live oficial do SBT no YouTube
YOUTUBE_URL = "https://www.youtube.com/@sbt/live"

def pegar_link_m3u8_youtube(url):
    try:
        print(f"Buscando link ao vivo em: {url}")
        # O yt-dlp extrai a URL de transmissão direta (.m3u8)
        comando = ["yt-dlp", "--get-url", url]
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        links = resultado.stdout.strip().splitlines()
        
        for l in links:
            if ".m3u8" in l or "manifest" in l:
                print("Link m3u8 encontrado com sucesso!")
                return l
    except Exception as e:
        print(f"Erro ao extrair do YouTube: {e}")
    return None

novo_link = pegar_link_m3u8_youtube(YOUTUBE_URL)

if novo_link:
    # Lê o arquivo lista.m3u atual
    with open("lista.m3u", "r", encoding="utf-8") as f:
        linhas = f.readlines()

    # Atualiza a linha que contém o link do SBT
    novo_conteudo = []
    atualizar_proxima = False
    
    for linha in linhas:
        if "SBT Ao Vivo" in linha:
            atualizar_proxima = True
            novo_conteudo.append(linha)
        elif atualizar_proxima:
            novo_conteudo.append(novo_link.strip() + "\n")
            atualizar_proxima = False
        else:
            novo_conteudo.append(linha)

    # Regrava o arquivo lista.m3u atualizado
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.writelines(novo_conteudo)
    
    print("Sua lista.m3u foi atualizada com o link novo do SBT!")
else:
    print("Não foi possível obter o link do YouTube neste momento.")
