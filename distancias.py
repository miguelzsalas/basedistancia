import pandas as pd
import openrouteservice
from geopy.geocoders import Nominatim
nom = Nominatim()
import time
client = openrouteservice.Client(key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') # Coloque a chave da sua API aqui
cidades = pd.read_excel('de_para.xlsx', 'Cidade', encoding = 'utf8') # Insira sua tabela de latitude e longitude extraida
origem = [-11.1111, -11.1111] #Insira aqui a latitude e a longitude do seu ponto de origem
df = pd.DataFrame(columns=['Origem', 'Estado', 'Cidade', 'Distancia']) # Gera um dataframe para ir armazenando os dados em uma tabela
row = 0
for i in cidades['ID.1']:
    try:
        cidade = i
        coords = ((origem[1], origem[0]),(cidades['LONGITUDE'][row], cidades['LATITUDE'][row]))
        routes = client.directions(coords)
        #print("Origem", cidade, "Distância:", routes['routes'][0]['summary']['distance']) # Tire essa linha como comentário caso queira ver como ficará o resultado
        df.loc[row] = ["Origem", cidade[-2:], cidade[:-2], routes['routes'][0]['summary']['distance']] # Joga o resultado diretamente no dataframe criado
        row = row + 1
        time.sleep(1)
    except:
        try:
            destino = nom.geocode(cidades["Mun/UF"][row]) # Utiliza o serviço Nominatim para consultar a latitude e a longitude de uma cidade, sem a necessidade de ter ela armazenada na tabela
            coords = ((origem[1], origem[0]),(destino.longitude, destino.latitude))
            routes = client.directions(coords)
            #print("Origem", cidade, "Distância:", routes['routes'][0]['summary']['distance'])
            df.loc[row] = ["Origem", cidade[-2:], cidade[:-2], routes['routes'][0]['summary']['distance']]
            row = row + 1
            time.sleep(1)
        except:
            row = row + 1
            time.sleep(1)