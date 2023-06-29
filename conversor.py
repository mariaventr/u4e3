import requests
from tkinter import *
from tkinter import ttk, messagebox

class Conversor:
    __ventana=None
    def __init__(self):
        self.__ventana=Tk()
        self.__ventana.geometry('290x115')
        self.__ventana.resizable(0,0)
        self.__ventana.title("Conversor de moneda")

        mainframe = ttk.Frame(self.__ventana, padding="5 5 12 5")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe['borderwidth'] = 2
        mainframe['relief'] = 'sunken'

        self.__dolares = StringVar()
        self.__pesos = StringVar()
        self.__dolares.trace('w', self.calcular)

        self.entry_Dolar=ttk.Entry(mainframe, width=7, textvariable=self.__dolares)
        opts={"ipady":10, "ipadx":10}
        self.entry_Dolar.grid(row=1, column=2, sticky=(W,E))
        ttk.Label(mainframe, text="dólares").grid(row=1, column=3, sticky=W, **opts)

        ttk.Label(mainframe,textvariable=self.__pesos).grid(row=2, column=2, sticky=(W,E))
        ttk.Label(mainframe,text="pesos").grid(row=2, column=3, sticky=W)
        ttk.Label(mainframe,text="es equivalente a").grid(row=2, column=0, sticky=E)
        ttk.Button(mainframe,text="salir", command=self.salir).grid(row=3, column=3, sticky=W)

        for hijo in mainframe.winfo_children():
            hijo.grid_configure(padx=3, pady=3)

        self.entry_Dolar.focus()

    def obtener_cotizacion_dolar(self):
        try:
            response = requests.get('https://www.dolarsi.com/api/api.php?type=dolar')
            data = response.json()
            cotizacion = float(data[0]['casa']['venta'].replace(',', '.'))
            return cotizacion
        except:
            messagebox.showerror(title="Error", message="No se pudo obtener la cotización del dólar")
            return None
    
    def calcular(self, *args):
        if self.entry_Dolar.get() != "":
            try:
                valor = float(self.entry_Dolar.get())
                cotizacion = self.obtener_cotizacion_dolar()
                if cotizacion is not None:
                    self.__pesos.set(valor * cotizacion)
            except ValueError:
                messagebox.showerror(title="Error de tipo", message="Debe Ingresar un valor numérico")
                self.__dolares.set("")
                self.entry_Dolar.focus()
        else:
            self.__pesos.set("")

    def salir(self):
        self.__ventana.destroy()

    def ejecutar(self):
        self.__ventana.mainloop()

if __name__ == "__main__":
    ventana=Conversor()
    ventana.ejecutar()
