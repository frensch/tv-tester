Feature: Navegando pelo globoplay

    Scenario: Navegando dentro da home
        Given Teste prefixo "nav1_"
        Given Modelo de tv Samsung
        When Captura imagem
        When Sequência de comandos "down,down,down"
        When Captura imagem
        When Sequência de comandos "up,up,up"

    Scenario: Navegando até um conteúdo
        Given Teste prefixo "content1_"
        Given Modelo de tv Samsung
        When Captura imagem
        When Sequência de comandos "down,down"
        When Executa comando "enter"
        When Captura imagem
        When Sequência de comandos "up,up"

    Scenario: Buscar um conteúdo
        Given Teste prefixo "search1_"
        Given Modelo de tv Samsung
        When Captura imagem
        When Sequência de comandos "left,up,enter"
        When Digita "pantanal"
        When Executa comando "enter"
        When Captura imagem
        When Sequência de comandos "up,up"