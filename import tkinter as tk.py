import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from datetime import datetime


class ErroClinica(Exception):
    pass


class HorarioOcupadoError(ErroClinica):
    pass


class Pessoa(ABC):
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self._cpf = cpf
        self.telefone = telefone

    @property
    def cpf(self):
        return self._cpf

    @abstractmethod
    def apresentar(self):
        pass


class Paciente(Pessoa):
    def __init__(self, nome, cpf, telefone, nascimento):
        super().__init__(nome, cpf, telefone)
        self.nascimento = nascimento
        self.consultas = []

    def apresentar(self):
        return f"Paciente: {self.nome}"

    def adicionar_consulta(self, consulta):
        self.consultas.append(consulta)


class Especialidade:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return self.nome


class Medico(Pessoa):
    def __init__(self, nome, cpf, telefone, crm):
        super().__init__(nome, cpf, telefone)
        self.crm = crm
        self.especialidades = []
        self.consultas = []

    def apresentar(self):
        return f"Dr(a). {self.nome} - CRM: {self.crm}"

    def adicionar_especialidade(self, especialidade):
        if especialidade not in self.especialidades:
            self.especialidades.append(especialidade)

    def adicionar_consulta(self, consulta):
        self.consultas.append(consulta)

    def listar_especialidades(self):
        return ", ".join(e.nome for e in self.especialidades)


class Recepcionista(Pessoa):
    def __init__(self, nome, cpf, telefone, matricula):
        super().__init__(nome, cpf, telefone)
        self.matricula = matricula

    def apresentar(self):
        return f"Recepcionista: {self.nome} - Matrícula: {self.matricula}"


class Consulta:
    STATUS = ("Agendada", "Realizada", "Cancelada")

    def __init__(self, paciente, medico, data_hora):
        self.paciente = paciente
        self.medico = medico
        self.data_hora = data_hora
        self._status = "Agendada"

    @property
    def status(self):
        return self._status

    def alterar_status(self, novo_status):
        if novo_status not in self.STATUS:
            raise ValueError("Status inválido.")
        self._status = novo_status


class Atendimento:
    contador = 0

    def __init__(self, consulta, descricao):
        Atendimento.contador += 1
        self.numero = Atendimento.contador
        self.consulta = consulta
        self.descricao = descricao

    def finalizar(self):
        self.consulta.alterar_status("Realizada")


class Clinica:
    def __init__(self, nome):
        self.nome = nome
        self.pacientes = []
        self.medicos = []
        self.recepcionistas = []
        self.especialidades = []
        self.consultas = []
        self.atendimentos = []

    def cadastrar_paciente(self, paciente):
        if not self.validar_cpf(paciente.cpf):
            raise ErroClinica("CPF inválido.")
        self.pacientes.append(paciente)

    def cadastrar_medico(self, medico):
        if not self.validar_cpf(medico.cpf):
            raise ErroClinica("CPF inválido.")
        self.medicos.append(medico)

    def cadastrar_recepcionista(self, recepcionista):
        if not self.validar_cpf(recepcionista.cpf):
            raise ErroClinica("CPF inválido.")
        self.recepcionistas.append(recepcionista)

    def cadastrar_especialidade(self, especialidade):
        self.especialidades.append(especialidade)

    def agendar_consulta(self, paciente, medico, data_hora):
        for consulta in self.consultas:
            if consulta.status == "Cancelada":
                continue

            if consulta.data_hora == data_hora:
                if consulta.paciente == paciente:
                    raise HorarioOcupadoError(
                        "O paciente já possui uma consulta nesse horário."
                    )

                if consulta.medico == medico:
                    raise HorarioOcupadoError(
                        "O médico já possui uma consulta nesse horário."
                    )

        consulta = Consulta(paciente, medico, data_hora)

        self.consultas.append(consulta)
        paciente.adicionar_consulta(consulta)
        medico.adicionar_consulta(consulta)

        return consulta

    def criar_atendimento(self, consulta, descricao):
        if consulta.status == "Cancelada":
            raise ErroClinica(
                "Não é possível atender uma consulta cancelada."
            )

        atendimento = Atendimento(consulta, descricao)
        self.atendimentos.append(atendimento)
        atendimento.finalizar()

        return atendimento

    def cancelar_consulta(self, consulta):
        if consulta.status == "Realizada":
            raise ErroClinica(
                "Uma consulta realizada não pode ser cancelada."
            )

        consulta.alterar_status("Cancelada")

    @staticmethod
    def validar_cpf(cpf):
        cpf = cpf.replace(".", "").replace("-", "")
        return len(cpf) == 11 and cpf.isdigit()

    @classmethod
    def criar_clinica_padrao(cls):
        clinica = cls("Clínica Fácil")

        for nome in ["Cardiologia", "Pediatria", "Dermatologia", "Clínica Geral"]:
            clinica.cadastrar_especialidade(Especialidade(nome))

        return clinica


