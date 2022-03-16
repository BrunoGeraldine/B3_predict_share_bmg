#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[1]:


import pandas as pd


# ## Load files

# In[36]:



def read_files(path, name_file, year_date, type_file):
    
    _file = f'{path}{name_file}{year_date}.{type_file}'
    
    cols_position = [(2,10),
                (10,12),
                (12,24),
                (27,39),
                (56,69),
                (69,82),
                (82,95),
                (108,121),
                (152,170),
                (170, 178)]
    
    cols_name = ['data_pregao', 'codbdi', 'sigla_acao',
                 'nome_acao', 'preco_abertura', 'preco maximo',
                 'preco_minimo', 'preco_fechamento', 'qtd_negocios',
                 'volume_negocios']
    
    df = pd.read_fwf(_file , colspecs=cols_position, names=cols_name, skiprows=1)
    
    return df


# In[ ]:


# antes da construção da função
# cols_position = [(2,10),
#             (10,12),
#             (12,24),
#             (27,39),
#             (56,69),
#             (69,82),
#             (82,95),
#             (108,121),
#             (152,170),
#             (170, 178)]
# 
# cols_name = ['data_pregao', 'codbdi', 'sigla_acao',
#              'nome_acao', 'preco_abertura', 'preco maximo',
#              'preco_minimo', 'preco_fechamento', 'qtd_negocios',
#              'volume_negocios']
# 
# df = pd.read_fwf('../data/external/COTAHIST_A2019.TXT', colspecs=cols_position, names=cols_name, skiprows=1)


# In[37]:


# Filtering data to codbdi == 2 and drop column

def filter_shares(df):
    df = df[df['codbdi']==2]
    df = df.drop(['codbdi'], axis=1)
    
    return df


# In[38]:



# Ajusta datetime
def parse_date(df):
    df1['data_pregao'] = pd.to_datetime(df1['data_pregao'], format='%Y%m%d')
    
    return df

# Ajuste Campo Numericos
def parse_numerical(df):
    df1['codbdi'] = df1['codbdi'].astype(int)
    df1['qtd_negocios'] = df1['qtd_negocios'].astype(int)
    df1['volume_negocios'] = df1['volume_negocios'].astype(int)
    
    return df


# In[41]:


# data concat

def concat_files(path, name_file, year_date, type_file, final_file):
    
    for i, y in enumerate(year_date):
        df = read_files(path, name_file, y, type_file)
        df = filter_shares(df)
        df = parse_date(df)
        df = parse_numerical(df)
        
        if i==0:
            df_final = df
        else:
            df_final = pd.concat([df_final, df])
    
    df_final.to_csv(f'{path}/{final_file}', index=False)


# In[44]:


# Execução do script:
year_date = ['2019', '2020', '2021']

path = f'/home/bruno/repos/B3_predict_share_bmg/data/'

name_file = 'COTAHIST_A'

type_file = 'TXT'

final_file = 'b3_bovespa.csv'

concat_files(path,name_file,year_date,type_file,final_file)


# In[ ]:




