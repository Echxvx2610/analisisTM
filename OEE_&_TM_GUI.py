import PySimpleGUI as sg
import pandas as pd
import datetime as dt
from datetime import date as fechas
from datetime import datetime
pd.options.mode.use_inf_as_na = True


"""
    Simple Form (a one-shot data entry window)
    Use this design pattern to show a form one time to a user that is "submitted"
"""
sg.theme('Reddit')
#......................:::: CONFIGURACION DEL DATAFRAME ::::..................
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
#pd.set_option('expand_frame_repr', False)

#*********************************************** OEE ****************************************************
hoy = dt.date.today()
#print(hoy)

BPAD_LEFT = ((10,10), (10, 10))
BPAD_RIGHT = ((10,20), (10, 20))
in_size=(4,1) # tamano para input box de causas de tiempo muerto
label_size=(34,1) #tamaño para etiquetas de causa de tiempo muerto
def oee(HI, HT, RT, PR, PD, PP,TM, Assy):

    fecha = fechas.today()
    hoy = fecha.strftime('%#m/%#d/%Y')
    #print(hoy)
    
    #print(" ")
    hora = datetime.now().hour
    #print(hora)
    
    #print(" ")


    #HI = TimeVar()
    HI_t = datetime.strptime(HI, '%H:%M') # convertimos el dato en formato tiempo (1900-1-1 h:m:s)
    #print(type(HI_t))
   # print(HI_t)
    HI_t = getTime(HI_t) #obtenemos la Hora en tupla
    HI_tt= timeInt(HI_t) #obtenemos la hora en int
    #print(HI_tt)

 
    HT_t = datetime.strptime(HT, '%H:%M') # convertimos el dato en formato tiempo (1900-1-1 h:m:s)
    #print(type(HI_t))
   #print(HT_t)
    HT_t = getTime(HT_t)
    HT_tt= timeInt(HT_t)
    #print(HT_tt)
 

    
    TD = ((HT_tt - HI_tt)*60) - PP
   # print(TD)
    TO = TD - TM
    TC = 60 / RT #(en min)
    PT = TD / TC
    #print(PT)
    PB = PR - PD


    # Components validation
    if TO <= TD and PR <= PT and PB <= PR:
        D = TO / TD
        E = PR / PT
        C = PB / PR

        OEE = D*E*C
        #List = [str(HI_t),str(HT_t),str(RT),str(TD),str(TO),str(PT),str(PR),str(PB),str(PD),str(PP),str(TM),str(D),str(E),str(C),str(OEE),str(Assy)]
#        List = [hoy,HI_t,HT_t,RT,TD,TO,PT,PR,PB,PD,PP,TM,D,E,C,OEE,Assy]
        #print(List)
#        reg_data(List)
        sg.popup('OEE: {}%'.format(round(OEE*100,2)),
                 'Disponibilidad: {}%'.format(round(D*100,2)),
                 'Eficiencia: {}%'.format(round(E*100,2)),
                 'Calidad: {}%'.format(round(C*100,2)),
                 background_color='black', button_color=('white','dark gray'),font='bold',no_titlebar=True, custom_text='Enterado'
                 )

       # return (print('OEE: {}%'.format(round(OEE*100,2))),
     #           print('Disponibilidad: {}%'.format(round(D*100,2)) ),
     #           print('Eficiencia: {}%'.format(round(E*100,2))),
      #          print('Calidad: {}%'.format(round(C*100,2))))

     # Errors validation
    if TO > TD:
       # print('Error. El tiempo operativo no puede ser mayot que el Tiempo Disponible.')
        sg.popup('Error. El tiempo operativo no puede ser mayor que el Tiempo Disponible.')
        last_row()
    if PR > PT:
       # print('Error. La Produccion Real no puede ser mayor a la Capacidad de Produccion.')
        sg.popup('Error. La Produccion Real no puede ser mayor a la Capacidad de Produccion.')
        last_row()
    if PB > PR:
        #print('Error. La Produccion Buena no puede ser mayor a la Produccion Real')
        sg.popup('Error. La Produccion Buena no puede ser mayor a la Produccion Real')
        last_row()

