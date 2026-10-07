from datetime import datetime
from src.modelos import Paciente, Medico, Consulta

class ClinicaGerenciador:
    def __init__(self):
        self.pacientes = []
        self.medicos = []
        self.consultas = []

    def cadastrar_paciente(self, paciente: Paciente):
        self.pacientes.append(paciente)

    def cadastrar_medico(self, medico: Medico):
        self.medicos.append(medico)

    def agendar_consulta(self, paciente: Paciente, medico: Medico, data_hora: datetime) -> bool:
        
        for c in self.consultas:
            if c.paciente.cpf == paciente.cpf and c.data_hora == data_hora and c.status != "Cancelada":
                print(f"Erro: O paciente {paciente.nome} já possui consulta neste horário!")
                return False

            if c.medico.crm == medico.crm and c.data_hora == data_hora and c.status != "Cancelada":
                print(f"Erro: O médico {medico.nome} já possui atendimento neste horário!")
                return False

        nova_consulta = Consulta(paciente=paciente, medico=medico, data_hora=data_hora)
        self.consultas.append(nova_consulta)
        print(f"Consulta agendada com sucesso para {paciente.nome} com Dr(a). {medico.nome}.")
        return True