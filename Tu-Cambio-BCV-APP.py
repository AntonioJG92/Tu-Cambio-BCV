# Aplicación de escritorio para calcular la conversión de $ a Bs y viceversa,
# utilizando la tasa de cambio del Banco central de Venezuela.

# Autor: Antonio Gamboa.

#--- Importaciones.

# Se importa módulo para trabajar con interfaces gráficas.
import sys
from tkinter import *
from tkinter import messagebox

# Se importa módulo para trabajar con imágenes Base64.
from base64 import b64decode

# Se importa módulo necesario para buscar información en páginas web.
from bs4 import BeautifulSoup 

# Se importa módulo para hacer peticiones HTTP.
import requests

#---

# --- Clases para excepciones personalizadas.

# Clase para controlar excepciones para el valor del $ mayor a 1,000,000.00 $.
class dolarmayorException(Exception):
     
     pass

# Clase para controlar excepciones para el valor de Bs mayor a 1,000,000.00 Bs.
class bolivarmayorException(Exception):
     
     pass

#---

# Bloques para excepciones en petición HTTP.
try:
    
    # OJO: Se puede extraer información de una página WEB con requests y BeautifulSoup.  
    # Se hace la petición para guardar la página HTML completa de prueba solicitada.
    # Se desactiva la verificación del certificado SSL.
    miDoc=requests.get("https://www.bcv.org.ve/",verify=False)

except:
    
    # Se muestra ventana emergente en caso de no estár conectado a internet.
    messagebox.showerror("Error", "Debe conectarse a Internet!")

    # Se finaliza la ejecución.
    sys.exit()


# Se guarda el texto de la página HTML de prueba con BeautifulSoup.
docFinal=BeautifulSoup(miDoc.text,"html.parser")

# Se guarda información sobre el precio del USD.
lista=docFinal.select(".col-sm-12.col-xs-12")

# Se guarda información sobre la fecha de cambio actual.
lista2=docFinal.select(".date-display-single")

# Fecha de cambio actual.
fechaCambio= lista2[0].text

# Lista que contiene el valor de la tasa de cambio de la divisa sin formatear.
divisa=lista[7].text

# Se crea nueva lista para guardar el valor de la tasa de cambio de la divisa ya formateado.
newdivisa=[] 

# Bucle para recorrer la lista divisa desde y hasta las posiciones que contienen el valor de la tasa de cambio de la divisa.
for  i in range(12,23):
    
    # Agregamos cada elemento del valor de la tasa de cambio de la divisa a la nueva lista.
    newdivisa.append(divisa[i])

# Reemplazamos la "," por un "." para poder realizar posteriormente una conversión a float.
newdivisa[2]="."

# Convertimos la lista con el valor de la tasa de cambio de la divisa a un String.
valorDivisaString=''.join(newdivisa)

# Convertimos el valor de la tasa de cambio de la divisa en String a float para poder hacer cálculos.
valorDivisaFinal=float(valorDivisaString)


#--- Creación GUI.

# Creo raíz para la interfaz.
# Ojo: Respetar mayúsculas y minúsculas para "Tk()".
root=Tk()

# Desactivamos la redimensión del root.
root.resizable(0,0)

# 07/12/2023.

# Dimensiones de la ventana.
width=400
height=400

# Se obtiene las dimensiones de la pantalla.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Se calcula la posición x e y para centrar la ventana.
position_x = int(screen_width / 2 - width / 2)
position_y = int(screen_height / 2 - height / 2)

# Se configura la geometría de la ventana.
root.geometry(f'{width}x{height}+{position_x}+{position_y}')

# Cambiamos título de la ventana.
root.title("Tu Cambio BCV")

# Cambiamos icono de la ventana.

# Variable con datos del ícono en Base64.
icon="""
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
"""

# Se decodifican los datos del ícono y se guardan.
icon=b64decode(icon)

# Se convierte variable con datos del ícono a objeto PhotoImage.
icon=PhotoImage(data=icon)

# Se carga ícono a la ventana.
root.iconphoto(False, icon)

# Creo Frame que recibe como parámetros la clase padre (El contenedor), y dimensiones de la ventana.
miFrame=Frame(root, width=400, height=400)

# Empaquetamos el Frame dentro del root.
miFrame.pack()

# Creamos Label para Título.
tituloLabel=Label(miFrame, text="Tu Cambio BCV")

# Cambiamos fuente y tamaño de la letra.
tituloLabel.config(font=("Roboto",18,"bold"))

# Ubicamos label para Título.
tituloLabel.place(x=115,y=25)

# Creamos label para fecha de la tasa de cambio.
fechaTasaCambioLabel=Label(miFrame,text="Fecha Valor: " + fechaCambio)

# Cambiamos fuente y tamaño de la letra.
fechaTasaCambioLabel.config(font=("Roboto",12,"bold"))

# Ubicamos Label para fecha.
fechaTasaCambioLabel.place(x=60, y=80)
 
# Creamos label para tasa de cambio.
tasaCambioLabel=Label(miFrame,text="La tasa de cambio es: {:.4f} ".format(valorDivisaFinal) + " Bs/$")

# Cambiamos fuente y tamaño de la letra.
tasaCambioLabel.config(font=("Roboto",12,"bold"))

# Ubicamos label para tasa de cambio.
tasaCambioLabel.place(x=60, y=105)

# Creo label para valor en dolar para conversión.
valorDolarLabel=Label(miFrame, text="Inserte valor en $ para conversión:")

