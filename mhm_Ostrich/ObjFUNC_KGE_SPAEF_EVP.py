import numpy as np
import csv
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import math
from netCDF4 import num2date, Dataset
from scipy.stats import variation, zscore
from datetime import datetime, timedelta
import pandas as pd

# Nome da bacia
basin = "Q_KGE_spaef_tws_evp0/Rio_Velhas"


# Definição das datas de início e a quantidade de dias
DataInicioObs = datetime(2003, 2, 1)
DataInicioSim = datetime(2010, 10, 1)
ndias = 1826  # quantidade de dias a ser adicionada a DataInicioSim para definir DataFim

# Definição da data de fim
DataFim = DataInicioSim + timedelta(days=ndias)

print(DataFim)

# Criação da tabela para DataObs
DataObs_range = pd.date_range(start=DataInicioObs, end=DataFim)
df_DataObs = pd.DataFrame(DataObs_range, columns=['DataObs'])
df_DataObs['PosObs'] = df_DataObs.index

# Criação da tabela para DataSim
DataSim_range = pd.date_range(start=DataInicioSim, end=DataFim)
df_DataSim = pd.DataFrame(DataSim_range, columns=['DataSim'])
df_DataSim['PosSim'] = df_DataSim.index

# Encontrar as posições de PosObs onde as datas estão presentes na coluna DataSim
matching_dates_pos = df_DataObs[df_DataObs['DataObs'].isin(df_DataSim['DataSim'])]['PosObs']

print(matching_dates_pos)


# Definição das funções SPAEFnew e filter_nan permanece a mesma
# Função SPAEF e suas dependências permanecem inalteradas
def filter_nan(s, o):
    data = np.transpose(np.array([s.flatten(), o.flatten()]))
    data = data[~np.isnan(data).any(1)]
    return data[:, 0], data[:, 1]

def SPAEFnew(s, o, bins):
    # remove NANs
    s, o = filter_nan(s, o)
    # compute ratio of CV
    alpha = variation(s) / variation(o)
    # compute zscore mean=0, std=1
    o = zscore(o)
    s = zscore(s)
    # compute histograms
    hobs, binobs = np.histogram(o, bins)
    hsim, binsim = np.histogram(s, bins)
    # convert int to float, critical conversion for the result
    hobs = np.float64(hobs)
    hsim = np.float64(hsim)
    # find the overlapping of two histogram
    minima = np.minimum(hsim, hobs)
    # compute the fraction of intersection area to the observed histogram area
    hh = np.sum(minima) / np.sum(hobs)
    # compute corr coeff
    cc = np.corrcoef(s, o)[0, 1]
    # compute SPAEF
    spaef = 1 - np.sqrt((cc - 1)**2 + (alpha - 1)**2 + (hh - 1)**2)
    return spaef, cc, alpha, hh




# Inicialização do SPAEF acumulado e dicionário para armazenar os resultados mensais
ONE_SPAEF = 0
SPAEF_monthly = {}



############################################################################################################ EVP

# Caminho para o arquivo simulado
sim_ncfile = f'Z:/EGU2024/6_OST500/{basin}/output/mHM_Fluxes_States.nc'
sim_fh = Dataset(sim_ncfile, mode='r')
aet = sim_fh.variables['aET'][:] 
mask_basin = (aet.data[0, ::] == -9999)

sim_fh.close()

# Caminho para o arquivo observado
obs_ncfile = f'Z:/EGU2024/6_OST500/{basin}/input/optional_data/pet.nc'
obs_fh = Dataset(obs_ncfile, mode='r')
pet = obs_fh.variables['pet'][matching_dates_pos, :, :] * 86400
obs_fh.close()

print(aet.shape)
print(pet.shape)
print(mask_basin.shape)

from datetime import datetime, timedelta
import pandas as pd

# Definindo as datas de início e fim
start_date = DataInicioSim  # Exemplo: começa em 15 de Março de 2020
end_date = DataFim  # Exemplo: termina em 31 de Outubro de 2023

# Criando um vetor com todas as datas entre o início e o fim
dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Criando uma tabela (DataFrame) com essas datas
df_dates = pd.DataFrame(dates, columns=['Date'])
df_dates['posVector'] = df_dates.index  # A posição no vetor é o índice
df_dates['month'] = df_dates['Date'].dt.month  # Extraindo o mês de cada data

print(df_dates)

