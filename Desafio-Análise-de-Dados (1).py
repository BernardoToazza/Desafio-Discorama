#!/usr/bin/env python
# coding: utf-8

# # Desafio Discorama 

# #### Ideias Iniciais

# A empresa chama-se Discorama tem como objetivo amadurecer na sua cultura do uso de dados por meio de melhor organização e escolha de ferramentas de análise de dados para que aumente o ticket médio e dimuninuindo o atraso médio na devolução de filmes. 

# # Entregas

# O objetivo aqui é de fazer uma análise exploratória que dê base a futuras soluções de negócios que visam o aumento do ticket médio e redução do atraso na devolução dos filmes. O foco foi explorar os dados entendê-los melhor.

# # Sumário
# #### 1. Análise Exploratória
#      A. Sobre o Consumidor:
#         * Consumo total de cada cliente no período; 
#         * Top 100 consumidores do período; 
#         * Ticket médio por gênero; 
#         * Clientes com cadastros inativos; 
#         * Gêneros de filmes mais procurados; 
# #### 2. Insights retirados dos dados
#         * Recuperação de clientes inativos;
#         * Investimento em gêneros com maiores;
#         * Explorar mercados aquecidos;
#         * Diminuição do tempo de atraso
# 

# # Análise Exploratória

# O foco deve sempre ser em torno de aumentar o ticket médio e reduzir o atraso médio na devolução dos filmes. Para aumentar o ticket médio o cliente deve gastar mais a cada compra. A pergunta é: porque ao invés de gastar
# - Identicar qual tabela possui dados sobre alugueis de filme que contenham datas de empréstimo e devolução;
# 

# In[4]:


#Libs
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[5]:


#Importando Data Sets
df_customer = pd.read_csv("C:/Users/toazz/Downloads/discorama/customer.csv", sep = ',', decimal = '.', encoding = 'latin')
df_customer.info()


# In[6]:


df_customer.head()


# In[8]:


#Tratamento Dtype colunas
df_customer['create_date'] = pd.to_datetime(df_customer.create_date)
df_customer['last_upadte'] = pd.to_datetime(df_customer.last_update)


# # Quanto cada pessoa já gastou?
# 

# - Racicínio: Somatório de todas as compras feitas por cada "costumer_id";
# - Quais são os usuários que realmente são relevantes para o negócio? Existem clientes que gastam mais. Clientes que estão com cadastro ativos mas nunca realizaram compras? Normalmente quantos filmes são alugados por compra?
# 

# In[9]:


#Importando DataSet Payment
df_payment = pd.read_csv("C:/Users/toazz/Downloads/discorama/payment.csv", sep = ',', decimal = '.', encoding = 'latin')
df_payment['payment_date'] = pd.to_datetime(df_payment.payment_date)
df_payment.info()


# In[10]:


#Agrupando por "Customer_id" para que saibamos quanto cada cliente já gastou.
df_payment_customer_id = df_payment.groupby(['customer_id'])['amount'].sum()
df_payment_customer_id.nlargest()


# In[11]:


#Plotar a distribuição de consumos 

for i in range(1, 4):
    plt.axvline(np.mean(df_payment_customer_id) + i * np.std(df_payment_customer_id), color='green', linestyle='dashed', linewidth=1)
    plt.axvline(np.mean(df_payment_customer_id) - i * np.std(df_payment_customer_id), color='green', linestyle='dashed', linewidth=1)


faixas_de_consumo = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250]
plt.hist(df_payment_customer_id, bins=faixas_de_consumo, edgecolor='black')
plt.axvline(np.median(df_payment_customer_id), color='red', linestyle='dashed', linewidth=2)
plt.xlabel('Faixas de Consumo')
plt.ylabel('Frequência')
plt.title('Distribuição de Consumo')
plt.show()




# Percebemos que 99,7% de todas os clientes possuem um total de consumo entre 25 a 175 dólares, com uma medianda de consumo em 100 dólares aproximadamente.

# # Quais são os 100 clientes que mais consumiram?

# O objetivo aqui é criar uma lista dos clientes mais importantes para a empresa. Como temos relativamente poucos clientes (600), é importante manter relacionamento com aqueles que são mais frequentes. Sabendo quem são eles podemos criar campan

# In[12]:


