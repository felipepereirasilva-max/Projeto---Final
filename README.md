Clínica Fácil
Sistema de gestão de uma clínica fictícia desenvolvido em Python com Tkinter, utilizando Programação Orientada a Objetos.

Status: Beta

Classes
Pessoa — classe base.

Paciente — herda de Pessoa.

Medico — herda de Pessoa e pode ter várias especialidades.

Recepcionista — herda de Pessoa.

Especialidade — representa uma especialidade médica.

Consulta — relaciona paciente, médico, data e status.

Atendimento — registra o atendimento de uma consulta.

Clinica — responsável por gerenciar os dados do sistema.

Relacionamentos
classDiagram
    Pessoa <|-- Paciente
    Pessoa <|-- Medico
    Pessoa <|-- Recepcionista

    Medico "1" --> "1..*" Especialidade
    Paciente "1" --> "0..*" Consulta
    Medico "1" --> "0..*" Consulta
    Consulta "1" --> "0..1" Atendimento
    Clinica --> Pessoa
    Clinica --> Paciente
    Clinica --> Medico
    Clinica --> Recepcionista
    Clinica --> Especialidade
    Clinica --> Consulta
    Clinica --> Atendimento

    class Pessoa {
        +nome
        -cpf
    }

    class Paciente {
        +telefone
    }

    class Medico {
        +crm
    }

    class Recepcionista {
        +matricula
    }

    class Especialidade {
        +nome
    }

    class Consulta {
        +data
        +status
    }

    class Atendimento {
        +descricao
    }

    class Clinica {
        +pacientes
        +medicos
        +consultas
        +atendimentos
    }
Paciente, Medico e Recepcionista herdam de Pessoa.

Um Medico pode ter várias Especialidade.

Um Paciente pode ter várias Consulta.

Um Medico pode ter várias Consulta.

Uma Consulta possui um paciente e um médico.

Uma Consulta pode gerar um Atendimento.

A Clinica mantém os dados das outras classes.

Conceitos de POO
Classes e objetos

Herança

Encapsulamento

Polimorfismo

Abstração

Associação

Composição

@property

Exceções personalizadas

Regras
O paciente não pode ter duas consultas no mesmo horário.

O médico não pode ter duas consultas no mesmo horário.

Toda consulta possui paciente, médico e status.

Consulta cancelada não pode gerar atendimento.

Um médico pode ter mais de uma especialidade.

Tecnologias
Python

Tkinter

Programação Orientada a Objetos

Execução
python clinica_facil.py
