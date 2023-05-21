from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import os


class Scraper:
    def __init__(self, username: str, password: str):
        # URLs para acessar as páginas do site
        self.url_login = 'https://www.prosispro.com/demo/AeraDemo.aspx'
        self.url_eng = 'https://www.prosispro.com/demo/EngineSpecification.aspx'
        self.url_eng_details = 'https://www.prosispro.com/demo/EngineSpecificationDetails.aspx?eid='

        # Dados de login
        self.username = username
        self.password = password

    def download_image(self, tag_a, dna: int) -> None:
        """
        Realiza o download dos diagramas 
        
        Args:
        tag_a: Tag onde está contida a imagem.
        dna: Id do DNA que está sendo gerado.

        Return:
            None
            ps: Gera a imagem na pasta do seu DNA
        """

        # Verificar se a pasta não existe
        if not os.path.exists(f'diagrams/{dna}'):
            # Criar a pasta
            os.makedirs(f'diagrams/{dna}')

        # Extrair o valor do atributo href e title
        href = tag_a['href']
        title = tag_a['title']

        # Realizar o download da imagem diretamente pelo link
        response = requests.get(f'https://www.prosispro.com/demo/{href}')

        # Verificar se a resposta é bem-sucedida
        if response.status_code == 200:
            # Salvar a imagem com o título como nome
            with open(f"diagrams/{dna}/{title}.gif", "wb") as file:
                file.write(response.content)
        else:
            print(f"Falha ao baixar a imagem. {title}.")

    def run(self, list_dnas: list) -> None:
        """
        Realiza a coleta de dados dos DNAs passados como parâmetro.
        
        Args:
        list_dnas (list): Lista de DNAs a serem coletados.

        Return:
            None
            ps: Gera um csv para cada DNA com seus atributos
        """

        with sync_playwright() as playwright:
            # Inicia o navegador e abre a página de login
            browser = playwright.chromium.launch()
            page = browser.new_page()

            page.goto(self.url_login, timeout=120000)
            time.sleep(3)

            # Preenche o campo de usuário e senha e clica no botão de login
            page.fill('#txtUserName', self.username)
            page.fill('#txtPassword', self.password)
            page.click('#btnlogin')

            # Espera a página carregar
            time.sleep(3)
            page.screenshot(path='login.png')

            # Loop para coletar os dados de cada DNA
            for dna in list_dnas:
                print(f'Coletando dados do DNA {dna}')

                # # Lista que armazenará os dataframes
                dataframes = []

                # Acessa a página de detalhes do DNA
                page.goto(f'{self.url_eng_details}{dna}',
                          wait_until='load', timeout=600000)
                page.wait_for_selector("#tab-main-1-contant")
                # gera uma imagem png do estado atual da pagina
                page.screenshot(path=f'dna_{dna}.png')

                # Extrai o código HTML da div que contém as tabelas
                html = page.inner_html("#tab-main-1-contant")

                # Transforma o código HTML em um objeto BeautifulSoup e encontra todas as tabelas
                soup = BeautifulSoup(html, 'html.parser')
                tabelas = soup.find_all("table")

                # Loop para ler cada tabela e salvar em um dataframe
                for tabela in tabelas:
                    df = pd.read_html(str(tabela))[0]  # Lê a tabela
                    # Reseta o índice do dataframe
                    df.reset_index(drop=True, inplace=True)
                    # Adiciona o dataframe à lista de dataframes
                    dataframes.append(df)

                # Crie um dataframe vazio com as colunas necessárias
                df_final = pd.DataFrame(
                    columns=["coluna1", "coluna2", "coluna3"])

                #  loop pelos dataframes a serem adicionados
                for df in dataframes:
                    # criar um DataFrame vazio com a mesma estrutura do DataFrame final
                    df_em_branco = pd.DataFrame(columns=df_final.columns)

                    # adicionar uma linha em branco ao DataFrame em branco
                    df_em_branco.loc[0] = [None] * len(df_final.columns)

                    # Gerar novos nomes para as colunas
                    new_columns = [
                        'Coluna' + str(i) for i in range(1, len(df.columns) + 1)]

                    # Mapear os novos nomes para as colunas existentes
                    mappings = dict(zip(df.columns, new_columns))

                    # Renomear as colunas do DataFrame
                    df = df.rename(columns=mappings)

                    # concatenar o DataFrame em branco e o DataFrame atual
                    df_final = pd.concat(
                        [df_final, df_em_branco, df], ignore_index=True)

                # Executar o código JavaScript para clicar no elemento
                page.evaluate("document.querySelector('#tab-main-2').click()")

                # Esperar um tempo para a ação ser concluída (opcional)
                page.wait_for_timeout(2000)  # Aguarda 2 segundos

                # Extrai o código HTML da div que contém as tabelas
                diagrams = page.inner_html("#ContentPlaceHolder1_UpdatePanel1")
                # print(diagrams)

                # Transforma o código HTML em um objeto BeautifulSoup e encontra todas as tabelas
                soup_d = BeautifulSoup(diagrams, 'html.parser')

                # Encontrar a div "diagrams"
                div_diagrams = soup_d.find('div', class_='clsDiagramsDesktop')

                # Verificar se a div foi encontrada
                if div_diagrams:
                    # Encontrar todas as tags <a> dentro da div
                    tags_a = div_diagrams.find_all('a')

                    # Iterar sobre as tags <a> encontradas
                    for tag in tags_a:
                        # Extrair o valor do atributo href e title
                        self.download_image(tag, dna)
                else:
                    print("Div 'diagrams' não encontrada.")

                # # Executar o código JavaScript para clicar no elemento
                # page.evaluate("document.querySelector('#tab-main-3').click()")
                # # casting_html = page.inner_html(".pd-t-15 pd-b-50")
                # page.wait_for_timeout(2000)  # Aguarda 2 segundos
                # page.screenshot(path=f'casting_{dna}.png')

                # soup_casting = BeautifulSoup(page, 'html.parser')

                # casting_table = soup_casting.find_all("table")
                # print(casting_table[-1])
                # casting_table = casting_table
                # df_casting = pd.read_html(str(casting_table))[0]  # Lê a tabela
                # df_casting.reset_index(drop=True, inplace=True)

                # df_casting = df_casting.drop(df_casting.columns[[0, 1, 2, 3]], axis=1)
                # df_casting.to_csv(f'casting_{dna}.csv', sep=';')

                # Exclua as colunas de índice 0, 1 e 2 e gera o csv
                df_final = df_final.drop(df_final.columns[[0, 1, 2]], axis=1)
                df_final.to_csv(f'dna_{dna}.csv', sep=';')

            # Fecha o navegador
            browser.close()


if __name__ == '__main__':
    # Dados de login
    username = 'manoelkenpachi@gmail.com'
    password = 'Manoel2023'

    scraper = Scraper(username, password)
    scraper.run([1, 2 ,3, 4, 5]) #list(map(lambda x: x, range(1, 10000)))