# Processamento mensal
for mon_ind in range(1, 13):  # Loop de 1 a 12 para meses
    # Filtra df_dates pelo mês atual no loop e obtém os índices correspondentes
    month_filter = df_dates[df_dates['month'] == mon_ind]['posVector'].values
    
    # Verifica se há dados suficientes para o mês atual antes de prosseguir
    if len(month_filter) == 0:
        continue

    # Filtra a primeira dimensão de aet e pet usando os índices do mês atual
    sim_monthly = aet[month_filter, :, :]
    obs_monthly = pet[month_filter, :, :]
    
    # Calcula a média mensal ao longo da primeira dimensão, que agora é temporal
    sim_monthly_mean = np.nanmean(sim_monthly, axis=0)
    obs_monthly_mean = np.nanmean(obs_monthly, axis=0)

    # Aplicar máscara de bacia e ajustar NaNs
    # Esta parte do código presume que mask_basin já está definido corretamente
    sim_monthly_mean[mask_basin] = np.nan
    obs_monthly_mean[mask_basin] = np.nan

    # Filtra NaNs para obter dados válidos para cálculo do SPAEF
    mask = np.isnan(sim_monthly_mean) | np.isnan(obs_monthly_mean)
    sim_valid = sim_monthly_mean[~mask]
    obs_valid = obs_monthly_mean[~mask]

    # Calcular SPAEF para o mês
    num_bin = int(math.sqrt(len(sim_valid)))
    SPAEF, cc, alpha, hh = SPAEFnew(sim_valid, obs_valid, num_bin)
    SPAEF_monthly[mon_ind] = SPAEF  # Índice de mês já é humano (1-12)


# O dicionário SPAEF_monthly agora contém os valores SPAEF para cada mês para a bacia "Rio_Velhas"
    
# Imprimir os valores de SPAEF para cada mês
for month, value in SPAEF_monthly.items():
    print(f"SPAEF EVP para o mês {month}: {value:.4f}")

# Calcular o valor médio de SPAEF para todos os meses
SPAEF_monthly_average_EVP = np.mean(list(SPAEF_monthly.values()))

# Imprimir o valor médio de SPAEF
print(f"\nValor médio de SPAEF EVP para todos os meses: {SPAEF_monthly_average_EVP:.4f}")

############################################################################################################ TWS


# Caminho para o arquivo simulado
sim_ncfile = f'Z:/EGU2024/6_OST500/{basin}/output/mHM_Fluxes_States.nc'
sim_fh = Dataset(sim_ncfile, mode='r')
aet = sim_fh.variables['SWC_L01'][:] 
mask_basin = (aet.data[0, ::] == -9999)

sim_fh.close()


# Caminho para o arquivo observado
obs_ncfile = f'Z:/EGU2024/6_OST500/{basin}/input/optional_data/tws.nc'
obs_fh = Dataset(obs_ncfile, mode='r')
tws = obs_fh.variables['tws'][matching_dates_pos, :, :] * 86400
obs_fh.close()

print(aet.shape)
print(tws.shape)
print(mask_basin.shape)


from datetime import datetime, timedelta
import pandas as pd

# Definindo as datas de início e fim
start_date = DataInicioSim  # Exemplo: começa em 15 de Março de 2020
end_date = DataFim  # Exemplo: termina em 31 de Outubro de 2023

# Criando um vetor com todas as datas entre o início e o fim
dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Criando uma tabela (DataFrame) com essas datas
df_dates = pd.DataFrame(dates, columns=['Date'])
df_dates['posVector'] = df_dates.index  # A posição no vetor é o índice
df_dates['month'] = df_dates['Date'].dt.month  # Extraindo o mês de cada data

print(df_dates)

# Processamento mensal
for mon_ind in range(1, 13):  # Loop de 1 a 12 para meses
    # Filtra df_dates pelo mês atual no loop e obtém os índices correspondentes
    month_filter = df_dates[df_dates['month'] == mon_ind]['posVector'].values
    
    # Verifica se há dados suficientes para o mês atual antes de prosseguir
    if len(month_filter) == 0:
        continue

    # Filtra a primeira dimensão de aet e tws usando os índices do mês atual
    sim_monthly = aet[month_filter, :, :]
    obs_monthly = tws[month_filter, :, :]
    
    # Calcula a média mensal ao longo da primeira dimensão, que agora é temporal
    sim_monthly_mean = np.nanmean(sim_monthly, axis=0)
    obs_monthly_mean = np.nanmean(obs_monthly, axis=0)

    # Aplicar máscara de bacia e ajustar NaNs
    # Esta parte do código presume que mask_basin já está definido corretamente
    sim_monthly_mean[mask_basin] = np.nan
    obs_monthly_mean[mask_basin] = np.nan

    # Filtra NaNs para obter dados válidos para cálculo do SPAEF
    mask = np.isnan(sim_monthly_mean) | np.isnan(obs_monthly_mean)
    sim_valid = sim_monthly_mean[~mask]
    obs_valid = obs_monthly_mean[~mask]

    # Calcular SPAEF para o mês
    num_bin = int(math.sqrt(len(sim_valid)))
    SPAEF, cc, alpha, hh = SPAEFnew(sim_valid, obs_valid, num_bin)
    SPAEF_monthly[mon_ind] = SPAEF  # Índice de mês já é humano (1-12)

