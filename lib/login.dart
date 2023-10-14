import 'dart:convert';              // JSON

import 'package:http/http.dart';    // making API calls
import 'package:html/parser.dart';  // HTML parsers

const url = 'http://webap.nkust.edu.tw/nkust/';

Future initiate(BaseClient client) async {
  Response response = await client.get(
    url + 'index_main.html'
  );
  
  var html = utf8.decode(response.bodyBytes);
  var document = parse(html);
  var verifyCode = document.getElementById('verifyCode');

  print(verifyCode.attributes);
}