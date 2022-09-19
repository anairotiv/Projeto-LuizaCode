from ast import Return
from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel
from functools import reduce 
        
app = FastAPI()
        
OK = "OK"
FALHA = "FALHA"

@app.get("/")
async def bem_vinda():
            site = "Seja bem vindo(a), e boas compras!"
            return site.replace('\n', '')
        
              
        
        # Classe representando os dados do endereço do cliente
class Endereco(BaseModel):
            id_endereco: int
            rua: str
            cep: str
            cidade: str
            estado: str
            
            def __str__(self) -> str:
                    return self.rua, self.cep, self.cidade, self.estado
        
        # Classe representando os dados do cliente
class Usuario(BaseModel):
            id: int
            nome: str
            email: str
            senha: str
            enderecos: List[Endereco] = []
            
        # Classe representando a lista de endereços de um cliente
class ListaDeEnderecosDoUsuario(BaseModel):
            usuario: Usuario
            #enderecos: List[Endereco] = []
       
        # Classe representando os dados do produto
class Produto(BaseModel):
            id: int
            nome: str
            descricao: str
            preco: float
       
        # Classe representando o carrinho de compras de um cliente com uma lista de produtos
class CarrinhoDeCompras(BaseModel):
            id_usuario: int
            id_produtos: List[Produto] = []
            preco_total: float
            quantidade_de_produtos: int
            

db_usuarios = {}
db_produtos = {}
db_enderecos = {}
db_carrinhos = {}

# Validar Usuários
#def regras_cadastro_usuario(usuario):
   # if usuario.id in db_usuarios:
      #  return FALHA
   # if usuario.email.endswith('@') == -1:
      #  return FALHA
   # if len(usuario.senha) < 3:
     #   return FALHA
   # return usuario(criar_usuário)
       
        
@app.post("/usuario/")
async def criar_usuário(usuario: Usuario):
            if usuario.id not in db_usuarios:
                 db_usuarios[usuario.id] = usuario
                 return OK, 'O usuário foi cadastrado no nosso banco de dados!'
            return FALHA
            
         
@app.get("/usuario/")
async def retornar_usuario(id: int):
            if id in db_usuarios:
                return db_usuarios[id]
            return FALHA, f'usuário não foi encontrado!'
     
        

@app.get("/usuario/nome")
async def retornar_usuario_com_nome(nome: str):
    for usuario in db_usuarios.values():
        if usuario.nome == nome:
            return f'id: {usuario.id}, nome: {usuario.nome}, email: {usuario.email}, senha: {usuario.senha}'
            
    return FALHA

# @app.get("/usuario/nome")
# async def retornar_usuario_com_nome(nome):
#                 for nome in db_usuarios:
#                     if nome == nome:
#                         return db_usuarios[nome]
#                     else:
#                         return FALHA
                
                
@app.delete("/usuario/id")
async def deletar_usuario(id: int):
            if id in db_usuarios:
                del db_usuarios[id]
                return "usuário deletado da nossa base de dados"
            else:
                return FALHA   
        
@app.post("/endereco/{id_usuario}/")
async def criar_endereco(end: Endereco, id_usuario: int):
            if id_usuario not in db_usuarios.keys():
                return FALHA, 'usuario não cadastrado'
            for endereco in db_usuarios[id_usuario].enderecos:
                if end == endereco:
                    return FALHA, 'endereco já cadastrado'
            db_usuarios[id_usuario].enderecos.append(end)
            return OK
            
@app.delete("/endereco/{id_endereco}/")
async def deletar_endereco(id_endereco: int):
            if id_endereco in db_enderecos:
                db_enderecos.pop(id_endereco)
                return OK
            return FALHA
                  
        # Se não existir usuário com o id_usuario retornar falha, 
        # senão retornar uma lista de todos os endereços vinculados ao usuário
        # caso o usuário não possua nenhum endereço vinculado a ele, retornar 
        # uma lista vazia
        ### Estudar sobre Path Params (https://fastapi.tiangolo.com/tutorial/path-params/)
        # não consegui ainda
        
