from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

carrinho = []

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


@app.route('/')
def inicio():
  termo_busca = request.args.get('q', '').lower()
  tema = request.args.get('tema', 'claro')

  # Filtra os produtos caso haja pesquisa
  produtos_filtrados = {}
  for id_p, p in produtos.items():
    if not termo_busca or termo_busca in p['nome'].lower():
      produtos_filtrados[id_p] = p

  return render_template(
      'index.html',
      produtos=produtos_filtrados,
      carrinho=carrinho,
      termo_busca=termo_busca,
      tema=tema,
      pagina='inicio',
  )


@app.route('/produto/<id_prod>')
def pagina_produto(id_prod):
  p = produtos.get(id_prod)
  tema = request.args.get('tema', 'claro')

  if not p:
    return 'Produto não encontrado', 404

  return render_template(
      'index.html',
      produto=p,
      id_prod=id_prod,
      tema=tema,
      pagina='detalhes',
  )


@app.route('/adicionar/<id_prod>')
def adicionar(id_prod):
  tema = request.args.get('tema', 'claro')
  p = produtos.get(id_prod)
  if p:
    carrinho.append(p)
  return redirect(url_for('ver_carrinho', tema=tema))


@app.route('/carrinho')
def ver_carrinho():
  tema = request.args.get('tema', 'claro')
  total = sum(item['preco'] for item in carrinho)

  return render_template(
      'index.html',
      carrinho=carrinho,
      total=total,
      tema=tema,
      pagina='carrinho',
  )


@app.route('/limpar')
def limpar():
  tema = request.args.get('tema', 'claro')
  carrinho.clear()
  return redirect(url_for('ver_carrinho', tema=tema))


if __name__ == '__main__':
  app.run(debug=True)