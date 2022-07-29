Feature: Navegando pelo globoplay

  Scenario: Navegando dentro da home
      Given Teste prefixo "nav_"
      Given Modelo de tv Samsung
      When Captura imagem
      When Sequência de comandos "down,down,down"
      When Executa comando "enter"
      When Captura imagem