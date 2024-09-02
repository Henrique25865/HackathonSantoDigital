import 'dart:io';

void main() async {
  // Mapa com as perguntas e os caminhos dos scripts
  Map<String, String> scripts = {
    'Quais são os 10 produtos mais vendidos (em quantidade) na categoria "Bicicletas", considerando apenas vendas feitas nos últimos dois anos?': 'scripts/dart/top10Products.dart',
    'Qual é o cliente que tem o maior número de pedidos realizados, considerando apenas clientes que fizeram pelo menos um pedido em cada trimestre do último ano fiscal?': 'scripts/dart/topCostumerOrders.dart',
    'Em qual mês do ano ocorrem mais vendas (em valor total), considerando apenas os meses em que a receita média por venda foi superior a 500 unidades monetárias?': 'scripts/dart/topMonthSales.dart',
    'Quais vendedores tiveram vendas com valor acima da média no último ano fiscal e também tiveram um crescimento de vendas superior a 10% em relação ao ano anterior?': 'scripts/dart/topSellersGrowth.dart',
  };

  // Linha separadora
  String getSeparator(int length) => '-' * length;

  print('\n${getSeparator(50)}\n');

  // Itera sobre cada pergunta e script
  for (MapEntry<String, String> entry in scripts.entries) {
    String question = entry.key;
    String scriptPath = entry.value;

    // Exibe a pergunta
    print('$question\n');

    // Executa o script
    ProcessResult result = await Process.run('dart', [scriptPath]);

    if (result.exitCode == 0) {
      // Exibe a saída do script
      print('${result.stdout}');
    } else {
      // Exibe o erro caso ocorra
      print('Erro ao executar $scriptPath:\n${result.stderr}');
    }

    print('\n${getSeparator(50)}\n');
    await Future.delayed(const Duration(seconds: 2));
  }
}
