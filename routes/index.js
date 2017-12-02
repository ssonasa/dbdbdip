var express = require('express');
var router = express.Router();
var mysql = require('mysql');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});
var tmp = '';

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
    
    res.send(message);  
  }

  //종류선택
  else if(_obj.content == '한식' || _obj.content == '일식' || _obj.content == '중식' || _obj.content == '양식' || _obj.content == '술집' || _obj.content == '기타') {
    console.log("여기1");
    console.log(_obj.content);
    let sql = 'select Rest_Name from FOOD_TYPE,RESTAURANT where Type_Num = T_Num and Type_Name = ?';
    
    db.query(sql,[_obj.content]  ,function (err, rows, fields) {
      for(var i = 0; i<rows.length;i++){
        console.log("1");
        console.log(rows[i].Rest_Name);
          if(rows.length-1 == i)
            tmp += rows[i].Rest_Name;
          else
            tmp += rows[i].Rest_Name + '\n';
      }
         
      let cb = function(){
        console.log("2");
        console.log(tmp);
        let message = {
          "keyboard": {
          "type": "text"    
          },
          "message": {
          "text": tmp
          }
        };
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
        "text": '안녕하세여'
      }
    };
    res.send(message);  
  }

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