def getTime(hora): #convertimos la hora en texto
    horaT = hora.strftime("%H:%M")
    #print(horaT)
    #print(type(horaT))
    return horaT

def timeInt(TInt): #convertimos la hora en numero
    TInt_data = TInt.split(":")
    #print(TInt_data)
    dataH= int(TInt_data[0])
    #print(dataH)
    dataM = int(TInt_data[1])/60 #convetimos minuto a decimal
    #print(dataM)
    TInt_data_TT = dataH + dataM
    #print(TInt_data_TT)
    return TInt_data_TT

def last_row():
    l_data = pd.read_csv("H:\Publico\SMT-Prog-Status\DOWN TIME(Total navico)\OEE.csv")
    #print(l_data)
    l_data.drop(index=l_data.index[-1],axis=0,inplace=True)
    #print(l_data)
    l_data.to_csv("H:\Publico\SMT-Prog-Status\DOWN TIME(Total navico)\OEE.csv", header=False,index=False)

def clean():
        window['LINEA'].update(values=[1,2,3,4,5])
        window['HORA INICIO'].update(value='00:00')
        window['HORA FINAL'].update(value='00:00')
        window['ENSAMBLE'].update(value='')
        window['ROUTING'].update(value='')
        window['PRODUCCION TOTAL'].update(value='0')
        window['PARO PLANIFICADO'].update(value='0')
        window['PRODUCCION DEFECTUOSA'].update(value='0')
        window['TIEMPO MUERTO'].update(value='0')
#*********************************************************** TM ****************************************************





#****************************************************** GUI ******************************************************
col11 = [ [sg.Text('Datos de OEE (HxH)', font='bold')],
          [sg.Text('Fecha', size=(14, 1)), sg.Input(default_text= hoy,key='FECHA',size=(14,1),)],
          [sg.Text('Linea ',size= (14, 1)), sg.Combo([1,2,3,4,5], size= (10,1),key='LINEA')],
          [sg.Text('Hora Inicio', size=(14,1)), sg.Input(key='HORA INICIO',size=(14,1),default_text='00:00')], 
          [sg.Text('Hora Final', size=(14,1)), sg.Input(key='HORA FINAL',size=(14,1),default_text='00:00')],
          [sg.Text('Ensamble', size=(14, 1)), sg.InputText(key='ENSAMBLE',size=(14,1))],
          [sg.Text('Routing', size=(14, 1)), sg.Input(key='ROUTING',size=(14,1))],
          [sg.Text('Prod. Total', size=(14, 1)), sg.Input(key='PRODUCCION TOTAL',size=(14,1))],
          [sg.Text('Paro Planeado', size=(14, 1)), sg.Input(key='PARO PLANIFICADO',size=(14,1),default_text='0')],
          [sg.Text('Prod. Defectuosa', size=(14, 1)), sg.Input(key='PRODUCCION DEFECTUOSA',size=(14,1),default_text='0')],
          [sg.Text('Tiempo Muerto', size=(14, 1)), sg.Input(key='TIEMPO MUERTO',size=(14,1),default_text='0')],
          
          [sg.Button('Save',pad=((100,10),(20,0))), sg.Button('Cancel',pad=((0,0),(20,0)))]
          ]

col_layout = [[sg.Col(col11, pad=((0,10),(25,0)),vertical_alignment='top')]]

