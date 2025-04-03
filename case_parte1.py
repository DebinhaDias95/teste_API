import requests
from bs4 import BeautifulSoup
import os
import zipfile
from urllib.parse import urljoin

# Configurações
base_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
output_zip = "anexos_ans.zip"
temp_dir = "temp_anexos"

# Criar diretório temporário se não existir
os.makedirs(temp_dir, exist_ok=True)

def baixar_anexos():
    # Fazendo a requisição para a página
    response = requests.get(base_url)
    response.raise_for_status()

    # Parseando o conteúdo HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurando por links dos anexos
    anexos_encontrados = []
    for link in soup.find_all('a'):
        href = link.get('href', '')
        text = link.get_text().lower()
        
        # Verifica se é Anexo 1 ou 2 (considerando diferentes formatos de escrita)
        if ('anexo i' in text or 'anexo 1' in text or 'anexo ii' in text or 'anexo 2' in text):
            # Verifica se é um link para arquivo (adaptar extensões conforme necessário)
            if any(href.lower().endswith(ext) for ext in ['.pdf', '.xlsx', '.docx', '.odt']):
                # Converte URL relativa para absoluta se necessário
                full_url = urljoin(base_url, href)
                # Determina se é anexo 1 ou 2
                anexo_num = '1' if ('anexo i' in text or 'anexo 1' in text) else '2'
                anexos_encontrados.append((anexo_num, full_url))

    if not anexos_encontrados:
        print("Não foram encontrados links para os anexos na página.")
        return False

    # Baixar cada anexo
    for num, url in anexos_encontrados:
        try:
            filename = os.path.basename(url)
            # Adiciona número do anexo ao nome do arquivo para evitar conflitos
            save_name = f"Anexo_{num}_{filename}"
            save_path = os.path.join(temp_dir, save_name)
            
            print(f"Baixando Anexo {num}: {filename}...")
            file_response = requests.get(url)
            file_response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(file_response.content)
            print(f"Anexo {num} salvo como: {save_name}")
            
        except Exception as e:
            print(f"Erro ao baixar Anexo {num} ({url}): {str(e)}")
    
    return True

def criar_zip():
    # Criar arquivo ZIP com todos os anexos baixados
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.basename(file_path))
    print(f"\nTodos os anexos foram compactados em: {output_zip}")

def limpar_temp():
    # Remover diretório temporário
    for root, _, files in os.walk(temp_dir):
        for file in files:
            os.remove(os.path.join(root, file))
    os.rmdir(temp_dir)

if __name__ == "__main__":
    try:
        if baixar_anexos():
            criar_zip()
        else:
            print("Nenhum anexo foi baixado.")
    finally:
        limpar_temp()
    print("Processo concluído!")