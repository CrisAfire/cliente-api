import requests
from tkinter import *

url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&"

def consultar_API(inicio, fin, panel_resultados):
    #Borrar resultados previos
    for resultado in panel_resultados.winfo_children():
        resultado.destroy()

    consulta = requests.get(url + f'starttime={inicio.get()}&endtime={fin.get()}')

    terremotos = consulta.json()

    cuenta = 1
    for terremoto in terremotos['features']:
        Label(panel_resultados, 
        text=f"{cuenta}.- En {terremoto['properties']['place']} ({terremoto['geometry']['coordinates'][0]}, {terremoto['geometry']['coordinates'][1]}). Magnitud: {terremoto['properties']['mag']}").pack(pady=5)
        cuenta = cuenta + 1
        if cuenta == 1050:
            break

def configurar_ventana(ventana):
    ventana.title("Cliente de una API")
    ventana.geometry('600x600')

    frame = Frame(ventana)
    frame.grid(row=0, column=0, sticky="nsew")

    ventana.grid_rowconfigure(0, weight=1)
    ventana.grid_columnconfigure(0, weight=1)

    lbl_titulo = Label(frame, text="API de Terremotos de la USGS")
    lbl_titulo.grid(column=0, row=0, columnspan=2, pady=10, sticky="ew")

    panel_fechas = Frame(frame)
    panel_fechas.grid(row=1, column=0, padx=100, pady=[20, 0], columnspan=2, sticky="nsew")

    Label(panel_fechas, text='Fecha de inicio').grid(column=0, row=0, sticky="w")
    Label(panel_fechas, text='Fecha de fin').grid(column=0, row=1, sticky="w")

    inicio = Entry(panel_fechas)
    inicio.grid(column=1, row=0, sticky="ew")
    inicio.insert(0, "2014-01-01")
    fin = Entry(panel_fechas)
    fin.grid(column=1, row=1, sticky="ew")
    fin.insert(0, "2014-01-02")

    panel_fechas.grid_rowconfigure(0, weight=0)  #Fecha inicio
    panel_fechas.grid_rowconfigure(1, weight=0)  #Fecha fin
    panel_fechas.grid_columnconfigure(0, weight=1)  #Izq
    panel_fechas.grid_columnconfigure(1, weight=1)  #Der

    canvas = Canvas(frame)
    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    panel_resultados = Frame(canvas, bg="lightgray")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.create_window((0, 0), window=panel_resultados, anchor="nw")

    panel_resultados.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.grid(row=3, column=0, columnspan=2, sticky="nsew")
    scrollbar.grid(row=3, column=2, sticky="ns")  

    btn_consultar = Button(frame, text='Consultar', width=25, command= lambda: consultar_API(inicio, fin, panel_resultados))
    btn_consultar.grid(row=2, column=0, columnspan=2, pady=20)

    frame.grid_rowconfigure(0, weight=0)  #Título
    frame.grid_rowconfigure(1, weight=0)  #Panel fechas
    frame.grid_rowconfigure(2, weight=0)  #Btn consultar
    frame.grid_rowconfigure(3, weight=1)  #Resultados
    frame.grid_columnconfigure(0, weight=1)  #Izq
    frame.grid_columnconfigure(1, weight=1)  #Der

def __main__():
    ventana = Tk()
    configurar_ventana(ventana)
    ventana.mainloop()

__main__()