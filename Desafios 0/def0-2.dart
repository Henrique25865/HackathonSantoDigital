import 'dart:io';

List<List<int>> encontrarParesComMenorDiferenca(List<int> numeros) {
  numeros.sort();
  
  int menorDiferenca = numeros[1] - numeros[0];
  List<List<int>> resultado = [];

  for (int i = 1; i < numeros.length; i++) {
    int diferenca = numeros[i] - numeros[i - 1];
    if (diferenca < menorDiferenca) {
      menorDiferenca = diferenca;
      resultado = [[numeros[i - 1], numeros[i]]];
    } else if (diferenca == menorDiferenca) {
      resultado.add([numeros[i - 1], numeros[i]]);
    }
  }

  return resultado;
}

void main() {
  print('Digite os números separados por espaço:');
  String? entrada = stdin.readLineSync();

  if (entrada != null && entrada.isNotEmpty) {
    List<int> numeros = entrada.split(' ').map(int.parse).toList();
    List<List<int>> pares = encontrarParesComMenorDiferenca(numeros);
    print('Os pares com a menor diferença são: $pares');
  } else {
    print('Nenhum número foi informado.');
  }
}
