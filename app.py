from flask import Flask, redirect, request, url_for


app = Flask(__name__)

# Lista que simula o carrinho inteligente
carrinho = []

# Produtos estruturados com comparador de preço e identidade em vermelho/estrelas
produtos = {
    'tomate': {
        'nome': 'Tomate Especial (kg)',
        'preco': 1.99,
        'comparativo': '⭐ R$ 1,99 por kg (Melhor preço da semana!)',
        'alergicos': '⚠️ NÃO CONTÉM GLÚTEN',
        'icone': '🍅',
        'local': 'Corredor 4, Prateleira 1',
    },
    'arroz': {
        'nome': 'Arroz Tipo 1 (5kg)',
        'preco': 21.90,
        'comparativo': '⭐ R$ 4,38 por kg',
        'alergicos': '⚠️ NÃO CONTÉM GLÚTEN',
        'icone': '🍚',
        'local': 'Corredor 3, Prateleira 2',
    },
    'aveia': {
        'nome': 'Aveia em Flocos (500g)',
        'preco': 6.50,
        'comparativo': '⭐ R$ 13,00 por kg',
        'alergicos': '⚠️ PODE CONTER TRAÇOS DE GLÚTEN',
        'icone': '🥣',
        'local': 'Corredor 4, Prateleira 1',
    },
    'feijao': {
        'nome': 'Feijão Preto (1kg)',
        'preco': 8.50,
        'comparativo': '⭐ R$ 8,50 por kg',
        'alergicos': '⚠️ NÃO CONTÉM GLÚTEN',
        'icone': '🫘',
        'local': 'Corredor 2, Prateleira 3',
    },
    'leite': {
        'nome': 'Leite Integral (1L)',
        'preco': 4.80,
        'comparativo': '⭐ R$ 4,80 por litro',
        'alergicos': '⚠️ CONTÉM LACTOSE',
        'icone': '🥛',
        'local': 'Corredor 5, Prateleira 1',
    },
}


