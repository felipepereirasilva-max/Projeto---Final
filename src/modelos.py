from datetime import datetime

class Pessoa:
    def __init__(self, nome: str, cpf: str, telefone: str):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone


class Paciente(Pessoa):
    def __init__(self, nome: str, cpf: str, telefone: str, convenio: str = "Particular"):
        super().__init__(nome, cpf, telefone)
        self.convenio = convenio


class Especialidade:
    def __init__(self, nome: str):
        self.nome = nome


class Medico(Pessoa):
    def __init__(self, nome: str, cpf: str, telefone: str, crm: str):
        super().__init__(nome, cpf, telefone)
        self.crm = crm
        self.especialidades = []  # Um médico pode ter múltiplas especialidades

    def adicionar_especialidade(self, especialidade: Especialidade):
        if especialidade not in self.especialidades:
            self.especialidades.append(especialidade)


class Recepcionista(Pessoa):
    def __init__(self, nome: str, cpf: str, telefone: str, turno: str):
        super().__init__(nome, cpf, telefone)
        self.turno = turno


class Consulta:
    def __init__(self, paciente: Paciente, medico: Medico, data_hora: datetime, status: str = "Agendada"):
        self.paciente = paciente
        self.medico = medico
        self.data_hora = data_hora
        self.status = status  # Ex: Agendada, Em Andamento, Concluída, Cancelada