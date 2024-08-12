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

col11 = [ [sg.Text('Datos de OEE (HxH)', font='bold')],
          [sg.Text('Fecha', size=(14, 1)), sg.Input(default_text= hoy,key='FECHA',size=(14,1),)],
          [sg.Text('Linea ',size= (14, 1)), sg.Combo([1,2,3,4,5], size= (2,1),key='LINEA')],
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


tab1_layout = [[sg.Col(col11, pad=((0,10),(25,0)),vertical_alignment='top')]]




window = sg.Window('Registro OEE', tab1_layout)
input_key_list = [key for key, value in window.key_dict.items() if isinstance(value, sg.Input)] #obtenemos la lista de todos los campos 

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
                 # print (f'valor:{valor}')


                  if all(map(str.strip, [values[key] for key in input_key_list])): #comprobamos que todos los campos tengas informacion
                      #  sg.popup("OK")
                        if valor >0:
                            df = pd.DataFrame(values, index=[0]) #los valores en datafreme para pasarlos al archivo
                            #print(df)
                            df.to_csv("H:\Publico\SMT-Prog-Status\DOWN TIME(Total navico)\OEE.csv", header=False, sep=',', index=False, mode='a') #agregamos renglon a las archivo
                            #print(df['ENSAMBLE'].astype('str'))
                            #print(df.dtypes)
                            #oee(df['HORA INICIO'],df['HORA FINAL'],df['ROUTING'],df['PRODUCCION TOTAL'],df['PRODUCCION DEFECTUOSA'],df['PARO PLANIFICADO'],df['TIEMPO MUERTO'],df['ENSAMBLE'])
      
                            sg.popup('Informacion Capturada')
                            clean()
                            datos= pd.read_csv("H:\Publico\SMT-Prog-Status\DOWN TIME(Total navico)\OEE.csv",names=['FECHA','LINEA','Hinicio','HFinal','ASSY','ROUTING','PTotal','PPlanificado','PDef','TIEMPOMUERTO'])
                            oee(datos['Hinicio'].iloc[-1],datos['HFinal'].iloc[-1],datos['ROUTING'].iloc[-1],datos['PTotal'].iloc[-1],datos['PDef'].iloc[-1],datos['PPlanificado'].iloc[-1],datos['TIEMPOMUERTO'].iloc[-1],datos['ASSY'].iloc[-1])
                        else:
                            
                            sg.popup("No se puede reliazar la captura",
                                         "Existe una campo en blanco.",title="ERROR")
                               
                  else:
                        sg.popup("No se puede reliazar la captura",
                                     "Existe una campo en blanco.", title="ERROR")
             except:
                  print('no es numero')
    
          
    if event=="Cancel":
         #print('Cancelado')
         sg.popup('Captura Cancelada')
         clean()
         
       
    
    if event == sg.WIN_CLOSED:           # always,  always give a way out!
        break
window.close()

