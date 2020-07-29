import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qrscan/qrscan.dart' as scanner;
import 'package:http/http.dart' as http;

class HomeScreen extends StatefulWidget {
  final details;

  HomeScreen(this.details);

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  void scanCustomer() async {
    final val = await scanner.scan();
    const url = 'http://fd7ea7a0d93c.ngrok.io/flutterUserVerify';
    try {
      final response = await http.post(url,
          body: json.encode({
            'val': val,
            'shop_id': widget.details['shop_id'],
          }));
      print(response.body);
      final res = json.decode(response.body);
      var text = "";
      var image = "";
      var fit;
      if (res['status'] == true) {
        text = "User Verified!";
        image =
            'https://cdn.dribbble.com/users/791530/screenshots/6827794/clip-illustration-style-icons8.png';
        fit = BoxFit.cover;
      } else {
        text = "Verification Failed.";
        image =
        'https://cdn.dribbble.com/users/1102193/screenshots/6375792/thief-01.png';
        fit = BoxFit.fitHeight;
      }
      showDialog(
          context: context,
          builder: (context) => AlertDialog(
                title: Text(text),
                content: Image.network(
                  image,
                  height: 200,
                  fit: BoxFit.cover,
                ),
                actions: <Widget>[
                  FlatButton(
                    onPressed: (){Navigator.pop(context);},
                    color: Colors.blue,
                    child: Text(
                      'OK',
                      style: TextStyle(
                        color: Colors.white,
                      ),
                    ),
                  )
                ],
              ));
      print(val);
    } on Exception catch (e) {
      print(e);
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: Container(
          color: Colors.white,
          constraints: BoxConstraints.expand(),
          child: Column(
            children: [
              Container(
                margin: EdgeInsets.only(bottom: 20),
                height: 320,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.only(
                    bottomRight: Radius.circular(50),
                    bottomLeft: Radius.circular(50),
                  ),
                  color: Colors.blue,
                  boxShadow: [
                    BoxShadow(
                      color: Colors.blue.withOpacity(0.7),
                      blurRadius: 15,
                    ),
                  ],
                ),
                alignment: Alignment.topCenter,
                child: Stack(
                  alignment: Alignment.bottomCenter,
                  children: <Widget>[
                      ClipRRect(
                        borderRadius: BorderRadius.only(
                          bottomLeft: Radius.circular(50),
                          bottomRight: Radius.circular(50),
                        ),
                        child: Image.network(
                          widget.details['image'],
                          width: double.infinity,
                          height: 300,
                          fit: BoxFit.cover,
                        ),
                    ),
                    Container(
                      decoration: BoxDecoration(
                        color: Colors.black.withAlpha(100),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      padding: EdgeInsets.all(10),
                      margin: EdgeInsets.only(bottom: 20),
                      child: Text(
                        "${widget.details['name']}, ${widget.details['location']}",
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              Spacer(),
              FlatButton(
                onPressed: scanCustomer,
                color: Colors.blue,
                child: Container(
                    margin: EdgeInsets.all(10),
                    child: Text(
                      "VERIFY CUSTOMER",
                      style: TextStyle(
                        fontSize: 20,
                        color: Colors.white,
                      ),
                    )),
              ),
              Spacer(),
              Image.network(
                'https://www.peekator.com/wp-content/uploads/2019/07/surveying_with_qr_code.png',
                height: 200,
                fit: BoxFit.cover,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
