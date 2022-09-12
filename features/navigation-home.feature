Feature: Navegando pelo globoplay

    Scenario: Navegando dentro da home
        Given test prefix "nav1_"
        When load the tv model lg
        When capture image
        #When run command "globoplay"
        #When wainting 10 seconds
        When run command "enter" and wait 4 second(s)
        When run command "down" for 10 times and wait 1 second(s)
        When capture image
        When run command "up" for 10 times and wait 1 second(s)

    Scenario: Navegando até um conteúdo
        Given test prefix "content1_"
        When load the tv model lg
        When capture image
        When sequence of commands "down,down" and wait 0.1 second(s)
        When run command "enter" and wait 0.1 second(s)
        When capture image
        When waiting 2 second(s)
        When run command "back" and wait 2 second(s)
        When sequence of commands "up,up" and wait 1 second(s)

    Scenario: Buscar um conteúdo
        Given test prefix "search1_"
        When load the tv model lg
        When capture image
        When sequence of commands "left,up,enter" and wait 3 second(s)
        When typing "pantanal" and wait 3 second(s)
        When sequence of commands "right,right,right,right,right,right,enter" and wait 2 second(s)
        When capture image
        When run command "back" and wait 2 second(s)
        When run command "back" and wait 2 second(s)
        When sequence of commands "down,enter" and wait 2 second(s)
        When sequence of commands "left,down,down,down,down,enter" and wait 2 second(s)
        When sequence of commands "right,enter" and wait 1 second(s)

        #When sequence of commands "up,up,right,right,left,down,down,down,down,enter" and wait 2 second(s)
