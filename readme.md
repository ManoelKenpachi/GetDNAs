# Web Scraping com Playwright e BeautifulSoup

Este é um projeto de Web Scraping utilizando as bibliotecas Playwright e BeautifulSoup em Python. O objetivo deste projeto é extrair informações do site https://www.prosispro.com/demo/AeraDemo.aspx e criar arquivos CSV para cada registro de motor.

## Instalação

Para utilizar este projeto, é necessário ter o Python 3.x instalado. Além disso, é necessário instalar as bibliotecas contidas no arquivo requirements.txt. Para instalar as bibliotecas, execute o seguinte comando no terminal:

```pip install -r requirements.txt```

Será necessário instalar o playwright
```playwright install```

## Utilização

Para utilizar o projeto, basta executar o script crawler.py. Ele irá coletar as informações de cada registro de motor e salvar em um arquivo CSV correspondente. Os arquivos CSV serão salvos na raiz do projeto.

## Exemplo de Uso

```python
from crawler import Scraper

scraper = Scraper()
scraper.run([1, 2, 3, 4, 5])
```

Neste exemplo, a função run é chamada com uma lista de ids de motor para serem coletados. Os arquivos CSV correspondentes serão salvos na raiz do projeto.

## Melhorias
- Verifcar se pricesará otimizar o código para coletar os 10 mil DNA's
- Coletar Diagrams e o Casting Number

## Contribuições
Contribuições são bem-vindas! Sintam-se à vontade.

## Licença
{...}
Basta copiar o texto acima e manter a formatação. Qualquer dúvida, estou à disposição!