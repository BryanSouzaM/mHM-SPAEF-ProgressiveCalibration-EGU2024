###################################################################################################
##                   -------------------------------------------
## ==================   Plot Script for mHM's discharge file    ===================================
##                   -------------------------------------------
##   
##  Author:    Pallav Kumar Shrestha    (pallav-kumar.shrestha@ufz.de)
##             07 October 2021
##
##  Usage:     Place this file alongside discharge.nc file and type the following in
##             the command line -
##
##                              Rscript hydrograph_call.R
##
##  Output:    <stationid>_hydrograph.png
##
##  Detail:    Creates hydrograph plot of the gauge specified in this file
##
##  Reference: 
##
##  Modifications:
##
###################################################################################################


# Source taylor-made functions
source("hydrograph.R")


## Variables
path <- "Z:/EGU2024/4_model/Rio_Velhas/output" # path to the discharge.nc file. 
station_name <- "The Interesting Gauge" # Name of the station/ gauge
station_id <- "398" # Station ID (should be same as in mhm.nml, do not worry about the padded zeroes)

## Generate texts
title_text <- paste("Gauge: ", station_name, " . ", station_id) # Plot title 
  
## Call the hydrograph function 
plot_hydrograph( path, station_id, title_text, "txt" ) # txt - read from daily_dicharge.txt, nc - read from discharge.nc





# Source taylor-made functions
source("hydrograph.R")

## Variáveis fixas
path <- "Z:/EGU2024/6_OST500/Rio_Velhas/output" # Caminho para o arquivo discharge.nc.

# Caminho para a pasta com os nomes dos arquivos de estação
input_path <- "Z:/EGU2024/6_OST500/Rio_Velhas/input/gauge"

# Lista os arquivos na pasta
files <- list.files(path = input_path, full.names = FALSE, pattern = ".txt")

# Loop para processar cada arquivo
for(file_name in files) {
  # Extrai o ID da estação do nome do arquivo, removendo a extensão .txt
  station_id <- sub(".txt", "", file_name)
  
  # O nome da estação não é especificado nos arquivos, então podemos usar o ID como nome, ou ajustar conforme necessário
  station_name <- station_id
  
  # Gera o texto do título
  title_text <- paste("Gauge: ", station_name, " . ", station_id)
  
  # Chama a função hydrograph para cada estação
  plot_hydrograph(path, station_id, title_text, "txt") # Supondo que o formato seja sempre txt
}
