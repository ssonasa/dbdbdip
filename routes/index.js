var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/keyboard', function(req, res){
  const menu = {
    "type": 'buttons',
    "buttons": ["안녕", "메롱"]
  };

  res.set({
    'content-type': 'application/json'
  }).send(JSON.stringify(menu));
});

zzzzzzz
module.exports = router;
