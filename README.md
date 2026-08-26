# Promissum Palace

## Descrição

O **Promissum Palace** é um sistema de gestão de reservas de hotel desenvolvido em **Python puro**, com foco em **Programação Orientada a Objetos (POO)**, arquitetura em camadas e aplicação de padrões de projeto utilizados em sistemas reais.

O projeto foi criado com o objetivo de praticar conceitos avançados de engenharia de software, como:

* SOLID
* Baixo acoplamento
* Alta coesão
* Object Calisthenics
* Separação de responsabilidades
* Persistência relacional
* Concorrência de reservas

Além disso, o sistema implementa padrões de projeto importantes, como:

* Builder Pattern
* MVC Pattern
* MySQL
* Decorator Pattern

O sistema permite o cadastro de hóspedes, quartos e reservas, além da adição de serviços extras em reservas utilizando composição dinâmica com Decorators.

Toda a persistência é feita utilizando **MySQL**, garantindo armazenamento real dos dados e separação adequada entre domínio e persistência.

---

# Funcionalidades

O sistema permite:

* Cadastrar hóspedes
* Cadastrar quartos
* Criar reservas
* Cancelar reservas
* Listar hóspedes
* Listar quartos
* Listar reservas
* Verificar conflitos de datas automaticamente
* Adicionar serviços extras em reservas
* Calcular valor total da reserva dinamicamente
* Persistir serviços extras no banco de dados

O sistema impede que dois hóspedes reservem o mesmo quarto no mesmo período.

------------------------------------------------------------------------------------

# Tecnologias utilizadas

* Python
* MySQL
* MySQL Workbench
* Programação Orientada a Objetos (POO)
* Arquitetura em camadas
* Builder Pattern
* MVC
* Decorator Pattern

------------------------------------------------------------------------------------

# Arquitetura do projeto

O projeto foi estruturado em camadas para reduzir acoplamento e facilitar manutenção e escalabilidade.

## Dominio

Contém as entidades principais do sistema:

* Hospede
* Quarto
* Reserva
* ServicoExtra

Também contém os Decorators responsáveis pelos serviços adicionais das reservas.

------------------------------------------------------------------------------------

## Builder

Responsável pela construção controlada de objetos complexos, como:

* Hospede
* Quarto
* Reserva

Garantindo validações e consistência na criação dos objetos.

---------------------------------------------------------------------------------------

## Repositorio

Responsável pela persistência de dados no banco MySQL.

Os repositórios encapsulam toda a lógica SQL da aplicação.

Exemplos:

* MySQLHospedeRepositorio
* MySQLQuartoRepositorio
* MySQLReservaRepositorio
* MySQLServicoExtraRepositorio

------------------------------------------------------------------------------------

## Servico

Responsável pelas regras de negócio do sistema.

Exemplos:

* Verificação de disponibilidade de quartos
* Validação de reservas
* Cancelamento de reservas
* Aplicação dinâmica de Decorators
* Cálculo do valor total da reserva

------------------------------------------------------------------------------------

## Controles

Intermediam a comunicação entre a interface do usuário e os serviços do sistema.

------------------------------------------------------------------------------------
## Main

Interface de linha de comando responsável pela interação com o usuário.

------------------------------------------------------------------------------------

# Decorator Pattern no projeto

O padrão **Decorator** foi utilizado para adicionar serviços extras às reservas de forma dinâmica, sem modificar diretamente a classe `Reserva`.

Cada serviço adicional funciona como um Decorator independente que encapsula a reserva base e adiciona novos comportamentos ao cálculo do valor final.

Os serviços implementados atualmente são:

* Café da Manhã
* SPA
* Garagem
* Late Checkout

O sistema utiliza composição dinâmica, permitindo combinar múltiplos serviços em uma mesma reserva.

Exemplo:

```python
Reserva Base + SPA + Garagem + Café

Cada Decorator possui responsabilidade única e adiciona apenas seu próprio comportamento ao sistema.

Os valores dos serviços extras não ficam hardcoded no código.

Todos os valores são persistidos e carregados diretamente do banco de dados através do MySQLServicoExtraRepositorio.
