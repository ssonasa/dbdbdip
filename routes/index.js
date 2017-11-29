var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/keyboard', function(req, res){
  const menu = {
  	"message": {
  		"text": [
  		'밥은 어디서 먹을래??',
  		'"학식" 이나 "외식" 이라 쓰시오',
  		]
  	},
  	"keyboard": {
    "type": 'buttons',
    "buttons": [
    	"학식",
    	"외식",
    	]
  }
  };

  res.set({
    'content-type': 'application/json'
  }).send(JSON.stringify(menu));
});



app.post('/message',function (req, res) {

    const _obj = {
        user_key: req.body.user_key,
        type: req.body.type,
        content: req.body.content
    };

    console.log(_obj.content)

    if(_obj.content == '학식')
    {

    }


    else if(_obj.content == '외식')
    {

      const massage = {
          "message": {
              "text": '뭐 먹을래?'
          },
          "keyboard": {
              "type": "buttons",
              "buttons": [
                  "한식",
                  "중식",
                  "일식",
                  "양식"
              ]
          }
      };
      res.set({
          'content-type': 'application/json'
      }).send(JSON.stringify(massage));
    }



    else {
        const massage = {
            "message": {
                "text": '못 알아 먹었다...'
            }
        }
    };
	res.set({
          'content-type': 'application/json'
      }).send(JSON.stringify(massage));
    };

module.exports = router;
