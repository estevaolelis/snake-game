import json
import os

class GerenciadorRecordes:
    def __init__(self, arquivo="recordes.json"):
        """Inicializa o gerenciador e carrega os recordes salvos."""
        self.arquivo = arquivo
        self.recordes = self.carregar_recordes()

    def carregar_recordes(self):
        """Lê o arquivo JSON ou cria uma lista padrão caso ele não exista."""
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return self._recordes_padrao()
        return self._recordes_padrao()

    def _recordes_padrao(self):
        """Retorna uma lista de 5 recordes zerados para a primeira vez que o jogo abrir."""
        return [{"nome": "AAA", "pontuacao": 0} for _ in range(5)]

    def salvar_recordes(self):
        """Salva a lista atual de recordes no arquivo JSON."""
        with open(self.arquivo, 'w') as f:
            json.dump(self.recordes, f, indent=4)

    def eh_novo_recorde(self, pontuacao):
        """Verifica se a pontuação atingida é maior que a do quinto colocado."""
        return pontuacao > self.recordes[-1]["pontuacao"]

    def adicionar_recorde(self, nome, pontuacao):
        """Adiciona o novo recorde, ordena a lista e descarta o sexto colocado."""
        self.recordes.append({"nome": nome, "pontuacao": pontuacao})
        
        # Ordena a lista baseada no valor da pontuação em ordem decrescente
        self.recordes.sort(key=lambda x: x["pontuacao"], reverse=True)
        
        # Corta a lista para manter estritamente os 5 primeiros
        self.recordes = self.recordes[:5]
        self.salvar_recordes()