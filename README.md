# Promissum Palace

## Home Pet

O **Promissum Palace** é um sistema de gestão desenvolvido inicialmente para reservas de hotel e atualmente em processo de evolução para uma plataforma de gestão de **hotel para pets**, denominada **Home Pet**.

O projeto utiliza **Python**, **Programação Orientada a Objetos**, arquitetura em camadas, **FastAPI**, **MySQL** e um frontend web em **HTML, CSS e JavaScript**.

A evolução do sistema busca manter os princípios de engenharia de software já utilizados no projeto original, enquanto adapta o domínio para as necessidades de hospedagem e gerenciamento de pets.

---

# Objetivos do projeto

O projeto tem como objetivos:

* Aplicar Programação Orientada a Objetos em um sistema real
* Utilizar arquitetura em camadas
* Separar regras de negócio, persistência e interface
* Aplicar princípios SOLID
* Reduzir acoplamento entre os componentes
* Manter alta coesão
* Aplicar padrões de projeto quando fizerem sentido
* Trabalhar com persistência relacional utilizando MySQL
* Desenvolver uma API REST utilizando FastAPI
* Construir uma interface web para utilização do sistema
* Evoluir o sistema de hotel tradicional para um sistema de gestão de hospedagem para pets

---

# Tecnologias utilizadas

* Python
* FastAPI
* Pydantic
* MySQL
* MySQL Connector/Python
* HTML5
* CSS3
* JavaScript
* MySQL Workbench
* Programação Orientada a Objetos
* Arquitetura em camadas
* Builder Pattern
* Decorator Pattern
* API REST

---

# Arquitetura

O projeto utiliza uma arquitetura dividida em responsabilidades.

```text
Promissum Palace/
│
├── api/
│   ├── main.py
│   └── schema/
│
├── builder/
│
├── controles/
│
├── dominio/
│   └── decorators/
│
├── frontend/
│   ├── css/
│   ├── js/
│   ├── index.html
│   ├── hospedes.html
│   └── reservas.html
│
├── repositorio/
│
├── servico/
│
├── README.md
└── .gitignore
```

## `api/`

Responsável pela API da aplicação utilizando **FastAPI**.

A API funciona como camada de entrada para o frontend e permite expor as funcionalidades do sistema através de endpoints HTTP.

Também contém os schemas utilizados para validação e estruturação dos dados da API através do **Pydantic**.

---

## `dominio/`

Contém as entidades e regras relacionadas ao domínio da aplicação.

No sistema original, o domínio possui entidades como:

* Hóspede
* Quarto
* Reserva
* Serviço Extra

Também contém os componentes relacionados ao **Decorator Pattern**.

Com a evolução para o Home Pet, o domínio será gradualmente adaptado para trabalhar com entidades relacionadas aos pets, tutores, hospedagens e demais elementos necessários ao novo sistema.

---

## `builder/`

Contém os Builders utilizados para a construção controlada de objetos complexos.

Exemplos atuais:

* `reserva_builder.py`
* `tutor_builder.py`

O objetivo é centralizar a construção dos objetos e evitar que regras de criação fiquem espalhadas pela aplicação.

---

## `repositorio/`

Responsável pela persistência dos dados.

Os repositórios encapsulam as operações relacionadas ao banco de dados MySQL, evitando que SQL e detalhes de persistência sejam espalhados pelas regras de negócio.

Exemplos:

* `MySQLQuartoRepositorio`
* `MySQLReservaRepositorio`
* `MySQLServicoExtraRepositorio`
* `MySQLTutorRepositorio`

Com a evolução do projeto, novos repositórios serão adicionados conforme novas entidades forem integradas.

---

## `servico/`

Responsável pelas regras de negócio da aplicação.

Essa camada deve concentrar comportamentos como:

* Validação de reservas
* Verificação de disponibilidade
* Cancelamento
* Cálculo de valores
* Aplicação de serviços adicionais
* Orquestração entre domínio e repositórios

