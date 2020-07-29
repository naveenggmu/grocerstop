import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:grocerstop/home_screen.dart';
import 'package:grocerstop/login.dart';

void main() {
    runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle(statusBarColor: Colors.blue));
    return MaterialApp(
      title: 'GrocerStop',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: LoginScreen(),
    );
  }
}