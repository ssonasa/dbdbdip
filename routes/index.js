var express = require('express');
var router = express.Router();
var mysql = require('mysql');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});
var tmp = '';
var chmod = 0;
//chmod = 1 : 밖 > 종류
//chmod = 2 : 밖 > 음식 
//chmod = 3 : 식당 선택

//mysql sever
var db = mysql.createConnection({
  host: 'choosethis.cemhkd80ccxj.us-east-2.rds.amazonaws.com',
  user: 'blcocas',
  password: '201221027',
  database: 'dbdbdeep'
});
//db connect
db.connect();


//초기 상태 get
router.get('/keyboard', function(req, res){

  const menu = {
      "type": 'buttons',
      "buttons": ["안에서 먹을래", "밖에서 먹을래"]
  };

  res.send(menu);
});


//message
router.post('/message', (req, res) => {
  const _obj = {
      user_key: req.body.user_key,
      type: req.body.type,
      content: req.body.content
  };
  //let message = undefined;
  //console.log(_obj.content);
  //console.log(typeof(_obj.content));

  //처음 메뉴
  if(_obj.content == '처음으로'){
    let message = {
      "keyboard": {
          "type": "buttons",
          "buttons": [
              "안에서 먹을래",
              "밖에서 먹을래"
          ]
      },
      "message" : {
        "text":'밖에서? 안에서?'
      }
    };
    res.send(message);
    tmp = '';
    chmod = 0;
  }
  //안에서 먹을래!
  else if(_obj.content ==  '안에서 먹을래'){
    console.log(_obj.content);
    let message = {
      "keyboard": {
          "type": "buttons",
          "buttons": [
              "학식",
              "기숙사식당-아침",
              "기숙사식당-점심",
              "기숙사식당-저녁",
              "교직원식당-점심",
              "교직원식당-저녁"
          ]
      },
      "message": {
        "text": '메뉴를 선택하세요.'
      }
    };
    res.send(message);  
  }

  //밖에서 먹을래!
  else if(_obj.content ==  '밖에서 먹을래'){
    console.log(_obj.content);
    let message = {
      "keyboard": {
          "type": "buttons",
          "buttons": [
              "종류로 검색",
              "음식으로 검색"
          ]
      },
      "message": {
        "text": '메뉴를 선택하세요.'
      }
    };
    res.send(message);  
  }
  
  //밖 > 종류
  else if(_obj.content ==  '종류로 검색'){
    console.log(_obj.content);
    let message = {
      "keyboard": {
          "type": "buttons",
          "buttons": [
              "한식",
              "일식",
              "중식",
              "양식",
              "술집",
              "기타"
          ]
      },
      "message": {
        "text": '메뉴를 선택하세요.'
      }
    };
    chmod = 1;
    res.send(message);  
  }

  //음식 종류 들어오고 종류선택
  else if(chmod == 1) {
    chmod = 0;
    console.log(_obj.content);
    let sql = 'select Rest_Name from FOOD_TYPE,RESTAURANT where Type_Num = T_Num and Type_Name = ?';
    
    db.query(sql,[_obj.content]  ,function (err, rows, fields) {
      for(var i = 0; i<rows.length;i++){
        console.log(rows[i].Rest_Name);
          if(rows.length-1 == i)
            tmp += rows[i].Rest_Name;
          else
            tmp += rows[i].Rest_Name + '\n';
      }
         
      let cb = function(){
        console.log(tmp);
        let message = {
          "keyboard": {
          "type": "text"    
          },
          "message": {
          "text": tmp + '\n식당이름을 입력해주세요.'
          }
        };
        chmod = 3;
        res.send(message);
      };
      cb();   
    });
  }

  //밖 > 음식
  else if(_obj.content ==  '음식으로 검색'){
    console.log(_obj.content);
    let message = {
      "keyboard": {
          "type": "text"    
      },
      "message": {
        "text": '원하시는 음식을 입력하세요.'
      }
    };
    chmod = 2;
    res.send(message);  
  }

  //음식 입력
  else if(chmod == 2){
    chmod = 0;
    console.log(_obj.content);
    console.log(chmod);
    let sql = 'select Rest_Name\
              from RESTAURANT\
              where Rest_Num in\
              (select R_Num\
              from COOKED_BY,FOOD\
              where F_Num=Food_Num and Food_Name = ?)';
    
    db.query(sql,[_obj.content]  ,function (err, rows, fields) {
      for(var i = 0; i<rows.length;i++){
        console.log(rows[i].Rest_Name);
          if(rows.length-1 == i)
            tmp += rows[i].Rest_Name;
          else
            tmp += rows[i].Rest_Name + '\n';
      }
         
      let cb = function(){
        console.log(tmp);
        if(tmp == ''){
          let message = {
            "keyboard": {
            "type": "text"    
            },
            "message": {
            "text": '해당 음식이 없습니다. 다시 입력해 주세요.\n처음으로 돌아가시려면 \'처음으로\'을 입력해주세요.'
            }
          };
          chmod = 2;
          res.send(message);  
        }
        else{
          let message = {
            "keyboard": {
            "type": "text"    
            },
            "message": {
            "text": tmp + '\n식당이름을 입력해주세요.'
            }
          };
          chmod = 3;
          res.send(message);
        }
      }; 
      cb();   
    });
  }

  //식당이름 들어오고 식당 입력
  else if(chmod == 3){
    console.log(chmod);
    chmod = 0;
    tmp = '';
    console.log(_obj.content);
    

    
    let foodsql = 'select Food_Name\
                  from FOOD\
                  WHERE Food_Num in\
                  (select F_Num\
                  from COOKED_BY, RESTAURANT\
                  where R_Num = Rest_Num and Rest_Name = ?)'; 
    let foodtmp = ''

    db.query(foodsql,[_obj.content]  ,function (err, rows, fields) {
      for(var i = 0; i<rows.length;i++){
        if(rows.length-1 == i)
            foodtmp += rows[i].Food_Name
          else
            foodtmp += rows[i].Food_Name + '\n';
      }
      console.log(foodtmp);
      let sql = 'select Rest_Name,Map, Average_Cost\
              from RESTAURANT\
              where Rest_Name = ?';
      db.query(sql,[_obj.content]  ,function (err, rows2, fields) {
        if(rows2[0] == undefined){
          let message = {
            "keyboard": {
            "type": "text"    
            },
            "message": {
            "text": '해당 음식점이 없습니다. 다시 입력해 주세요.\n처음으로 돌아가시려면 \'처음으로\'을 입력해주세요.'
            }
          };
          chmod = 3;
          res.send(message); 
        }
          
        else {
          console.log(rows2[0]);
          tmp += '식당이름 : ' + rows2[0].Rest_Name + '\n메뉴 : '+ foodtmp + '\n예상가격(1인당) : ' + rows2[0].Average_Cost;
          console.log(tmp); 
          let cb = function(){
            let message = {
              "keyboard": {
              "type": "buttons",
              "buttons":[
                "처음으로"
                ]    
              },
              "message": {
                "text": tmp,
                "message_button" : {
                  "label": "위치",
                  "url" : rows2[0].Map
                }
              } 
            };
            res.send(message);   
            
          };// let cb function() = ~
          cb();
        }
      });//db.query(sql)  

    });//db.query(foodsql)
  }//else if  
      

  //나머지
  else {
    console.log("나머지");
    let message = {
      "keyboard": {
          "type": "buttons",
          "buttons": [
              "처음으로",    
          ]
      },
      "message": {
        "text" : '처음으로 돌아갑니다.'
      } 
    };
    res.send(message);
  }

  

});
module.exports = router;
