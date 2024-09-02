import 'dart:io';

List<List<int>> encontrarSubconjuntos(List<int> conjunto) {
  List<List<int>> subconjuntos = [[]];

  for (int numero in conjunto) {
    int tamanhoAtual = subconjuntos.length;
    for (int i = 0; i < tamanhoAtual; i++) {
      List<int> subconjuntoNovo = List.from(subconjuntos[i]);
      subconjuntoNovo.add(numero);
      subconjuntos.add(subconjuntoNovo);
    }
  }

  return subconjuntos;
}

void main() {
  print('Informe os números separados por espaço:');
  String? entrada = stdin.readLineSync();

  if (entrada != null) {
    List<int> numeros = entrada.split(' ').map(int.parse).toList();
    List<List<int>> resultado = encontrarSubconjuntos(numeros);

    print('Subconjuntos:');
    print(resultado);
  } else {
    print('Nenhuma entrada recebida.');
  }
}
