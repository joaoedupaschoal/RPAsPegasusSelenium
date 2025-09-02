# language: pt
# features/abastecimento.feature

Funcionalidade: Cadastro de Abastecimento
  Como usuário do sistema de gestão
  Quero cadastrar informações de abastecimento de veículos
  Para que eu possa controlar e monitorar o consumo de combustível da frota

  Contexto:
    Dado que estou logado no sistema
    E que estou na página inicial do sistema

  Cenário: Cadastro completo de abastecimento com sucesso
    Quando eu acesso o módulo de abastecimento
    E eu clico em cadastrar novo abastecimento
    E eu preencho a data do abastecimento
    E eu seleciono o tipo de combustível
    E eu seleciono o motorista
    E eu seleciono o veículo
    E eu seleciono o posto de combustível
    E eu preencho os dados complementares
    E eu preencho os dados do abastecimento
    Quando eu clico em salvar
    E eu recuso o lançamento no Contas à Pagar
    Então o sistema deve exibir mensagem de sucesso

  Cenário: Cadastro de abastecimento sem preencher data obrigatória
    Quando eu acesso o módulo de abastecimento
    E eu clico em cadastrar novo abastecimento
    E eu seleciono o tipo de combustível
    E eu seleciono o motorista
    E eu seleciono o veículo
    E eu seleciono o posto de combustível
    E eu preencho os dados do abastecimento
    Quando eu clico em salvar
    Então o sistema deve exibir mensagem de alerta

  Cenário: Cadastro de abastecimento sem selecionar combustível
    Quando eu acesso o módulo de abastecimento
    E eu clico em cadastrar novo abastecimento
    E eu preencho a data do abastecimento
    E eu seleciono o motorista
    E eu seleciono o veículo
    E eu seleciono o posto de combustível
    E eu preencho os dados do abastecimento
    Quando eu clico em salvar
    Então o sistema deve exibir mensagem de alerta

  Cenário: Cadastro de abastecimento sem selecionar motorista
    Quando eu acesso o módulo de abastecimento
    E eu clico em cadastrar novo abastecimento
    E eu preencho a data do abastecimento
    E eu seleciona o tipo de combustível
    E eu seleciono o veículo
    E eu seleciono o posto de combustível
    E eu preencho os dados do abastecimento
    Quando eu clico em salvar
    Então o sistema deve exibir mensagem de alerta

  Cenário: Cadastro de abastecimento sem selecionar veículo
    Quando eu acesso o módulo de abastecimento
    E eu clico em cadastrar novo abastecimento
    E eu preencho a data do abastecimento
    E eu seleciono o tipo de combustível
    E eu seleciono o motorista
    E eu seleciono o posto de combustível
    E eu preencho os dados do abastecimento
    Quando eu clico em salvar
    Então o sistema deve exibir mensagem de alerta

  Cenário: Cadastro de abastecimento com dados inválidos
    Quando eu acesso o módulo de abastecimento
    E eu clico em cadastrar novo abastecimento
    E eu preencho a data do abastecimento
    E eu seleciono o tipo de combustível
    E eu seleciono o motorista
    E eu seleciono o veículo
    E eu preencho os dados do abastecimento com valores inválidos
    Quando eu clico em salvar
    Então o sistema deve exibir mensagem de alerta

  @smoke @regression
  Cenário: Cadastro simplificado de abastecimento
    Quando eu acesso o módulo de abastecimento
    E eu clico em cadastrar novo abastecimento
    E eu preencho apenas os campos obrigatórios para abastecimento
    Quando eu clico em salvar
    E eu recuso o lançamento no Contas à Pagar
    Então o sistema deve exibir mensagem de sucesso