# @app.get("/usuario/")
# async def retornar_usuario(id: int):
#             if id in db_usuarios:
#                 return db_usuarios[id]
#             return FALHA, f'usuário não foi encontrado!'
     
@app.get("/usuario/{id_usuario}/enderecos/")
async def retornar_enderecos_do_usuario(id_usuario: int):
           if id_usuario in db_usuarios:
               return db_usuarios[id_usuario]
           return FALHA


@app.get("/usuarios/emails/{dominio_requisitado}")
async def retornar_emails(dominio_requisitado):
    lista_dominios = []
    for id_usuario, dados_usuario in db_usuarios.items():
        dominio = dados_usuario.email.split("@")[1]
        if "dominio=@" + dominio == dominio_requisitado:
            lista_dominios.append(dados_usuario.email)
    return lista_dominios

   
@app.post("/produto/")
async def criar_produto(produto: Produto):
             if produto.id not in db_produtos:
                 db_produtos[produto.id] = produto
                 return OK, 'O produto foi cadastrado no nosso banco de dados!'
             return FALHA
            

@app.get("/produto/{id_produto}/")
async def consultar_produto(id_produto: int):
        if id_produto in db_produtos:
                return db_produtos[id_produto]
        return FALHA, f'usuário não foi encontrado!'
      
      
@app.delete("/produto/{id_produto}/")
async def deletar_produto(id_produto: int):
    if id_produto in db_produtos:
                del db_produtos[id_produto]
                return OK, 'O produto foi descartado com sucesso'

def cria_carrinho(id_usuario):
    db_carrinhos[id_usuario] = {
        
        'id_usuario': 1,
        'id_produtos': {},
        'preco_total': 0,
        'quantidade_de_produtos': 0
    }        

#adicionando item no carrinho"        
@app.post("/carrinho/{id_usuario}/{id_produto}{quantidade}/")
async def adicionar_item_carrinho(id_usuario, id_produto, quantidade):
        db_carrinhos[id_usuario]['i_produtos'][id_produto] =({
            "id": id_produto,
            "quantidade": quantidade
        })
        
        db_carrinhos[id_usuario]['quantidade_de_produtos'] += quantidade
        db_carrinhos[id_usuario]['preco_total'] += db_produtos[id_produto].preco * quantidade
        print(db_carrinhos)

        # Adicionando item no carrinho   
@app.post("/carrinho/{id_usuario}/{id_produto}/{quantidade}/")
async def adicionar_carrinho(id_usuario: int, id_produto: int, quantidade: int):
    if not id_usuario in db_usuarios or not id_produto in db_produtos:
        return FALHA
    if not id_usuario in db_carrinhos:
        cria_carrinho(id_usuario)
        adicionar_item_carrinho(id_usuario, id_produto, quantidade)
        return OK
    else :
        adicionar_item_carrinho(id_usuario, id_produto, quantidade)
        return OK
    
                  
#ainda não"
@app.get("/carrinho/{id_usuario}/")
async def retornar_carrinho(id_usuario: int):
            if id_usuario in db_carrinhos:
                return db_carrinhos[id_usuario]
            return FALHA
            
# Buscando total do carrinho de um usuário
@app.get("/carrinho/{id_usuario}/total")
async def retornar_total_carrinho(id_usuario: int):
    if id_usuario in db_carrinhos:
        return db_carrinhos[id_usuario]['quantidade_de_produtos'],    
    db_carrinhos[id_usuario]['preco_total'] 
    return FALHA
            

    
@app.delete("/carrinho/{id_usuario}/")
async def deletar_carrinho(id_usuario: int):
            if id_usuario not in db_usuarios:
                return FALHA
            else:
                del db_carrinhos[id_usuario]
                return OK
        