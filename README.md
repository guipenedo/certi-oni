## Setup

1. Clonar e dar cd

    ```
    git clone git@github.com:guipenedo/certi-oni.git
    cd certi-oni
    ```

2. Criar e ativar um virtualenv
    ```
    python3 -m virtualenv env
    source env/bin/activate
    ```
    
3. Instalar os requirements

    ```
    pip install -r requirements.txt
    sudo apt-get install texlive-latex-base texlive-latex-extra
    ```

4. Adicionar ao diretório onde o script corre o ficheiro "passwd.txt" do mooshak

5. Alterar o ficheiro template.tex
    Há as seguintes tags:
    - **@POS@** posição na classificação
    - **@ANO@** ano de escolaridade
    - **@ESCOLA@** sigla escola
    - **@NOME@** nome concorrente (sem escola)
    - **@PONTOS@** pontuação
    - **@ESCOLA_COMP@** nome escola - completo (tirado do passwd.txt)
    - **@NOME_COMP@** nome concorrente (sem escola) - completo (tirado do passwd.txt)

6. Correr o programa e indicar o URL com a classificação
    ```
    python certi-oni.py
    ```

A output é gerada automaticamente e guardada em output/
É possível mudar algumas settings como output directory, filename, nome de ficheiro template etc alterando as variáveis no topo do script