class ClinicaApp:
    def __init__(self, janela):
        self.clinica = Clinica.criar_clinica_padrao()
        self.janela = janela

        self.janela.title("Clínica Fácil - Gestão de Clínica")
        self.janela.geometry("1050x650")
        self.janela.minsize(900, 600)

        self.configurar_estilo()
        self.criar_interface()
        self.atualizar_tabelas()

    def configurar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "TNotebook",
            background="#f1f5f9",
            borderwidth=0
        )

        estilo.configure(
            "TNotebook.Tab",
            padding=[15, 8],
            font=("Arial", 10, "bold")
        )

        estilo.configure(
            "Treeview",
            rowheight=30,
            font=("Arial", 10)
        )

        estilo.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    def criar_interface(self):
        titulo = tk.Label(
            self.janela,
            text="CLÍNICA FÁCIL",
            font=("Arial", 24, "bold"),
            bg="#0f172a",
            fg="white",
            pady=15
        )
        titulo.pack(fill="x")

        subtitulo = tk.Label(
            self.janela,
            text="Sistema de Gestão de Clínica",
            font=("Arial", 11),
            bg="#0f172a",
            fg="#cbd5e1",
            pady=0
        )
        subtitulo.pack(fill="x")

        self.abas = ttk.Notebook(self.janela)
        self.abas.pack(fill="both", expand=True, padx=15, pady=15)

        self.aba_inicio = ttk.Frame(self.abas)
        self.aba_pacientes = ttk.Frame(self.abas)
        self.aba_medicos = ttk.Frame(self.abas)
        self.aba_consultas = ttk.Frame(self.abas)
        self.aba_atendimentos = ttk.Frame(self.abas)

        self.abas.add(self.aba_inicio, text="Início")
        self.abas.add(self.aba_pacientes, text="Pacientes")
        self.abas.add(self.aba_medicos, text="Médicos")
        self.abas.add(self.aba_consultas, text="Consultas")
        self.abas.add(self.aba_atendimentos, text="Atendimentos")

        self.criar_inicio()
        self.criar_pacientes()
        self.criar_medicos()
        self.criar_consultas()
        self.criar_atendimentos()

    def criar_inicio(self):
        frame = ttk.Frame(self.aba_inicio, padding=30)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Bem-vindo à Clínica Fácil",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        tk.Label(
            frame,
            text="Sistema para gerenciamento de pacientes, médicos,\n"
                 "especialidades, consultas e atendimentos.",
            font=("Arial", 12),
            justify="center"
        ).pack(pady=10)

        self.lbl_resumo = tk.Label(
            frame,
            text="",
            font=("Arial", 12),
            justify="center"
        )
        self.lbl_resumo.pack(pady=30)

        tk.Button(
            frame,
            text="Atualizar informações",
            command=self.atualizar_resumo,
            padx=15,
            pady=8
        ).pack()

        self.atualizar_resumo()

    def atualizar_resumo(self):
        self.lbl_resumo.config(
            text=(
                f"Pacientes cadastrados: {len(self.clinica.pacientes)}\n"
                f"Médicos cadastrados: {len(self.clinica.medicos)}\n"
                f"Consultas cadastradas: {len(self.clinica.consultas)}\n"
                f"Atendimentos realizados: {len(self.clinica.atendimentos)}"
            )
        )

    def criar_pacientes(self):
        formulario = ttk.LabelFrame(
            self.aba_pacientes,
            text="Cadastrar paciente",
            padding=15
        )
        formulario.pack(fill="x", padx=15, pady=15)

        self.paciente_nome = self.criar_campo(formulario, "Nome:", 0)
        self.paciente_cpf = self.criar_campo(formulario, "CPF:", 1)
        self.paciente_telefone = self.criar_campo(formulario, "Telefone:", 2)
        self.paciente_nascimento = self.criar_campo(
            formulario, "Nascimento:", 3
        )

        ttk.Button(
            formulario,
            text="Cadastrar paciente",
            command=self.cadastrar_paciente
        ).grid(row=4, column=0, columnspan=2, pady=10)

        tabela_frame = ttk.Frame(self.aba_pacientes)
        tabela_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.tabela_pacientes = ttk.Treeview(
            tabela_frame,
            columns=("nome", "cpf", "telefone", "nascimento"),
            show="headings"
        )

        for coluna, texto in [
            ("nome", "Nome"),
            ("cpf", "CPF"),
            ("telefone", "Telefone"),
            ("nascimento", "Nascimento")
        ]:
            self.tabela_pacientes.heading(coluna, text=texto)
            self.tabela_pacientes.column(coluna, width=180)

        self.tabela_pacientes.pack(fill="both", expand=True)

    def criar_medicos(self):
        formulario = ttk.LabelFrame(
            self.aba_medicos,
            text="Cadastrar médico",
            padding=15
        )
        formulario.pack(fill="x", padx=15, pady=15)

        self.medico_nome = self.criar_campo(formulario, "Nome:", 0)
        self.medico_cpf = self.criar_campo(formulario, "CPF:", 1)
        self.medico_telefone = self.criar_campo(formulario, "Telefone:", 2)
        self.medico_crm = self.criar_campo(formulario, "CRM:", 3)

        ttk.Label(formulario, text="Especialidade:").grid(
            row=0, column=2, padx=5, pady=5, sticky="e"
        )

        self.medico_especialidade = ttk.Combobox(
            formulario,
            state="readonly",
            width=25
        )
        self.medico_especialidade.grid(
            row=0, column=3, padx=5, pady=5
        )

        ttk.Button(
            formulario,
            text="Cadastrar médico",
            command=self.cadastrar_medico
        ).grid(row=4, column=0, columnspan=4, pady=10)

        tabela_frame = ttk.Frame(self.aba_medicos)
        tabela_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.tabela_medicos = ttk.Treeview(
            tabela_frame,
            columns=("nome", "crm", "especialidade"),
            show="headings"
        )

        for coluna, texto in [
            ("nome", "Nome"),
            ("crm", "CRM"),
            ("especialidade", "Especialidade")
        ]:
            self.tabela_medicos.heading(coluna, text=texto)
            self.tabela_medicos.column(coluna, width=250)

        self.tabela_medicos.pack(fill="both", expand=True)

    def criar_consultas(self):
        formulario = ttk.LabelFrame(
            self.aba_consultas,
            text="Agendar consulta",
            padding=15
        )
        formulario.pack(fill="x", padx=15, pady=15)

        ttk.Label(formulario, text="Paciente:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )

        self.consulta_paciente = ttk.Combobox(
            formulario,
            state="readonly",
            width=28
        )
        self.consulta_paciente.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Médico:").grid(
            row=0, column=2, padx=5, pady=5, sticky="e"
        )

        self.consulta_medico = ttk.Combobox(
            formulario,
            state="readonly",
            width=28
        )
        self.consulta_medico.grid(row=0, column=3, padx=5, pady=5)

        self.consulta_data = self.criar_campo(
            formulario, "Data (DD/MM/AAAA):", 1, 0
        )

        self.consulta_hora = self.criar_campo(
            formulario, "Hora (HH:MM):", 1, 2
        )

        ttk.Button(
            formulario,
            text="Agendar consulta",
            command=self.agendar_consulta
        ).grid(row=2, column=0, columnspan=4, pady=10)

        tabela_frame = ttk.Frame(self.aba_consultas)
        tabela_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.tabela_consultas = ttk.Treeview(
            tabela_frame,
            columns=(
                "paciente",
                "medico",
                "data",
                "hora",
                "status"
            ),
            show="headings"
        )

        for coluna, texto in [
            ("paciente", "Paciente"),
            ("medico", "Médico"),
            ("data", "Data"),
            ("hora", "Hora"),
            ("status", "Status")
        ]:
            self.tabela_consultas.heading(coluna, text=texto)
            self.tabela_consultas.column(coluna, width=150)

        self.tabela_consultas.pack(fill="both", expand=True)

        botoes = ttk.Frame(self.aba_consultas)
        botoes.pack(pady=10)

        ttk.Button(
            botoes,
            text="Cancelar consulta selecionada",
            command=self.cancelar_consulta
        ).pack(side="left", padx=5)

    def criar_atendimentos(self):
        formulario = ttk.LabelFrame(
            self.aba_atendimentos,
            text="Registrar atendimento",
            padding=15
        )
        formulario.pack(fill="x", padx=15, pady=15)

        ttk.Label(formulario, text="Consulta:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )

        self.atendimento_consulta = ttk.Combobox(
            formulario,
            state="readonly",
            width=70
        )
        self.atendimento_consulta.grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(formulario, text="Descrição:").grid(
            row=1, column=0, padx=5, pady=5, sticky="ne"
        )

        self.atendimento_descricao = tk.Text(
            formulario,
            width=60,
            height=5
        )
        self.atendimento_descricao.grid(
            row=1, column=1, padx=5, pady=5
        )

        ttk.Button(
            formulario,
            text="Finalizar atendimento",
            command=self.criar_atendimento
        ).grid(row=2, column=0, columnspan=2, pady=10)

        tabela_frame = ttk.Frame(self.aba_atendimentos)
        tabela_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.tabela_atendimentos = ttk.Treeview(
            tabela_frame,
            columns=("numero", "paciente", "medico", "descricao"),
            show="headings"
        )

        for coluna, texto in [
            ("numero", "Nº"),
            ("paciente", "Paciente"),
            ("medico", "Médico"),
            ("descricao", "Descrição")
        ]:
            self.tabela_atendimentos.heading(coluna, text=texto)
            self.tabela_atendimentos.column(coluna, width=180)

        self.tabela_atendimentos.pack(fill="both", expand=True)

    def criar_campo(self, frame, texto, linha, coluna=0):
        ttk.Label(frame, text=texto).grid(
            row=linha,
            column=coluna,
            padx=5,
            pady=5,
            sticky="e"
        )

        entrada = ttk.Entry(frame, width=28)
        entrada.grid(
            row=linha,
            column=coluna + 1,
            padx=5, 
        )