col21=  [ [sg.Text('Causas Tiempo Muerto', font='bold')],
          [sg.Text('')],
          [sg.Text('Fecha', size=(14, 1)), sg.Input(default_text= hoy,key='FECHA TM',size=(14,1),)],
          [sg.Text('Linea ',size= (14, 1)), sg.Combo([1,2,3,4,5], size= (2,1),key='LINEA TM')],
          [sg.Text('Hora Inicio', size=(14,1)), sg.Input(key='HORA INICIO TM',size=(14,1),default_text='00:00')], 
          [sg.Text('Hora Final', size=(14,1)), sg.Input(key='HORA FINAL TM',size=(14,1),default_text='00:00')],
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

col22 = [[sg.Text('A4: Sin Prog. de Produccion/ Mejora Continua', size=label_size), sg.Input(key='A4',size=in_size,default_text='0')],
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

col2_layout = [[sg.Col(col21,pad =((0,0),(0,0)),vertical_alignment='top'),sg.Col(col22,pad=((0,10),(60,0)),vertical_alignment='top')]]


layout = [[sg.TabGroup([[sg.Tab('OEE', col_layout), sg.Tab('TM', col2_layout)]])],]

window = sg.Window('Registro OEE',layout,element_justification='center',finalize=True)
#input_key_list = [key for key, value in window.key_dict.items() if isinstance(value, sg.Input)] #obtenemos la lista de todos los campos 
key_list_elements = [key for key, value in window.key_dict.items()] #obtenemos la lista de todos los campos
key_list_OEE = key_list_elements[0:10]
key_list_TM = key_list_elements[13:]
# print("Total key",key_list_elements)
# print(len(key_list_elements))
# print("OEE: ",key_list_OEE)
# print("TM: ",key_list_TM)



# **************************************************************************************************
while True:
    event, values = window.read()

    if event == 'Save':
     #   print(input_key_list)gf
     #   print(values['LINEA'])
     #   print(type(values['LINEA']))
        lin= values['LINEA']
        if lin =='':
     #        print('vacio')
             sg.popup('Linea no seleccionada', title="ERROR")
        else:
            try:
                valor = int(lin)
                # interamos sobre los valores de key en lista key_list_OEE
                if all([values[key] for key in key_list_OEE]):
                    #sg.popup("OK")
                    if valor > 0:
                        #valores = [values[key] for key in key_list_OEE]
                        #print(valores)
                        
                        df = pd.DataFrame({key: values[key] for key in key_list_OEE}, index=[0])
                        print(df)
                        #df.to_csv("H:\Publico\SMT-Prog-Status\DOWN TIME(Total navico)\OEE.csv", header=False, sep=',', index=False, mode='a') #agregamos renglon a las archivo
                        sg.popup('Informacion Capturada')
                        #print(df['ENSAMBLE'].astype('str'))
                        #print(df.dtypes)
                        #oee(df['HORA INICIO'],df['HORA FINAL'],df['ROUTING'],df['PRODUCCION TOTAL'],df['PRODUCCION DEFECTUOSA'],df['PARO PLANIFICADO'],df['TIEMPO MUERTO'],df['ENSAMBLE'])
                        clean()
                        #datos= pd.read_csv("H:\Publico\SMT-Prog-Status\DOWN TIME(Total navico)\OEE.csv",names=['FECHA','LINEA','Hinicio','HFinal','ASSY','ROUTING','PTotal','PPlanificado','PDef','TIEMPOMUERTO'])
                        #print(datos)
                        #oee(datos['Hinicio'].iloc[-1],datos['HFinal'].iloc[-1],datos['ROUTING'].iloc[-1],datos['PTotal'].iloc[-1],datos['PDef'].iloc[-1],datos['PPlanificado'].iloc[-1],datos['TIEMPOMUERTO'].iloc[-1],datos['ASSY'].iloc[-1])
                    else:
                        sg.popup("No se puede reliazar la captura",
                                         "Existe una campo en blanco.",title="ERROR")
                               
                else:
                    sg.popup("No se puede reliazar la captura",
                                     "Existe una campo en blanco.", title="ERROR")
            except Exception as e:
                print(e)
                  
    
    
          
    if event=="Cancel":
         #print('Cancelado')
         sg.popup('Captura Cancelada')
         clean()   
    
    if event == sg.WIN_CLOSED:           # always,  always give a way out!
        break
    
    window.close()

