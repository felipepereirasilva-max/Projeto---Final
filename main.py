import sys
from pathlib import Path

# Adiciona a pasta raiz do projeto ao caminho de busca do Python
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.modelos import Paciente, Medico, Especialidade
from src.gerenciador import ClinicaGerenciador






from datetime import datetime
from src.modelos import Paciente, Medico, Especialidade
from src.gerenciador import ClinicaGerenciador

def rodar_demonstracao():
    clinica = ClinicaGerenciador()

    # 1. Criando Especialidades
    cardio = Especialidade("Cardiologia")
    pediatria = Especialidade("Pediatria")

    # 2. Criando e cadastrando Médico com múltiplas especialidades
    medico1 = Medico("Carlos Silva", "111.222.333-44", "9999-8888", "CRM/SP 123456")
    medico1.adicionar_especialidade(cardio)
    medico1.adicionar_especialidade(pediatria)
    clinica.cadastrar_medico(medico1)

    # 3. Criando e cadastrando Paciente
    paciente1 = Paciente("Ana Maria", "555.666.777-88", "8888-7777")
    clinica.cadastrar_paciente(paciente1)

    # 4. Agendando Consulta válida
    horario = datetime(2026, 11, 10, 14, 0)
    clinica.agendar_consulta(paciente1, medico1, horario)

    # 5. Tentando agendar consulta no mesmo horário (Deve falhar)
    print("\n--- Testando Regra de Horário Duplicado ---")
    clinica.agendar_consulta(paciente1, medico1, horario)

if __name__ == "__main__":
    rodar_demonstracao()