# --- TELA INICIAL (Com Suporte a Modo Escuro/Claro) ---
@app.route('/')
def inicio():
  total_itens = len(carrinho)
  termo_busca = request.args.get('q', '').lower()
  tema = request.args.get('tema', 'claro')

  # Cores dinâmicas para o Modo Escuro ou Claro
  if tema == 'escuro':
    bg_geral = '#121212'
    bg_card = '#1e1e1e'
    texto = '#ffffff'
    borda = '#333333'
    input_bg = '#2a2a2a'
  else:
    bg_geral = '#f5f5f5'
    bg_card = '#ffffff'
    texto = '#333333'
    borda = '#ffcccc'
    input_bg = '#ffffff'

  grid_produtos = ''
  for id_p, p in produtos.items():
    if termo_busca and termo_busca not in p['nome'].lower():
      continue

    grid_produtos += f"""
        <a href="/produto/{id_p}?tema={tema}" style="text-decoration: none; color: inherit;">
            <div style="border: 1px solid {borda}; border-radius: 8px; padding: 10px; background: {bg_card}; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 38px; margin: 5px 0;">{p['icone']}</div>
                <p style="font-size: 12px; font-weight: bold; margin: 6px 0 4px 0; color: {texto};">{p['nome']}</p>
                <span style="color: #e74c3c; font-weight: bold; font-size: 13px;">R$ {p['preco']:.2f}</span>
                <div style="font-size: 10px; color: #ff6b6b; margin-top: 3px;">⭐ {p['comparativo'].split('(')[0]}</div>
            </div>
        </a>
        """

  if not grid_produtos:
    grid_produtos = f'<p style="grid-column: span 2; color: gray; font-size: 13px; text-align: center;">Nenhum produto encontrado.</p>'

  outro_tema = 'escuro' if tema == 'claro' else 'claro'
  texto_botao_tema = '🌙 Escuro' if tema == 'claro' else '☀️ Claro'

  return f"""
    <body style="background-color: {bg_geral}; margin: 0; padding: 0;">
    <div style="background: {bg_card}; border-radius: 12px; width: 360px; margin: 20px auto; box-shadow: 0px 0px 15px rgba(0,0,0,0.3); font-family: Arial; overflow: hidden; color: {texto};">
        
        <!-- BARRA DO TOPO -->
        <div style="background: #c0392b; color: white; padding: 12px 15px; display: flex; justify-content: space-between; align-items: center; font-size: 14px;">
            <span>⚙️ Config</span>
            <span style="font-weight: bold;">⭐  </span>
            <a href="/?tema={outro_tema}" style="color: white; text-decoration: none; font-size: 12px; background: rgba(0,0,0,0.2); padding: 4px 8px; border-radius: 4px;">{texto_botao_tema}</a>
        </div>

        <div style="padding: 20px;">
            <h1 style="color: #c0392b; margin: 0 0 5px 0; text-align: center; font-size: 22px;">⭐ Mercado Dia a Dia</h1>
            <p style="color: {'#aaa' if tema == 'escuro' else '#666'}; font-size: 12px; text-align: center; margin-bottom: 15px;">Economia garantida com comparador de preços!</p>

            <!-- BARRA DE PESQUISA -->
            <form action="/" method="GET" style="margin-bottom: 15px; display: flex; gap: 5px;">
                <input type="hidden" name="tema" value="{tema}">
                <input type="text" name="q" value="{termo_busca}" placeholder="🔍 Pesquisar produto..." style="flex: 1; padding: 8px 10px; border: 1px solid {borda}; background: {input_bg}; color: {texto}; border-radius: 20px; outline: none; font-size: 13px;">
                <button type="submit" style="background: #c0392b; color: white; border: none; padding: 8px 12px; border-radius: 20px; cursor: pointer; font-size: 12px; font-weight: bold;">Ir</button>
            </form>

            <!-- CARD DO CARRINHO -->
            <div style="background: {'#332712' if tema == 'escuro' else '#fdebd0'}; padding: 10px 15px; border-radius: 8px; border: 1px solid {'#7d6608' if tema == 'escuro' else '#f8c471'}; display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <span style="font-size: 13px; font-weight: bold; color: {'#f1c40f' if tema == 'escuro' else '#b9770e'};">🛒 Lista: {total_itens} item(ns)</span>
                <a href="/carrinho?tema={tema}" style="color: {'#f39c12' if tema == 'escuro' else '#d35400'}; font-weight: bold; text-decoration: none; font-size: 12px;">Ver Total ➔</a>
            </div>

            <!-- GRADE DE PRODUTOS -->
            <h3 style="font-size: 14px; color: {texto}; margin-bottom: 10px;">⭐ Produtos em Destaque:</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; max-height: 250px; overflow-y: auto; padding-right: 2px;">
                {grid_produtos}
            </div>

            <br>
            <button onclick="document.getElementById('modalOferta').showModal()" style="background: #e74c3c; color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; font-size: 13px;">
                🔥 Ver Oferta Especial
            </button>
        </div>
    </div>

    <!-- MODAL FLUTUANTE -->
    <dialog id="modalOferta" style="background: {bg_card}; color: {texto}; padding: 20px; border-radius: 10px; border: 1px solid {borda}; box-shadow: 0px 0px 20px rgba(0,0,0,0.5); text-align: center; font-family: Arial; width: 280px;">
        <h3 style="color: #c0392b; margin-top: 0;">⭐ Super Promoção!</h3>
        <p style="font-size: 14px;">Leve 2 pacotes de Arroz por R$ 38,00!</p>
        <p style="font-size: 12px; color: {'#aaa' if tema == 'escuro' else '#7f8c8d'};">📍 Corredor 3, Prateleira 2</p>
        <br>
        <button onclick="document.getElementById('modalOferta').close()" style="background: #c0392b; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 12px;">
            Fechar [X]
        </button>
    </dialog>
    </body>
    """


# --- PÁGINA DETALHADA DO PRODUTO ---
@app.route('/produto/<id_prod>')
def pagina_produto(id_prod):
  p = produtos.get(id_prod)
  tema = request.args.get('tema', 'claro')

  if tema == 'escuro':
    bg_geral = '#121212'
    bg_card = '#1e1e1e'
    texto = '#ffffff'
    borda = '#333333'
  else:
    bg_geral = '#f5f5f5'
    bg_card = '#ffffff'
    texto = '#333333'
    borda = '#ffcccc'

  if not p:
    return 'Produto não encontrado', 404

  return f"""
    <body style="background-color: {bg_geral}; margin: 0; padding: 0;">
    <div style="background: {bg_card}; border-radius: 12px; width: 360px; margin: 20px auto; box-shadow: 0px 0px 15px rgba(0,0,0,0.3); font-family: Arial; overflow: hidden; color: {texto};">
        
        <div style="background: #c0392b; color: white; padding: 12px 15px; font-size: 14px; display: flex; justify-content: space-between; align-items: center;">
            <a href="/?tema={tema}" style="color: white; text-decoration: none; font-weight: bold;">← Voltar à Vitrine</a>
            <a href="/produto/{id_prod}?tema={'escuro' if tema == 'claro' else 'claro'}" style="color: white; text-decoration: none; font-size: 12px; background: rgba(0,0,0,0.2); padding: 4px 8px; border-radius: 4px;">{'🌙 Escuro' if tema == 'claro' else '☀️ Claro'}</a>
        </div>

        <div style="padding: 20px; text-align: center;">
            <h2 style="color: #c0392b; margin: 0 0 5px 0; font-size: 20px;">{p['nome']}</h2>
            <div style="font-size: 64px; margin: 15px 0;">{p['icone']}</div>
            
            <h1 style="color: #27ae60; margin: 0 0 5px 0; font-size: 26px;">R$ {p['preco']:.2f}</h1>
            
            <div style="background: {'#332712' if tema == 'escuro' else '#fef9e7'}; padding: 8px; border-radius: 6px; border: 1px solid {'#7d6608' if tema == 'escuro' else '#f9e79f'}; margin: 10px 0; font-size: 12px; color: {'#f1c40f' if tema == 'escuro' else '#b7950b'}; font-weight: bold;">
                {p['comparativo']}
            </div>

            <p style="color: {'#aaa' if tema == 'escuro' else '#7f8c8d'}; font-size: 13px; margin-bottom: 10px;">📍 <b>{p['local']}</b></p>
            
            <div style="background: {'#4a1515' if tema == 'escuro' else '#fadbd8'}; padding: 10px; border-radius: 6px; border: 1px solid {'#922b21' if tema == 'escuro' else '#f5b7b1'}; margin-bottom: 20px; font-size: 13px; color: {'#f5b7b1' if tema == 'escuro' else '#922b21'}; font-weight: bold;">
                {p['alergicos']}
            </div>

            <a href="/adicionar/{id_prod}?tema={tema}" style="background: #c0392b; color: white; padding: 12px; text-decoration: none; border-radius: 6px; font-weight: bold; display: block; font-size: 14px;">🛒 Adicionar à Lista de Compras</a>
        </div>
    </div>
    </body>
    """