top_100_clientes = df_payment_customer_id.nlargest(100)
top_100_clientes_id =  top_100_clientes.index.tolist()
top_100_clientes_id #Lembrando que a lista está em ordem descrente


# # Ticket Médio por Gênero

# Sendo o ticket édio o Somatório dos valores de todos os alugueis por gênero dividido pelo número de aluguéis feitos. A ideia é
# concatenar as quase todas as tabelas de forma lógica e sequencial para que sabendo o "rental_id" (da tabela "Payment") descobrimos quanto cada categoria faturou no período.
# 

# In[13]:


df_payment


# In[14]:


#Importando os datasets necessários
df_rental = pd.read_csv("C:/Users/toazz/Downloads/discorama/rental.csv", sep = ',', decimal = '.', encoding = 'latin')
df_inventory = pd.read_csv("C:/Users/toazz/Downloads/discorama/inventory.csv", sep = ',', decimal = '.', encoding = 'latin')
df_film_category = pd.read_csv("C:/Users/toazz/Downloads/discorama/film_category.csv", sep = ',', decimal = '.', encoding = 'latin')
df_category= pd.read_csv("C:/Users/toazz/Downloads/discorama/category.csv", sep = ',', decimal = '.', encoding = 'latin')



# In[15]:


#Concatenando as tabelas
df_merged = pd.merge(df_payment, df_rental, on = 'rental_id')
df_merged = pd.merge(df_merged, df_inventory, on = 'inventory_id')
df_merged = pd.merge(df_merged, df_film_category, on = 'film_id')
df_merged = pd.merge(df_merged, df_category, on = 'category_id')
df_merged.info()


# In[86]:


df_merged_amount


# In[17]:


#Apresentando graficamente
df_merged_amount = df_merged_amount.sort_values(ascending = False)
plt.barh(df_merged_amount.index, df_merged_amount)
plt.axvline(np.median(df_merged_amount), color='red', linestyle='dashed', linewidth=2)
plt.ylabel('Faturamento')
plt.xlabel('Gênero')
plt.show()


# Observamos que temos Sports despontando na frente com pouco menos de 2000 dólares de faturamento de diferença em relação ao último. Poderíamos checar se estamos planejando comprar uma leva de filmes que se enquadram no top5 com menos faturamento e investir em exemplares de gêneros que possuem mais procura e que possam estar até em falta.
# 

# In[18]:


df_customer.active.count()


# In[19]:


df_customer.active.sum()


# Vemos que há uma diferença entre a contagem das linhas da coluna "Active" e o somatório dos valores em cada linha, sendo "1" sendo considerado ativo e zero inativo. Portanto, temos 35 usuários inativos. Queremos saber quem são eles:

# # Listando os clientes inativos

# In[20]:


#Listando os clientes inativos 
usuarios_inativos = df_customer.loc[df_customer['active'] == 0]
usuarios_inativos.index.tolist()


# Sabemos agora quem são os clientes que não estão mais tidos como ativos, e podemos tomar decisões de entrar em contato para sabermos o porquê de não serem mais consumidores, tentando fazê-los retornarem a consumidor por meio de campanhas promocionais, por exemplo.
# 

# 
# # Distância média entre os clientes e as lojas

# In[21]:


#importando os datasets necessários
df_address = pd.read_csv("C:/Users/toazz/Downloads/discorama/address.csv", sep = ',', decimal = '.', encoding = 'latin')
df_payment.head()


# In[22]:


df_customer


# In[23]:


df_address.head()


# A ideia é que façamos um link entre as tabelas para que no fim tenhamos acesso ao endereço do cliente baseado em seu "payment_id". Assim, poderemos rastrear o faturamento por cidade, estado e país.

# In[24]:


df_merged2 = pd.merge(df_payment, df_customer, on = 'customer_id')
df_merged2= pd.merge(df_merged2, df_address, on = 'address_id')
df_merged2.head()


# In[25]:


df_merged2.city_id.sort_values().unique()


# # Tempo Médio que um filme passa alugado

# In[28]:


df_rental.head()


# In[29]:


from datetime import datetime


#Transformando o dtype das colunas do df_rental para datetime
df_rental['rental_date'] = pd.to_datetime(df_rental.rental_date)
df_rental['return_date'] = pd.to_datetime(df_rental.return_date)
df_rental['dias_alugados'] = (df_rental['return_date'] - df_rental['rental_date']).dt.total_seconds()
df_rental['dias_alugados'] =  df_rental['dias_alugados'] / 86400
df_rental.head(30)


