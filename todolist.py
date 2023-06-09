import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget
import mysql.connector

class Tarefas(QWidget):
    def __init__(self):
        super().__init__()

        # Conexão ao banco de dados
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="todolist_python"
        )
        self.criar_tabela()

        # Definição dos elementos da interface
        self.label = QLabel('Adicionar tarefa:')
        self.input = QLineEdit()
        self.botao = QPushButton('Adicionar')
        self.lista_tarefas = QListWidget()
        self.lista_tarefas.addItems(self.listar_tarefas())

        # Definição dos layouts
        layout_v = QVBoxLayout()
        layout_v.addWidget(self.label)
        layout_v.addWidget(self.input)

        layout_h = QHBoxLayout()
        layout_h.addWidget(self.botao)

        layout_v.addLayout(layout_h)
        layout_v.addWidget(self.lista_tarefas)

        # Conexão dos elementos à função de adicionar tarefa
        self.botao.clicked.connect(self.adicionar_tarefa)
        self.input.returnPressed.connect(self.adicionar_tarefa)

        # Definição do layout principal
        self.setLayout(layout_v)

    def criar_tabela(self):
        # Criação da tabela 'tarefas', se ela ainda não existir
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tarefas
               (ID INT PRIMARY KEY AUTO_INCREMENT,
               DESCRICAO VARCHAR(255) NOT NULL,
               FEITA BOOLEAN NOT NULL DEFAULT 0);''')
        self.conn.commit()

    def adicionar_tarefa(self):
        # Inserção de tarefa na tabela
        descricao = self.input.text()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tarefas (DESCRICAO, FEITA) VALUES (%s, 0)", (descricao,))
        self.input.clear()
        self.conn.commit()
        self.lista_tarefas.clear()
        self.lista_tarefas.addItems(self.listar_tarefas())

    def listar_tarefas(self):
        # Consulta de tarefas na tabela
        cursor = self.conn.cursor()
        cursor.execute("SELECT ID, DESCRICAO, FEITA from tarefas")
        tarefas = []
        for row in cursor:
            tarefa = f"{row[1]} (ID: {row[0]})"
            if row[2]:
                tarefa += " - Feita"
            tarefas.append(tarefa)
        return tarefas

    def closeEvent(self, event):
        # Fechamento da conexão com o banco de dados ao encerrar o programa
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tarefas = Tarefas()
    tarefas.show()
    sys.exit(app.exec_())