# O dicionário SPAEF_monthly agora contém os valores SPAEF para cada mês para a bacia "Rio_Velhas"
    
# Imprimir os valores de SPAEF para cada mês
for month, value in SPAEF_monthly.items():
    print(f"SPAEF TWS para o mês {month}: {value:.4f}")

# Calcular o valor médio de SPAEF para todos os meses
SPAEF_monthly_average_TWS = np.mean(list(SPAEF_monthly.values()))

# Imprimir o valor médio de SPAEF
print(f"\nValor médio de SPAEF TWS para todos os meses: {SPAEF_monthly_average_TWS:.4f}")


############################################################################################################


def calculate_kge(simulated, observed):
    """
    Calcula o Kling-Gupta Efficiency (KGE) entre séries simuladas e observadas.

    :param simulated: numpy.ndarray, valores simulados
    :param observed: numpy.ndarray, valores observados
    :return: KGE, cc (coeficiente de correlação), alpha (variabilidade), beta (viés)
    """
    r = np.corrcoef(observed, simulated)[0, 1]
    alpha = np.std(simulated) / np.std(observed)
    beta = np.mean(simulated) / np.mean(observed)
    kge = 1 - np.sqrt((r - 1)**2 + (alpha - 1)**2 + (beta - 1)**2)
    return kge

# Usando a função calculate_kge com seus dados

ONE_KGE = 0

# Carregando os dados de descarga diária
Q_data = np.loadtxt(f'Z:/EGU2024/6_OST500/{basin}/output/daily_discharge.out', skiprows=1)

# Pares de colunas para calcular o KGE
# Pares de colunas originais ajustados para começar a contagem na coluna correta
column_pairs = [(5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16)]


# Lista para armazenar os valores KGE de cada par de colunas
kge_values = []

for pair in column_pairs:
    # Extração das séries observada e simulada, considerando apenas valores > 0 na coluna observada
    o = Q_data[:, pair[0]-1][Q_data[:, pair[0]-1] > 0]
    s = Q_data[:, pair[1]-1][Q_data[:, pair[0]-1] > 0]
    
    # Calculando o KGE para o par de colunas atual
    kge = calculate_kge(s, o)
    kge_values.append(kge)
    
    # Imprimindo o valor de KGE para o par de colunas atual
    print(f"KGE for columns {pair[0]} and {pair[1]}: {kge}")

# Calculando a média dos valores KGE para obter o One_KGE
ONE_KGE = np.mean(kge_values)

# Imprimindo o valor final de One_KGE
print("Final ONE_KGE:", ONE_KGE)




















#######################################################################################

# Definindo o nome do arquivo de saída
csvfile = 'TSEB_SPAEF_KGE_SPAEF_TWS.out'

# Preparando os dados para serem escritos no arquivo
val = np.array([['METRIC', 'VALUE'], ['KGE', np.around(1-ONE_KGE, 7)]])

# Escrevendo os dados no arquivo
with open(csvfile, "w") as output:
    writer = csv.writer(output, delimiter=' ', lineterminator='\n')
    for row in val:
        writer.writerow(row)

print('Dados de KGE escritos com sucesso em', csvfile)

#######################################################################################

# Supondo que SPAEF_monthly_average já foi calculado ou definido anteriormente
# SPAEF_monthly_average_EVP = 0.85  # Exemplo de valor, ajuste conforme necessário

# Nome do arquivo CSV para adicionar a nova linha
csvfile = 'TSEB_SPAEF_KGE_SPAEF_TWS.out'

# Novos dados para adicionar ao arquivo
new_row = ['SPAEF_EVP', np.around(1-SPAEF_monthly_average_EVP, 7)]

# Abrindo o arquivo em modo de append para adicionar a nova linha
with open(csvfile, "a") as output:
    writer = csv.writer(output, delimiter=' ', lineterminator='\n')
    writer.writerow(new_row)

print('Linha SPAEF_EVP adicionada com sucesso ao arquivo', csvfile)


#######################################################################################

# Supondo que SPAEF_TWS já foi calculado ou definido anteriormente
# SPAEF_monthly_average_TWS = 0.75  # Exemplo de valor, ajuste conforme necessário

# Nome do arquivo CSV para adicionar a nova linha
csvfile = 'TSEB_SPAEF_KGE_SPAEF_TWS.out'

# Novos dados para adicionar ao arquivo
new_row = ['SPAEF_TWS', np.around(1-SPAEF_monthly_average_TWS, 7)]

# Abrindo o arquivo em modo de append para adicionar a nova linha
with open(csvfile, "a") as output:
    writer = csv.writer(output, delimiter=' ', lineterminator='\n')
    writer.writerow(new_row)

