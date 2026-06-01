import ast
from enum import Enum
from typing import Any

from App import sort_count as sc
from App import sort_count_util as scu


class CliCommand(Enum):
    EXIT = 0
    SET_LIST = 1
    TOGGLE_COUNT = 2
    TOGGLE_SPEARMAN = 3
    TOGGLE_TAU = 4
    SHOW = 5


class Cli:
    def __init__(self):
        self.current_list: list[Any] = []
        self.show_count: bool = False
        self.show_spearman: bool = False
        self.show_tau: bool = False

    @staticmethod
    def query_list(msg: str) -> list[Any]:
        # Rotina de leitura de lista do usuário.
        # Aceita tanto uma representação literal de lista (ex: [1, 2, 3]) quanto
        # uma lista de itens separados por vírgula (ex: 1, 2, 3).
        raw_items = input(msg).strip()
        if raw_items == "":
            return []

        if raw_items.startswith("[") and raw_items.endswith("]"):
            parsed = ast.literal_eval(raw_items)
            if not isinstance(parsed, list):
                raise ValueError("A entrada deve ser uma lista.")
            return parsed

        tokens = raw_items.split(",")
        if any(token.strip() == "" for token in tokens):
            raise ValueError("Itens vazios não são permitidos.")

        parsed_items: list[Any] = []
        for token in tokens:
            stripped_token = token.strip()
            try:
                parsed_items.append(ast.literal_eval(stripped_token))
            except (ValueError, SyntaxError):
                parsed_items.append(stripped_token)
        return parsed_items

    def query_list_for_set(self):
        try:
            self.current_list = self.query_list("Digite os itens da nova lista: ")
        except Exception as e:
            print(
                f"Erro de leitura: {str(e)}. A entrada deve ser uma lista de itens, por exemplo: [1, 2, 3]. Tente novamente."
            )

    def show_menu_and_query_commands(self) -> CliCommand:
        print("Opções atuais:")
        print("========================================")
        print(f"Lista atual: {self.current_list}")
        print(f"Contagem de inversões: {'ON' if self.show_count else 'OFF'}")
        print(f"Índice de Spearman: {'ON' if self.show_spearman else 'OFF'}")
        print(f"Índice Tau de Kendall: {'ON' if self.show_tau else 'OFF'}")
        print("========================================")
        print("Selecione uma ação:")
        print("========================================")
        print("1. Definir nova lista")
        print("2. Alternar exibição da contagem de inversões")
        print("3. Alternar exibição do índice de Spearman")
        print("4. Alternar exibição do índice Tau de Kendall")
        print("5. Computar e mostrar resultados")
        print("0. Sair")
        print("========================================")
        return CliCommand(int(input("Digite o número da ação desejada: ")))

    def main(self):
        while True:
            command = self.show_menu_and_query_commands()
            if command == CliCommand.EXIT:
                # print("Encerrando o programa. Até mais!")
                break
            elif command == CliCommand.SET_LIST:
                self.query_list_for_set()
            elif command == CliCommand.TOGGLE_COUNT:
                self.show_count = not self.show_count
            elif command == CliCommand.TOGGLE_SPEARMAN:
                self.show_spearman = not self.show_spearman
            elif command == CliCommand.TOGGLE_TAU:
                self.show_tau = not self.show_tau
            elif command == CliCommand.SHOW:
                try:
                    inv_num, sorted_list = sc.SortCount.run(self.current_list)
                    if self.show_count:
                        print(f"Contagem de inversões: {inv_num}")
                    if self.show_spearman:
                        rs = scu.SortCountUtil.spearman(self.current_list)
                        print(f"Índice de Spearman: {rs:.4f}")
                    if self.show_tau:
                        tau = scu.SortCountUtil.kendall_tau_2(
                            inv_num, len(self.current_list)
                        )
                        print(f"Índice Tau de Kendall: {tau:.4f}")
                    print("========================================")
                    print(f"Lista ordenada: {sorted_list}")
                    print("========================================")
                except Exception as e:
                    print(
                        f"Erro ao computar resultados: {str(e)}. Verifique se a lista atual é válida e tente novamente."
                    )