# Cambiamos fuente y tamaño de la letra.
valorDolarLabel.config(font=("Roboto",11,"bold"))

# Ubicamos label para valor en $ a convertir.
valorDolarLabel.place(x=30, y=150)

# Creo label para valor en Bs para conversión.
valorBolivarLabel=Label(miFrame, text="Inserte valor en Bs para conversión:")

# Cambiamos fuente y tamaño de la letra.
valorBolivarLabel.config(font=("Roboto",11,"bold"))

# Ubicamos label para valor en Bs a convertir.
valorBolivarLabel.place(x=30, y=185)

# Creo label para mostrar resultado en Bs.
resultadoLabel=Label(miFrame)

# Ubicamos label para mostrar resultado en Bs.
resultadoLabel.place(x=25, y=290)

# Cambiamos fuente y tamaño de la letra.
resultadoLabel.config(font=("Roboto",12, "bold"))

# Creo label para mostrar resultado en $.
resultado2Label=Label(miFrame)

# Ubicamos label para mostrar resultado en $.
resultado2Label.place(x=25, y=330)

# Cambiamos fuente y tamaño de la letra.
resultado2Label.config(font=("Roboto",12, "bold"))

# Creo label para mostrar nombre del autor.
autorLabel=Label(miFrame, text="GitHub: antoniojg92 | Hive: antoniojg")

# Ubicamos label para mostrar nombre del autor.
autorLabel.place(x=10, y=375)

# Cambiamos fuente y tamaño de la letra.
autorLabel.config(font=("Roboto",11,"bold"))

# Objeto valorDolar.
valorDolar=DoubleVar(value=1.00)

# Creamos Entry para leer valor en $ de la interfaz.
cuadroTextoEntryDolar=Entry(miFrame, textvariable=valorDolar)

# Ubicamos Entry para leer valor en $ de la interfaz.
cuadroTextoEntryDolar.place(x=295, y=153, width=65 )

# Cambiamos fuente y tamaño de la letra.
cuadroTextoEntryDolar.config(font=("Roboto",10,"bold"))

# Objeto valorBolivar.
valorBolivar=DoubleVar(value=1.00)

# Creamos Entry para leer valor en Bs de la interfaz.
cuadroTextoEntryBolivar=Entry(miFrame, textvariable=valorBolivar)

# Ubicamos Entry para leer valor en Bs de la interfaz.
cuadroTextoEntryBolivar.place(x=295, y=185, width=65 )

# Cambiamos fuente y tamaño de la letra.
cuadroTextoEntryBolivar.config(font=("Segoe",10,"bold"))

# Se crea acción a realizar para evento del botón.
# función para calculo de conversión.
def funcionBoton():

    # Bloques para excepciones.
    try: 
        
         # Condición para controlar que valor introducido en $ sea menor o igual a 1,000,000.00 $ .
         if float(valorDolar.get())>(1000000):
                
                # Lanzamos excepción para controlar error.
                raise dolarmayorException
         
         # Condición para controlar que valor introducido en Bs sea menor o igual a 1,000,000.00 Bs.
         if float(valorBolivar.get())>(1000000): 
              
                # Lanzamos excepción para controlar error.
                raise bolivarmayorException

         # Calculamos el valor final en $ de acuerdo a tasa de cambio actual.
         totalConversion=float(valorDolar.get())*valorDivisaFinal 

         # Calculamos el valor final en Bs de acuerdo a tasa de cambio actual.
         totalConversion2=float(valorBolivar.get())/valorDivisaFinal 

         # Guardamos resultado de conversión en label para mostrar resultado de conversión $ a Bs.
         resultadoLabel.config(text="{:,.2f} $ es equivalente a {:,.2f} Bs  ".format(valorDolar.get(),totalConversion))

         # Guardamos resultado de conversión en label para mostrar resultado de conversión Bs a $.      
         resultado2Label.config(text="{:,.2f} Bs es equivalente a {:,.2f} $  ".format(valorBolivar.get(),totalConversion2))
   
    except TclError:

         # Muestra una ventana emergente en caso de no introducir un número.
         messagebox.showerror("Error", "Debe introducir un número!")

    except dolarmayorException:

         # Muestra una ventana emergente en caso de introducir un número mayor a 1,000,000.00 $.
         messagebox.showerror("Error", "Debe introducir un número menor o igual a 1,000,000.00 $") 

    except bolivarmayorException:
        
        # Muestra una ventana emergente en caso de introducir un número mayor a 1,000,000.00 Bs.
         messagebox.showerror("Error", "Debe introducir un número menor o igual a 1,000,000.00 Bs") 

 
# función para evento de la tecla Enter.
def enterEntry(event):

     # Llamamos a función para calculo de conversión.
     funcionBoton() 

# Creamos botón para calculo de conversión.
calculoButton=Button(miFrame, text="Calcular", width=8, height=2, command=funcionBoton)

# Cambiamos fuente y tamaño de la letra.
calculoButton.config(font=("Roboto",11,"bold"))

# Ubicamos botón para calculo.
calculoButton.place(x=155, y=225)

# Enlazamos evento de presionar la tecla Enter al Entry del valor en $.
cuadroTextoEntryDolar.bind('<Return>', enterEntry)

# Enlazamos evento de presionar la tecla Enter al Entry del valor en Bs.
cuadroTextoEntryBolivar.bind('<Return>', enterEntry)

# Bucle para que la interfaz se mantenga abierta.
root.mainloop()