# --- ROTA ADICIONAR AO CARRINHO ---
@app.route('/adicionar/<id_prod>')
def adicionar(id_prod):
  tema = request.args.get('tema', 'claro')
  p = produtos.get(id_prod)
  if p:
    carrinho.append(p)
  return redirect(url_for('ver_carrinho', tema=tema))


# --- TELA DO CARRINHO ---
@app.route('/carrinho')
def ver_carrinho():
  tema = request.args.get('tema', 'claro')

  if tema == 'escuro':
    bg_geral = '#121212'
    bg_card = '#1e1e1e'
    texto = '#ffffff'
    borda = '#333333'
  else:
    bg_geral = '#f5f5f5'
    bg_card = '#ffffff'
    texto = '#333333'
    borda = '#ffcccc'

  total = sum(item['preco'] for item in carrinho)
  itens_html = ''
  for item in carrinho:
    itens_html += f"""
        <li style="margin-bottom: 8px; border-bottom: 1px solid {borda}; padding-bottom: 5px; text-align: left; font-size: 13px; color: {texto};">
            <b>{item['icone']} {item['nome']}</b> - R$ {item['preco']:.2f} 
            <br><span style="font-size: 11px; color: {'#aaa' if tema == 'escuro' else 'gray'};">📍 {item['local']}</span>
        </li>
        """

  return f"""
    <body style="background-color: {bg_geral}; margin: 0; padding: 0;">
    <div style="background: {bg_card}; border-radius: 12px; width: 360px; margin: 20px auto; box-shadow: 0px 0px 15px rgba(0,0,0,0.3); font-family: Arial; overflow: hidden; color: {texto};">
        
        <div style="background: #c0392b; color: white; padding: 12px 15px; font-size: 14px; display: flex; justify-content: space-between; align-items: center;">
            <a href="/?tema={tema}" style="color: white; text-decoration: none; font-weight: bold;">← Continuar Comprando</a>
            <a href="/carrinho?tema={'escuro' if tema == 'claro' else 'claro'}" style="color: white; text-decoration: none; font-size: 12px; background: rgba(0,0,0,0.2); padding: 4px 8px; border-radius: 4px;">{'🌙 Escuro' if tema == 'claro' else '☀️ Claro'}</a>
        </div>

        <div style="padding: 20px; text-align: center;">
            <h2 style="color: #c0392b; margin-top: 0;">🛒 Lista de Compras Inteligente</h2>
            
            <ul style="list-style-type: none; padding: 0; max-height: 180px; overflow-y: auto; margin: 15px 0;">
                {itens_html if carrinho else f'<p style="color: {"#aaa" if tema == "escuro" else "gray"}; font-size: 13px;">Sua lista está vazia.</p>'}
            </ul>
            
            <hr style="border: 0; border-top: 1px solid {borda}; margin: 15px 0;">
            <h3 style="color: {texto}; margin: 5px 0;">Total: R$ {total:.2f}</h3>
            <br>
            <a href="/limpar?tema={tema}" style="color: #e74c3c; text-decoration: none; font-size: 12px;">Esvaziar Lista</a>
        </div>
    </div>
    </body>
    """


# --- ROTA LIMPAR CARRINHO ---
@app.route('/limpar')
def limpar():
  tema = request.args.get('tema', 'claro')
  carrinho.clear()
  return redirect(url_for('ver_carrinho', tema=tema))


if __name__ == '__main__':
  app.run(debug=True)
