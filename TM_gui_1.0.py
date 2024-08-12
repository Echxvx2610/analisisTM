import PySimpleGUI as sg
import pandas as pd
import datetime as dt
"""
    Simple Form (a one-shot data entry window)
    Use this design pattern to show a form one time to a user that is "submitted"
"""
sg.theme('Reddit')
hoy = dt.date.today()
#print(hoy)

BPAD_LEFT = ((10,10), (10, 10))
BPAD_RIGHT = ((10,20), (10, 20))
in_size=(4,1) # tamano para input box de causas de tiempo muerto
label_size=(34,1) #tamaño para etiquetas de causa de tiempo muerto
def limpiar():
        window['LINEA'].update(values=[1,2,3,4,5])
        window['HORA INICIO'].update(value='00:00')
        window['HORA FINAL'].update(value='00:00')
        window['E1'].update(value='0')
        window['E2'].update(value='0')
        window['E3'].update(value='0')
        window['E4'].update(value='0')
        window['E5'].update(value='0')
        window['E6'].update(value='0')
        window['E7'].update(value='0')
        window['E8'].update(value='0')
        window['M1'].update(value='0')
        window['M2'].update(value='0')
        window['M3'].update(value='0')
        window['M4'].update(value='0')
        window['M5'].update(value='0')
        window['M6'].update(value='0')
        window['A1'].update(value='0')
        window['A2'].update(value='0')
        window['A3'].update(value='0')
        window['A4'].update(value='0')
        window['A5'].update(value='0')
        window['A6'].update(value='0')
        window['A7'].update(value='0')
        window['A8'].update(value='0')
        window['A9'].update(value='0')
        window['A10'].update(value='0')
        window['A11'].update(value='0')
        window['A12'].update(value='0')
        window['A13'].update(value='0')
        window['A14'].update(value='0')
        window['A15'].update(value='0')
        window['Q1'].update(value='0')
        window['Q2'].update(value='0')
        window['Q3'].update(value='0')
        window['Q4'].update(value='0')
        window['C1'].update(value='0')
        window['C2'].update(value='0')
        window['S1'].update(value='0')
        window['S2'].update(value='0')

def guaradado():
      sg.popup('Informacion capturada')

col12=  [ [sg.Text('Causas Tiempo Muerto', font='bold')],
          [sg.Text('')],
          [sg.Text('Fecha', size=(14, 1)), sg.Input(default_text= hoy,key='FECHA',size=(14,1),)],
          [sg.Text('Linea ',size= (14, 1)), sg.Combo([1,2,3,4,5], size= (2,1),key='LINEA')],
          [sg.Text('Hora Inicio', size=(14,1)), sg.Input(key='HORA INICIO',size=(14,1),default_text='00:00')], 
          [sg.Text('Hora Final', size=(14,1)), sg.Input(key='HORA FINAL',size=(14,1),default_text='00:00')],
          [sg.Text('E1: Mantenimiento Correctivo', size=label_size), sg.Input(key='E1',size=in_size,default_text='0')],
          [sg.Text('E2: Mantenimiento Preventivo', size=label_size), sg.Input(key='E2',size=in_size,default_text='0')], 
          [sg.Text('E3: Esperando partes de Reemplazo', size=label_size), sg.Input(key='E3',size=in_size,default_text='0')],
          [sg.Text('E4: Esperando Tecnico', size=label_size), sg.Input(key='E4',size=in_size,default_text='0')],
          [sg.Text('E5: Protos o Prueba de Ingenieria', size=label_size), sg.Input(key='E5',size=in_size,default_text='0')],
          [sg.Text('E6: Esperando Carga de Programa', size=label_size), sg.Input(key='E6',size=in_size,default_text='0')],
          [sg.Text('E7: Problemas de Proceso', size=label_size), sg.Input(key='E7',size=in_size,default_text='0')],
          [sg.Text('E8: Problemas de Equipo de Prueba', size=label_size), sg.Input(key='E8',size=in_size,default_text='0')],
          [sg.Text('M1: Material Equivocado (Carrusel / Almacen)', size=label_size), sg.Input(key='M1',size=in_size,default_text='0')],
          [sg.Text('M2: Seguridad (Conatos, Alarmas, Simulacros)', size=label_size), sg.Input(key='M2',size=in_size,default_text='0')],
          [sg.Text('M3: Falla de Servicios (Luz, Agua, etc.)', size=label_size), sg.Input(key='M3',size=in_size,default_text='0')],
          [sg.Text('M4: Esperando material de AVNET', size=label_size), sg.Input(key='M4',size=in_size,default_text='0')],
          [sg.Text('M5: Discrepancia de Material', size=label_size), sg.Input(key='M5',size=in_size,default_text='0')],
          [sg.Text('M6: Kit no a Tiempo (por carga de trabajo)', size=label_size), sg.Input(key='M6',size=in_size,default_text='0')],
          [sg.Text('A1: Falta de material(Disc./Prod.)', size=label_size), sg.Input(key='A1',size=in_size,default_text='0')],
          [sg.Text('A2: Setup Arrenque / Traslape', size=label_size), sg.Input(key='A2',size=in_size,default_text='0')],
          [sg.Text('A3: Cambio de Setup', size=label_size), sg.Input(key='A3',size=in_size,default_text='0')],
          
          
          ]

