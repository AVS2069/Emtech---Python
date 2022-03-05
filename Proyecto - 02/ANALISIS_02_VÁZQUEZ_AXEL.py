#%%
#Cargando packages

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#%%
#Loading db, coercion to df
#Tener el csv en la misma carpeta del script, d.o.f., colocar path completo
db = pd.read_csv('synergy_logistics_database.csv',index_col=0)

# Dando formato time a columna date
db['date'] = pd.to_datetime(db['date'],format='%d/%m/%y')
db.head(8)

#%%
# Comenzando con Op.1:

# Filtar por tipo de Dirección mediante cmd loc
db_imports = db.loc[db['direction'] == 'Imports']
db_exports = db.loc[db['direction'] == 'Exports']

#%%
#IMPORTACIONES

#Respecto a Imports, contar las 10 más demandadas
res_imports = db_imports[['origin','destination']].value_counts()
df_importa = res_imports[:10].to_frame()
print(f'Tabla de Importaciones de las 10 rutas más importantes: \n {df_importa}')
print(f'Se tiene que el flujo total de importaciones es de {sum(res_imports)}, por lo que, el porcentaje de dicho flujo que abarcan estás 10 rutas es de {(sum(res_imports[:10])/sum(res_imports))*100}%')


#%%
#EXPORTACIONES

#Respecto a Exports, contar las 10 más demandadas
res_exports = db_exports[['origin','destination']].value_counts()
df_exporta = res_exports[:10].to_frame()
print(f'Tabla de Exportaciones de las 10 rutas más importantes: \n {df_exporta}')
print(f'Se tiene que el flujo total de exportaciones es de {sum(res_exports)}, por lo que, el porcentaje de dicho flujo que abarcan estás 10 rutas es de {(sum(res_exports[:10])/sum(res_exports))*100}%')


#%%
#OPCIÓN 2:

#Obtener el valor total por cada tipo de transporte(var categorica) filtrado por Import
Trans_import = db_imports['transport_mode'].unique()
dict_imp_tot = {}

#Función para contar por var. categor.
for i in Trans_import:
  df_res_tmp = db_imports.loc[db_imports['transport_mode'] == i]
  dict_imp_tot[i] = df_res_tmp['total_value'].sum()

Total_import = pd.DataFrame.from_dict(dict_imp_tot, orient='index',columns=['total_imp'])
Total_import = Total_import.sort_values(by=['total_imp'],ascending=False)
imp_a = Total_import['total_imp'].apply(lambda x: "${:,.2f}".format((x))).to_frame()
print(f'El total de exportaciones por tipo de transporte fue de: \n {imp_a}')

#%%
#Plot tipos de transporte de Importaciones
axisx = ['Sea', 'Rail', 'Road', 'Air']
axisy = Total_import.total_imp
plt.bar(axisx, axisy, color=['green', 'blue', 'yellow', 'red'], edgecolor='grey')
plt.ylabel('Total de Importaciones en $')
plt.xlabel('Tipo de Transporte')
plt.title('Gráfico de Importaciones \n por tipo de transporte', loc = 'center')
plt.show()

#%%
#Obtener el valor total por cada tipo de transporte(var categorica) filtrado por Export
Trans_export = db_exports['transport_mode'].unique()
dict_exp_tot = {}
for i in Trans_export:
  df_res_tmp = db_exports.loc[db_exports['transport_mode'] == i]
  dict_exp_tot[i] = df_res_tmp['total_value'].sum()

Total_export = pd.DataFrame.from_dict(dict_exp_tot, orient='index',columns=['total_exp'])
Total_export = Total_export.sort_values(by=['total_exp'],ascending=False)
print(Total_export['total_exp'].apply(lambda x: "${:,.2f}".format((x))).to_frame())

#%%

#Plot tipos de transporte de Exportaciones

axisy = Total_export.total_exp

plt.bar(axisx, axisy, color=['green', 'blue', 'red','yellow'], edgecolor='grey')
plt.ylabel('Total de Exportaciones en $')
plt.xlabel('Tipo de Transporte')
plt.title('Gráfico de Exportaciones \n por tipo de transporte', loc = 'center')
plt.show()

#%%
#Uniendo resultados import y export en un mismo df
result = pd.concat([Total_import, Total_export], axis=1)
result['total_imp']=result['total_imp'].apply(lambda x: "${:,.2f}".format((x)))
result['total_exp']=result['total_exp'].apply(lambda y: "${:,.2f}".format((y)))
result

