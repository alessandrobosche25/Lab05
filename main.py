import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    alert = AlertManager(page)

    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")

    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    input_tipo = ft.TextField(label="Tipo")
    input_marca = ft.TextField(label="Marca")
    input_anno = ft.TextField(label="Anno di acquisto")
    input_valore = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    def decrementa_valore(e):
        input_valore.value = str(int(input_valore.value) - 1)

    def incrementa_valore(e):
        input_valore.value = str(int(input_valore.value) + 1)

    def handler_aggiungi_strumento(e):
        try:
            anno = int(input_anno.value)
        except ValueError:
            alert.show_alert("❌ L'anno di acquisto deve essere un numero intero")
            return
        try:
            valore = float(input_valore.value)
        except ValueError:
            alert.show_alert("❌ Il valore deve essere un numero")
            return

        deposito.aggiungi_strumento(input_tipo.value, input_marca.value, anno, valore)

        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        input_valore.value = "0"

        aggiorna_lista_strumenti()

    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    pulsante_meno = ft.IconButton(icon=ft.Icons.REMOVE, on_click=decrementa_valore)
    pulsante_piu = ft.IconButton(icon=ft.Icons.ADD, on_click=incrementa_valore)
    pulsante_aggiungi = ft.Button("Aggiungi strumento", on_click=handler_aggiungi_strumento)

    page.add(
        toggle_cambia_tema,

        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        ft.Row(controls=[input_tipo, input_marca, input_anno],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=[pulsante_meno, input_valore, pulsante_piu],
               alignment=ft.MainAxisAlignment.CENTER),
        pulsante_aggiungi,

        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)