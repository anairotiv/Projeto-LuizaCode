from ast import Return
import email
from genericpath import exists
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
        
app = FastAPI()
        
OK = "OK"
FALHA = "FALHA"
              
        
        # Classe representando os dados do endereço do cliente
class Endereco(BaseModel):
            rua: str
            cep: str
            cidade: str
            estado: str
        
        # Classe representando os dados do cliente
class Usuario(BaseModel):
            id: int
            nome: str
            email: str
            senha: str
            
       
        # Classe representando a lista de endereços de um cliente
class ListaDeEnderecosDoUsuario(BaseModel):
            usuario: Usuario
            enderecos: List[Endereco] = []
       
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
db_end = {}
db_carrinhos = {}


# Validar Usuários
# def regras_cadastro_usuario(usuario):
#     if usuario.id in db_usuarios:
#         return FALHA
#     if usuario.email.endswith('@') == -1:
#         return FALHA
#     if len(usuario.senha) < 3:
#         return FALHA
#     return usuario(criar_usuário)
       
        
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
            return FALHA
     
        
@app.get("/usuario/nome")
async def retornar_usuario_com_nome(nome):
                for nome in db_usuarios:
                    if nome == nome:
                        return db_usuarios[nome]
                    else:
                        return FALHA
                
        
@app.delete("/usuario/")
async def deletar_usuario(id: int):
            if id in db_usuarios:
                del db_usuarios[id]
                return "o usuário foi deletado do nosso banco de dados com sucesso"
            
        # Se não existir usuário com o id_usuario retornar falha, 
        # senão retornar uma lista de todos os endereços vinculados ao usuário
        # caso o usuário não possua nenhum endereço vinculado a ele, retornar 
        # uma lista vazia
        ### Estudar sobre Path Params (https://fastapi.tiangolo.com/tutorial/path-params/)
@app.get("/usuario/{id_usuario}/endereços/")
async def retornar_enderecos_do_usuario(id_usuario: int):
            if id_usuario not in db_usuarios:
                return FALHA
            else:
                db_usuarios = id_usuario[id_usuario]
        
        
        
@app.get("/usuarios/emails/")
async def retornar_emails(dominio: str):
            if email == dominio:
                return dominio[dominio]
            
#@app.get("/usuarios/emails/")
#async def retornar_emails(dominio: str):
            #if dominio.endswith: "@gmail.com"
            #return dominio
        
        
        
        
        # Se não existir usuário com o id_usuario retornar falha, 
        # senão cria um endereço, vincula ao usuário e retornar OK
# endereco = {
#     1: {"rua":"pompeia0", "número":31, "cep":25455},
#     2: {"rua":"pompeia1", "número":32, "cep":25455},
#     3: {"rua":"pompeia2", "número":33, "cep":25455},
#     4: {"rua":"pompeia3", "número":34, "cep":25455},
#     5: {"rua":"pompeia4", "número":35, "cep":25455},
#     }

@app.post("/endereco/{id_usuario}/")
async def criar_endereco(endereco: Endereco, id_usuario: int):
            return OK
        
        # Se não existir endereço com o id_endereco retornar falha, 
        # senão deleta endereço correspondente ao id_endereco e retornar OK
        # (lembrar de desvincular o endereço ao usuário)
@app.delete("/endereco/{id_endereco}/")
async def deletar_endereco(id_endereco: int):
            if id_endereco in db_usuarios:
                return OK
            else:
                del db_usuarios[id_endereco]
        
    
        # Se tiver outro produto com o mesmo ID retornar falha, 
        # senão cria um produto e retornar OK
        
@app.post("/produto/")
async def criar_produto(produto: Produto):
            return OK
        
        # Se não existir produto com o id_produto retornar falha, 
        # senão deleta produto correspondente ao id_produto e retornar OK
        # (lembrar de desvincular o produto dos carrinhos do usuário)
@app.delete("/produto/{id_produto}/")
async def deletar_produto(id_produto: int):
            if id_produto in db_produtos:
                del db_produtos[id_produto]
                return OK
            
        
        
        # Se não existir usuário com o id_usuario ou id_produto retornar falha, 
        # se não existir um carrinho vinculado ao usuário, crie o carrinho
        # e retornar OK
        # senão adiciona produto ao carrinho e retornar OK
@app.post("/carrinho/{id_usuario}/{id_produto}/")
async def adicionar_carrinho(id_usuario: int, id_produto: int):
            return OK
        
        
        # Se não existir carrinho com o id_usuario retornar falha, 
        # senão retorna o carrinho de compras.
@app.get("/carrinho/{id_usuario}/")
async def retornar_carrinho(id_usuario: int):
            return CarrinhoDeCompras
        
        
        # Se não existir carrinho com o id_usuario retornar falha, 
        # senão retorna o o número de itens e o valor total do carrinho de compras.
        #criar uma instancia precisa invocar
        #buug
@app.get("/carrinho/{id_usuario}/")
async def retornar_total_carrinho(id_usuario: int):
            numero_itens, valor_total = 0
            return numero_itens, valor_total
    
    
        # Se não existir usuário com o id_usuario retornar falha, 
        # senão deleta o carrinho correspondente ao id_usuario e retornar OK
@app.delete("/carrinho/{id_usuario}/")
async def deletar_carrinho(id_usuario: int):
            if id_usuario not in db_usuarios:
                return FALHA
            else:
                del db_carrinhos[id_usuario]
                return OK
        
        
@app.get("/")
async def bem_vinda():
            site = "Seja bem vinda"
            return site.replace('\n', '')
        
        
        
        #buscar o carrinho e retornar ele ao inves de criar um novo.