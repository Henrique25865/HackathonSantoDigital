import 'dart:io';

void main() {
  print("Informe um número");
  int num = int.parse(stdin.readLineSync()!);
  String a = "*";
  List list = [];

  for (int i = 0; i < num; i++) {
    list.add(a * (i + 1));
  }
  print(list);
}
