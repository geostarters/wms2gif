var express = require('express');
var mailApp = require('../controllers/mail');

var router = express.Router();
var config = require('../config');
var GifGenerator = require('../controllers/gifGenerator')

router.get('/' + config.pathMainWeb + '/', async function(req, res, next) {

    if (req.query.bbox && req.query.email) {

        const output = await GifGenerator.run(req.query);
        res.json(output);

    }
    else {
        
        res.json({"ok": false, "msg": "Missing parameters"});

    }

});

module.exports = router;
