
<h3 align="center">FAZENDO BUSCAS AUTOMÁTICAS NO GOOGLE</h3>


<!-- ABOUT THE PROJECT -->
## Sobre o Projeto

[![tela inicial][product-screenshot]]()

Busca automática no Google. O Bot irá fazer uma busca por palavras chaves pré-definidas

### Construído com

* [Python](https://www.python.org/)
* [Selenium](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/)



<!-- GETTING STARTED -->
## Começando

O bot irá logar no site www.google.com.br, e irá fazer uma busca pelas palavras chaves que está configurado no código. Após localizar o item corretor, ele irá clicar nesse item. Em seguida, ele irá acessar um servidor proxy, e novamente fazer a busca, utilizando as palavras chaves. Esse processo irá ficar em looping até ser interrompido. 

### Pré-requisitos

Antes de tudo você precisa ter o Python instalado no seu computador. Então vá até o site e baixe a versão 3.9 ou superior.
* python
  ```sh
  https://www.python.org/
  ```

### Instalação de bibliotecas

Instalar as bibliotecas abaixo é obrigado para o funcionamento do script.
```sh
pip install selenium
```
```sh
pip install webdriver-manager
```
