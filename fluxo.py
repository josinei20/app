import pandas as pd
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

# Função para carregar os dados do arquivo Excel
def load_data(file_path):
    """Carrega os dados do arquivo CSV e retorna um DataFrame pandas."""
    try:
        df = pd.read_excel('Pasta 13.xlsx')
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        return None
    except pd.errors.ParserError:
        print(f"Erro: Falha ao analisar o arquivo '{file_path}'. Verifique o formato.")
        return None

# Função para buscar dados no DataFrame
def search_data(df, nf_number):
    """Busca a NF no DataFrame e retorna as informações do produto, baia, cliente e data."""
    try:
        nf_number = int(nf_number)  # Converte para inteiro
        result = df[df['NF'] == nf_number]
        if not result.empty:
            bay = result.iloc[0]['IT / BAIA']
            product = result.iloc[0]['PRODUTO']
            client = result.iloc[0]['CLIENTE']
            date = result.iloc[0]['DATA']
            return f"PRODUTO: {product}\nCLIENTE: {client}\nBaia: {bay}\nData: {date}"
        else:
            return "NF não encontrada."
    except ValueError:
        return "NF inválida. Digite um número."

# Layout em KV para o KivyMD
KV = '''
ScreenManager:
    SearchScreen:

<SearchScreen>:
    name: 'search'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: "Consulta de NF"
            halign: "center"
            theme_text_color: "Primary"
            font_style: "H4"
            size_hint_y: None
            height: "40dp"

        MDTextField:
            id: nf_input
            hint_text: "Digite o número da NF"
            icon_right: "barcode"
            size_hint_x: None
            width: "280dp"
            pos_hint: {"center_x": 0.5}

        MDRaisedButton:
            text: "Buscar"
            pos_hint: {"center_x": 0.5}
            on_release: app.search_nf()

        MDLabel:
            id: result_label
            text: ""
            halign: "center"
            theme_text_color: "Secondary"
            font_style: "H6"
            size_hint_y: None
            height: "80dp"
'''

# Telas do aplicativo
class SearchScreen(Screen):
    pass

class SearchApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(SearchScreen(name='search'))
        return Builder.load_string(KV)

    def search_nf(self):
        nf_number = self.root.get_screen('search').ids.nf_input.text.strip()
        df = load_data("Pasta 13.xlsx")  # Substitua pelo caminho do seu arquivo

        if df is not None:
            result = search_data(df, nf_number)
            self.root.get_screen('search').ids.result_label.text = result
        else:
            self.show_dialog("Erro", "Não foi possível carregar os dados.")

    def show_dialog(self, title, text):
        """Exibe um diálogo de erro."""
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

if __name__ == '__main__':
    SearchApp().run()
