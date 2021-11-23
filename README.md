# Parser de Cardápio do RU
A problemática envolve conseguir dados do cardápio do restaurante universitário da Universidade de Brasília de maneira automatizada. Pensando nisso, o parser lê os dados do cardápio passado como argumento e retorna um JSON com os dados.

## Tecnologia
Feito em Python. Utiliza as bilbiotecas Camelot, NumPy e Json.

## Execucação:

Para rodar, use: 
```sh
python parser.py [arquivo].pdf
```

## Saída:

Gera um arquivo **data.json** no seguinte formato:
```sh
[
  {
    "date": "23/11",
    "week_day": "monday",
    "breakfast": [],
    "lunch": [],
    "dinner": []
  },
]
```

## Bugs
- É necessário setar um inicio para as subtabelas.
- Certas colunas grandes (que ocupam uma linha inteira) tem seu valor inserido em uma subtabela.
- Subarrays sem uma chave definida dentro dos atributos de refeição. Envolve decisão de arquitetura do JSON final.