#%%
import dataframe_image as dfi
dfi.export(result,'resultados_opcion2.png')

#%%
# Grafica para los tipos de transporte de Imports y Exports
#Fuente del data a graficar:
serie_imp = Total_import.total_imp
serie_exp = Total_export.total_exp

numero_de_grupos = len(serie_imp)
indice_barras = np.arange(numero_de_grupos)
ancho_barras = 0.4

plt.bar(indice_barras, serie_imp, width=ancho_barras, label='Imports')
plt.bar(indice_barras + ancho_barras, serie_exp, width=ancho_barras, label='Exports')
plt.legend(loc = 1)

## Se colocan los indicadores en el eje x
plt.xticks(indice_barras + ancho_barras/2, axisx)

plt.ylabel('Total en $')
plt.xlabel('Tipo de Transporte')
plt.title('Gráfico del total de  \n Importaciones y Exportaciones',loc='center')
plt.savefig("Gráfica_Opcion2.jpg")
plt.show()

#%%
#OPCIÓN 3

# Total de importaciones
Total_source_value = db_imports['total_value'].sum()

# Para obtener el total de importaciones en formato monetario
Total_format = '${:,.2f}'.format(Total_source_value)
print(f'Se tiene un valor total de Importaciones de ${Total_format}')

#%%
# Paises que importan, filtrado en origin
source_ori = db_imports['origin'].unique()
source_ori

#%%
# Generar listado para cada origen sumando el total_value por cada origen
source_total = []

for origen in source_ori:
  source = db_imports.loc[db_imports['origin'] == origen]
  source_total.append([origen,source['total_value'].sum()])
source_total
# pd.DataFrame(source_total)

#%%
# Creamos un df para el total de Países con respecto a Imports
# Agregamos columnas de ['percent', 'cum_percent'], para tabla de frecuencia acumulada
df_sources = pd.DataFrame(source_total, columns = ['Origen', 'Total Importación'])
df_sources = df_sources.sort_values(by=['Total Importación'],ascending=False)
df_sources['Porcentaje'] = ((df_sources['Total Importación'] / Total_source_value))
df_sources['Porcentaje Acumulado'] = df_sources['Porcentaje'].cumsum()
df_sources[:8]

#%%
# Creamos un pie chart para los procentajes de cada origen con respecto a Imports solo para los que cubren el 80% de la demanda
# Data to plot
labels = df_sources['Origen'][:8]
sizes_a = df_sources['Porcentaje'][:8]
theexplode = [0.1,0,0,0,0,0,0,0]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','mediumorchid','cyan', "orange", "blue",]
# Plot
plt.pie(sizes_a, labels=labels, colors=colors, autopct='%.2f%%', shadow=True, startangle=45, explode=theexplode)
plt.axis('equal')
plt.legend(title = 'Principales importadores:', loc = 'best')
plt.title('Gráfico de porcentajes de los paises \n que albergan el 80% de las importaciones ',loc = 'center')
plt.show()

#%%
# EXPORTACIONES
total_target_value = db_exports['total_value'].sum()

# Para obtener el total de exportaciones 
total_print = '${:,.2f}'.format(total_target_value)
print(f'El Total de exportaciones es de: {total_print}')

#%%
# Paises que Exportan, filtrado en destination
target_list = db_exports['destination'].unique()
target_list

#%%

# Generar listado para cada destination

target_total = []

for dest in target_list:
  destin = db_exports.loc[db_exports['destination'] == dest]
  target_total.append([dest,destin['total_value'].sum()])
target_total


#%%
#df para el total de Países respecto a Exports

df_target = pd.DataFrame(target_total, columns = ['Destino', 'Total Exportaciones'])
df_target = df_target.sort_values(by=['Total Exportaciones'],ascending=False)
df_target['Porcentaje'] = ((df_target['Total Exportaciones'] / total_target_value))
df_target['Porcentaje Acumulado'] = df_target['Porcentaje'].cumsum()
df_target[:13]

#%%
#Pie Chart:
labels = df_target['Destino'][:13]
sizes_b = df_target['Porcentaje'][:13]
theexplode = [0.2,0,0,0,0,0,0,0,0,0,0,0,0]
plt.pie(sizes_b, labels=labels, autopct='%.1f%%', startangle=80,shadow = True, explode=theexplode )
plt.axis('equal')
# plt.legend(title = 'Principales exportadores:', loc = 'best')
plt.title('Gráfico de porcentajes de los paises \n que albergan el 80% de las exportaciones ',loc = 'center')
plt.show()