print('Linha SPAEF_TWS adicionada com sucesso ao arquivo', csvfile)
#######################################################################################

# Nome do arquivo CSV para adicionar a nova linha
csvfile = 'TSEB_SPAEF_KGE_SPAEF_TWS.out'

# Novos dados para adicionar ao arquivo
new_row = ['Q_KGE_SPAEF_TWS', np.around(0.5*(1-ONE_KGE)+0.5*(1-SPAEF_monthly_average_TWS), 7)]

# Abrindo o arquivo em modo de append para adicionar a nova linha
with open(csvfile, "a") as output:
    writer = csv.writer(output, delimiter=' ', lineterminator='\n')
    writer.writerow(new_row)

print('Linha Q_KGE_SPAEF_TWS adicionada com sucesso ao arquivo', csvfile)


#######################################################################################

# Nome do arquivo CSV para adicionar a nova linha
csvfile = 'TSEB_SPAEF_KGE_SPAEF_TWS.out'

# Novos dados para adicionar ao arquivo
new_row = ['Q_KGE_SPAEF_EVP', np.around(0.5*(1-ONE_KGE)+0.5*(1-SPAEF_monthly_average_EVP), 7)]

# Abrindo o arquivo em modo de append para adicionar a nova linha
with open(csvfile, "a") as output:
    writer = csv.writer(output, delimiter=' ', lineterminator='\n')
    writer.writerow(new_row)

print('Linha Q_KGE_SPAEF_EVP adicionada com sucesso ao arquivo', csvfile)

#######################################################################################

# Nome do arquivo CSV para adicionar a nova linha
csvfile = 'TSEB_SPAEF_KGE_SPAEF_TWS.out'

# Novos dados para adicionar ao arquivo
new_row = ['Q_KGE_SPAEF_EVP_TWS', np.around(0.5*(1-ONE_KGE)+0.25*(1-SPAEF_monthly_average_EVP)+0.25*(1-SPAEF_monthly_average_TWS), 7)]

# Abrindo o arquivo em modo de append para adicionar a nova linha
with open(csvfile, "a") as output:
    writer = csv.writer(output, delimiter=' ', lineterminator='\n')
    writer.writerow(new_row)

print('Linha Q_KGE_SPAEF_EVP_TWS adicionada com sucesso ao arquivo', csvfile)


# Supondo que SPAEF_monthly_average já foi calculado ou definido anteriormente
# SPAEF_monthly_average_EVP = 0.85  # Exemplo de valor, ajuste conforme necessário

# Nome do arquivo CSV para adicionar a nova linha
csvfile = 'TSEB_SPAEF_KGE_SPAEF_TWS.out'

# Novos dados para adicionar ao arquivo
new_row = ['Real_KGE', np.around(ONE_KGE, 7)]

# Abrindo o arquivo em modo de append para adicionar a nova linha
with open(csvfile, "a") as output:
    writer = csv.writer(output, delimiter=' ', lineterminator='\n')
    writer.writerow(new_row)

print('Linha SPAEF_EVP adicionada com sucesso ao arquivo', csvfile)

#######################################################################################

# Supondo que SPAEF_monthly_average já foi calculado ou definido anteriormente
# SPAEF_monthly_average_EVP = 0.85  # Exemplo de valor, ajuste conforme necessário

# Nome do arquivo CSV para adicionar a nova linha
csvfile = 'TSEB_SPAEF_KGE_SPAEF_TWS.out'

# Novos dados para adicionar ao arquivo
new_row = ['Real_SPAEF_EVP', np.around(SPAEF_monthly_average_EVP, 7)]

# Abrindo o arquivo em modo de append para adicionar a nova linha
with open(csvfile, "a") as output:
    writer = csv.writer(output, delimiter=' ', lineterminator='\n')
    writer.writerow(new_row)

print('Linha SPAEF_EVP adicionada com sucesso ao arquivo', csvfile)


#######################################################################################

# Supondo que SPAEF_TWS já foi calculado ou definido anteriormente
# SPAEF_monthly_average_TWS = 0.75  # Exemplo de valor, ajuste conforme necessário

# Nome do arquivo CSV para adicionar a nova linha
csvfile = 'TSEB_SPAEF_KGE_SPAEF_TWS.out'

# Novos dados para adicionar ao arquivo
new_row = ['Real_SPAEF_TWS', np.around(SPAEF_monthly_average_TWS, 7)]

# Abrindo o arquivo em modo de append para adicionar a nova linha
with open(csvfile, "a") as output:
    writer = csv.writer(output, delimiter=' ', lineterminator='\n')
    writer.writerow(new_row)

print('Linha SPAEF_TWS adicionada com sucesso ao arquivo', csvfile)