# In[30]:


#Média
df_rental.dias_alugados.mean()


# In[31]:


df_rental.dias_alugados.median()


# # Quais foram os filmes com maior faturamento
# Precisamos concatenar tabelas com as colunas com o nome do filme e Faturamento.
# 

# In[32]:


#importando o dataset film
df_film = pd.read_csv("C:/Users/toazz/Downloads/discorama/film.csv", sep = ',', decimal = '.', encoding = 'latin')
df_merged3 = pd.merge(df_merged, df_film, on = 'film_id')
df_merged3.head()


# In[34]:





# In[33]:


#agrupando por filme
df_merged3.groupby(['category_id'])['amount'].sum().sort_values(ascending = False)
mapping = {1: 'Action', 2: 'Animation', 3: 'Children', 4: "Classics", 5: "Comedy",6: "Documentary", 7: "Drama", 8: "Family",9: "Foreign",10: "Games",11: "Horror", 12: "Music", 13:"New", 14: "Sci-Fi",15:"Sports",16:"Travel"}
df_merged3['category_id'] = df_merged3['category_id'].replace(mapping)
df_merged3.groupby(['store_id','category_id', 'title'])['amount'].sum()


# In[71]:


df_city = pd.read_csv('C:/Users/toazz/Downloads/discorama/city.csv', sep = ',', decimal = '.', encoding = 'latin1')
df_country = pd.read_csv('C:/Users/toazz/Downloads/discorama/country.csv', sep = ',', decimal = '.', encoding = 'latin1')
df_country


# # Faturamento por país

# In[98]:


df_merged2= pd.merge(df_merged2, df_city, on = 'city_id')
df_merged2= pd.merge(df_merged2, df_country, on = 'country')
grouped_country = df_merged2.groupby(['country' ])['amount'].sum().sort_values(ascending = False)
grouped_country


# # Ticket médio por país 

# In[118]:


ticket_país = grouped_country/ grouped_country.count()
ticket_país


# # Conclusão

# In[88]:


df_payment.info()


# In[92]:


revenue_day = df_payment.groupby(df_payment['payment_date'].dt.date).sum()
revenue_day.amount.mean()


# In[ ]:





# # Recupear clientes inativos
# 
# É muito importante fazer o resgate dos 15 clientes inativos. Um consumidor gastou (mediana), cerca de 100 dólares nesse período. No total, seria um acréscimo de 1.500 dólares de faturamento, quase um dia do faturamento das lojas.
# 

# # Investimento em estoques
# 
# Após uma extensa, mas não inútil análise exploratória, como poderíamos tomar decisões para que duas dores nossas sejam melhoradas. Nosso ticket médio por gênero ficou em torno de U$4.0000. Seria interessante fornecer maiores variedades de filmes e aumentar estoques dos top 4 gêneros mais locados (Sports, Sci-Fi, Animation, Drama, Comedy). Evitamos que filmes com alta demanda não sejam alugados por não termos estoques suficientes.
# 
# 

# # Explorar mercados aquecidos
# Mercados como a índia, China, Estados Unidos e México despontam com muita diferença do restante em relação ao ticket médio. São consumidores que gastam mais, o que deve ser levado em consideração nas tomadas de decisões. 
# 
# Ideias de como valorizar os clientes desses países:
# - Criar modelos de clusterização para que sejam recomendados filmes que façam sentidos serem locados conjuntamente;
# - Oferecer descontos em filmes que são sequências. Os consumidores são muito mais propensos a locarem o conjunto da obra;
# - Oferecer planos de aluguéis mensais com determinada quantidade de filmes disponíveis (contando com filmes exclusivos);
# 

# # Diminuição do tempo de atraso
# É importante que as pessoas aluguem os filmes por não tanto tempo. Atualmente o tempo médio é de 5 dias. Caso demore muito, outros clientes a procura desse filme podem ficar sem pela quantidade de tempo que outro cliente utilizou. Pode ser dado benefícios como descontos ou alugueis de filmes gratuitamente após determinado X números de filmes entregues na data correta. Cabe ressaltar a importância de entendermos a função de receita pelo tempo e maximizá-la.

# In[ ]:




