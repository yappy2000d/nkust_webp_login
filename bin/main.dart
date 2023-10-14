import 'package:NKUST_WEBP_LOGIN/login.dart' as login;
import 'package:http/http.dart';

void main(List<String> arguments) async {
  await login.initiate(Client());
}