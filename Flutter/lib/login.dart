import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:grocerstop/home_screen.dart';
import 'package:http/http.dart' as http;
import 'package:qrscan/qrscan.dart' as scanner;

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  var requestSent = false;
  final shopIDController = TextEditingController();

  final passwordController = TextEditingController();

  void sendData(shopId, pw, context) async {
    print("sent");
    const url = "http://fd7ea7a0d93c.ngrok.io/flutterShopVerify";
    try {
      setState(() {
        requestSent = true;
      });
      final response = await http.post(
        url,
        body: json.encode(
          {
            'shop_id': shopId,
            'password': pw,
          },
        ),
      );
      print(response.body);
      setState(() {
        requestSent = false;
      });

      final res = json.decode(response.body);
      if (res['status']==true){
        var details = {
          'shop_id' : shopId,
          'image' : res['details']['image'],
          'name' : res['details']['name'],
          'location' : res['details']['location'],
        };
        FocusScope.of(context).requestFocus(FocusNode());
        Navigator.pushReplacement(context, MaterialPageRoute( builder: (_)=> HomeScreen(details)));
      }else{
        print('status false');
      }
    } on Exception catch (e) {
      setState(() {
        requestSent=false;
      });
      print(e);
    }

  }

  @override
  Widget build(BuildContext context) {
    final mediaQuery = MediaQuery.of(context);
    return SafeArea(
      child: Scaffold(
        resizeToAvoidBottomPadding: false,
        body: GestureDetector(
          onTap: (){
            FocusScope.of(context).requestFocus(FocusNode());
          },
          child: Stack(
            alignment: Alignment.center,
            children: <Widget>[
              Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                ),
                constraints: BoxConstraints.expand(),
                child: Column(
                  children: <Widget>[
                    Image.network("https://tevera.com/wp-content/uploads/2019/12/login.png", fit: BoxFit.cover, ),
                    Spacer(),
                    Image.network("https://img.deszone.net/2019/12/online-shopping-vector-illustration1.jpg", fit: BoxFit.cover,),

                  ],
                ),
              ),
              Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(10),
                  color: Colors.white,
                  border: Border.all(color: Colors.blue, width: 1,),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.blue.withOpacity(0.5),
                      blurRadius: 5,
                    ),]
                ),
                child: Container(
                  margin: EdgeInsets.symmetric(horizontal: 30, vertical: 20),
                  width: mediaQuery.size.width * 0.6,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: <Widget>[
                      TextField(
                        decoration: InputDecoration(
                            hintText: "Shop ID"
                        ),
                        controller: shopIDController,
                      ),
                      SizedBox(height: 20,),
                      TextField(
                        decoration: InputDecoration(
                            hintText: "Password"
                        ),
                        controller: passwordController,
                      ),
                      SizedBox(
                        height: 20,
                      ),
                      !requestSent?FlatButton(
                        onPressed: (){
                          sendData(shopIDController.text, passwordController.text, context);
                        },
                        color: Colors.blue,
                        child: Text("Submit", style: TextStyle(
                          color: Colors.white,
                        ),),
                      ):
                          Container(
                            height: 20,
                            width: 20,
                            child: CircularProgressIndicator(),
                          )
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