A camada de serviço deve evitar responsabilidades relacionadas diretamente à interface ou ao SQL.

---

## `controles/`

Responsável por intermediar as operações da aplicação e conectar as diferentes camadas.

Os controles recebem operações da aplicação e encaminham as responsabilidades para os serviços e repositórios apropriados.

---

## `frontend/`

Contém a interface web da aplicação.

Tecnologias utilizadas:

* HTML
* CSS
* JavaScript

Atualmente existem telas relacionadas ao gerenciamento de hóspedes e reservas.

A interface será gradualmente adaptada para o fluxo do **Home Pet** durante a implementação da V1.5.

---

# Padrões de projeto

## Builder Pattern

O Builder Pattern é utilizado para controlar a criação de objetos que possuem múltiplos atributos ou regras de construção.

Exemplo atual:

```text
Reserva
   ↓
ReservaBuilder
   ↓
Reserva validada e construída
```

---

## Decorator Pattern

O Decorator Pattern foi utilizado inicialmente para permitir a adição dinâmica de serviços extras às reservas.

Serviços implementados no sistema original:

* Café da Manhã
* SPA
* Garagem
* Late Checkout

A estrutura permite combinar diferentes serviços sem modificar diretamente a classe base da reserva.

Exemplo conceitual:

```text
Reserva Base
    ↓
+ Café da Manhã
    ↓
+ Garagem
    ↓
+ SPA
    ↓
Reserva com serviços adicionais
```

Os valores dos serviços são obtidos através da camada de persistência, evitando que os preços fiquem espalhados ou fixos nas regras de negócio.

---

# Banco de dados

O sistema utiliza **MySQL** como banco de dados relacional.

A persistência é realizada através da camada de repositórios, mantendo a responsabilidade pelo acesso ao banco separada das entidades e regras de negócio.

O banco original contém estruturas relacionadas a:

* Tutores
* Hóspedes
* Quartos
* Reservas
* Serviços extras

Durante a evolução para o Home Pet, o banco será adaptado para suportar as entidades específicas do novo domínio.

---

# Home Pet — V1.5

A **V1.5** representa a transformação progressiva do sistema de reservas de hotel em um sistema de gestão para hospedagem de pets.

A implementação seguirá uma ordem definida para evitar que funcionalidades de interface sejam construídas antes de suas respectivas estruturas de dados e regras de negócio.

## Ordem oficial de implementação

### 1. Integrar PET ao banco

**Status:** ⬜ Pendente

Primeiro será criada e integrada a estrutura de pets no banco de dados.

Objetivos:

* Criar tabela de pets
* Definir relacionamento entre PET e tutor
* Definir os campos necessários do PET
* Criar persistência
* Criar repositório de PET
* Garantir operações básicas de cadastro, consulta, atualização e exclusão

Essa etapa é a base das demais funcionalidades da V1.5.

---

### 2. Integrar PET ao sistema

**Status:** ⬜ Pendente

Após a estrutura do banco estar funcionando, o PET será integrado às camadas da aplicação.

Objetivos:

* Criar entidade de domínio PET
* Criar Builder quando necessário
* Criar serviços relacionados ao PET
* Criar controle das operações
* Criar schemas da API
* Criar endpoints da API
* Integrar PET ao fluxo de hospedagem/reserva
* Relacionar PET e tutor corretamente

Ao final dessa etapa, o PET deverá existir de forma funcional dentro da aplicação, e não apenas no banco.

---

### 3. Ficha do PET

**Status:** ⬜ Pendente

Será criada uma ficha individual para cada PET.

A ficha deverá concentrar as principais informações necessárias para sua identificação e hospedagem.

Possíveis informações:

* Nome
* Espécie
* Raça
* Sexo
* Data de nascimento
* Peso
* Tutor
* Observações
* Informações relevantes para hospedagem