col12_1 = [[sg.Text('A4: Sin Prog. de Produccion/ Mejora Continua', size=label_size), sg.Input(key='A4',size=in_size,default_text='0')],
           [sg.Text('A5: Falta de Personal / Entrenamiento', size=label_size), sg.Input(key='A5',size=in_size,default_text='0')],
          [sg.Text('A6: Juntas o Limpieza (Ejercicios)', size=label_size), sg.Input(key='A6',size=in_size,default_text='0')],
          [sg.Text('A7: Cubriendo Otra Linea', size=label_size), sg.Input(key='A7',size=in_size,default_text='0')],
          [sg.Text('A8: Esperando Placa (Maq Previa o sig. Caida)', size=label_size), sg.Input(key='A8',size=in_size,default_text='0')],
          [sg.Text('A9: Error de Operacion', size=label_size), sg.Input(key='A9',size=in_size,default_text='0')],
          [sg.Text('A10: Costando Rollo', size=label_size), sg.Input(key='A10',size=in_size,default_text='0')],
          [sg.Text('A11: Contando material(conteo ciclico)', size=label_size), sg.Input(key='A11',size=in_size,default_text='0')],
          [sg.Text('A12: Buscando Rollo', size=label_size), sg.Input(key='A12',size=in_size,default_text='0')],
          [sg.Text('A13: Esperando Setup', size=label_size), sg.Input(key='A13',size=in_size,default_text='0')],
          [sg.Text('A14: Cambios de Rollo', size=label_size), sg.Input(key='A14',size=in_size,default_text='0')],
          [sg.Text('A15: Descansos', size=label_size), sg.Input(key='A15',size=in_size,default_text='0')],
          [sg.Text('Q1: Inspeccion o Problema de Calidad', size=label_size), sg.Input(key='Q1',size=in_size,default_text='0')],
          [sg.Text('Q2: Proveedor', size=label_size), sg.Input(key='Q2',size=in_size,default_text='0')],
          [sg.Text('Q3: Falta de Material (QC Inspeccion)', size=label_size), sg.Input(key='Q3',size=in_size,default_text='0')],
          [sg.Text('Q4: Liberacion de Calidad', size=label_size), sg.Input(key='Q4',size=in_size,default_text='0')],
          [sg.Text('C1: Cambio de programa (Prioridades)', size=label_size), sg.Input(key='C1',size=in_size,default_text='0')],
          [sg.Text('C2: Error en Plan de Produccion', size=label_size), sg.Input(key='C2',size=in_size,default_text='0')],
          [sg.Text('S1: Fallas de Sistema', size=label_size), sg.Input(key='S1',size=in_size,default_text='0')],
          [sg.Text('S2: Fallas de equipo de Computo', size=label_size), sg.Input(key='S2',size=in_size,default_text='0')],
          [sg.Text('NOTA: no debe dejar espacio en blanco', text_color='black')],
         
          [sg.Button('Save',font='bold', pad=((160,25),(0,0))), sg.Button('Cancel',font='bold', pad=((0,0),(0,0)))]
          ]

tab1_layout = [[sg.Col(col12,pad =((0,0),(0,0)),vertical_alignment='top'),sg.Col(col12_1,pad=((0,10),(60,0)),vertical_alignment='top')]]




window = sg.Window('Registro Tiempo Muerto', tab1_layout)
input_key_list = [key for key, value in window.key_dict.items() if isinstance(value, sg.Input)] #obtenemos la lista de todos los campos 

while True:
    event, values = window.read()

    if event == 'Save':
        linea = values['LINEA']
    if linea == '':
        sg.popup('Linea no seleccionada', title="ERROR")
    else:
        try:
            valor = int(linea)
            if all(map(str.strip, [values[key] for key in input_key_list])):
                if valor > 0:
                    df = pd.DataFrame(values, index=[0])
                    try:
                        df.to_csv("H:\Publico\SMT-Prog-Status\DOWN TIME(Total navico)\TM_SMT.csv", header=False, sep=',', index=False, mode='a')
                        guaradado()
                        limpiar()
                    except FileNotFoundError as e:
                        print('Directorio no encontrado:', e)
                        sg.popup('Directorio no encontrado', title="ERROR")
                else:
                    sg.popup("No se puede realizar la captura", "Existe un campo en blanco.", title="ERROR")
            else:
                sg.popup("No se puede realizar la captura", "Existe un campo en blanco.", title="ERROR")
        except ValueError as e:
            #print('No es un número:', e)
            sg.popup('El valor ingresado para la línea no es un número válido', title="ERROR")
        except Exception as e:
            #print('Error desconocido al guardar el archivo:', e)
            sg.popup('Error desconocido al guardar el archivo', title="ERROR")
        

          
    if event=="Cancel":
         print('Cancelado')
         sg.popup('la captura sera cancelada')
         limpiar()
         
       
    
    if event == sg.WIN_CLOSED:           # always,  always give a way out!
        break
window.close()