A ficha deverá utilizar os dados reais provenientes da API e do banco.

---

### 4. Dashboard

**Status:** ⬜ Pendente

Será criada uma visão geral da operação do Home Pet.

O dashboard deverá apresentar informações relevantes para a gestão, como:

* Pets hospedados
* Hospedagens futuras
* Hospedagens em andamento
* Check-ins
* Check-outs
* Ocupação
* Indicadores financeiros básicos

Os indicadores deverão ser baseados nos dados reais do sistema.

---

### 5. Agenda

**Status:** ⬜ Pendente

Será implementada uma agenda para visualização e gerenciamento das hospedagens.

Objetivos:

* Visualizar hospedagens por data
* Identificar check-ins
* Identificar check-outs
* Visualizar ocupação
* Facilitar o acompanhamento das reservas
* Integrar agenda com os dados de hospedagem

---

### 6. Histórico

**Status:** ⬜ Pendente

Será criado o histórico do PET.

O objetivo é permitir consultar acontecimentos e hospedagens anteriores.

Possíveis informações:

* Hospedagens anteriores
* Períodos de hospedagem
* Serviços utilizados
* Valores
* Observações
* Check-in
* Check-out

O histórico deverá utilizar dados persistidos no banco, evitando informações duplicadas ou armazenadas exclusivamente no frontend.

---

### 7. Relatório financeiro básico

**Status:** ⬜ Pendente

A última etapa da V1.5 será a criação de um módulo financeiro básico.

Objetivos:

* Total recebido
* Total de hospedagens
* Receita por período
* Serviços adicionais
* Valores de reservas
* Relatórios básicos por período

Essa etapa será implementada após a existência dos dados necessários nas etapas anteriores.

---

# Fluxo da V1.5

A evolução seguirá a seguinte dependência:

```text
Banco PET
   ↓
PET no sistema
   ↓
Ficha do PET
   ↓
Dashboard
   ↓
Agenda
   ↓
Histórico
   ↓
Relatório financeiro
```

A ordem não deve ser invertida sem uma justificativa técnica, pois cada etapa depende dos dados e funcionalidades construídos anteriormente.

---

# Princípios de desenvolvimento

Durante a evolução do projeto, serão priorizados:

* Código legível
* Responsabilidade única
* Baixo acoplamento
* Alta coesão
* Separação de responsabilidades
* Validação explícita
* Tratamento adequado de erros
* Persistência desacoplada do domínio
* APIs claras
* Frontend separado da lógica de negócio
* Evitar duplicação
* Evitar regras de negócio no frontend
* Evitar SQL espalhado pela aplicação

A complexidade deve ser adicionada somente quando houver necessidade real.

---

# Estado atual

O projeto encontra-se em processo de transição de:

```text
Sistema de reservas de hotel
```

para:

```text
Home Pet
Sistema de gestão de hospedagem para pets
```

A base atual já possui:

* Python
* Programação Orientada a Objetos
* MySQL
* Arquitetura em camadas
* Repositórios
* Serviços
* Controles
* Builders
* Decorators
* FastAPI
* Pydantic
* Frontend web
* Integração inicial entre frontend e backend

A próxima etapa oficial é:

```text
V1.5 — Etapa 1
Integrar PET ao banco
```

---

# Próximas versões

A V1.5 tem como foco principal a transformação do domínio para Home Pet e a construção das funcionalidades essenciais de gestão.

Após a conclusão da V1.5, novas versões poderão evoluir funcionalidades como:

* Integração com WhatsApp
* Notificações
* Comunicação automática com tutores
* Relatórios avançados
* Gestão financeira avançada
* Controle operacional
* Melhorias de autenticação e autorização
* Escalabilidade da API
* Novos módulos administrativos

Essas funcionalidades não fazem parte da implementação imediata da V1.5 e não devem antecipar as etapas definidas para a versão.
