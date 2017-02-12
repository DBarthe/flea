const express = require('express');
const router = express.Router();

/* GET home page. */
router.get('/', (req, res) => {
    res.render('index', { title: 'Express' });
});

router.get('/students', (req, res) => {
    req.cassandra.manager._client.execute("select * from student", { prepare: true })
        .then(result => {
            res.json(result.rows)
        })
        .catch(err => {
            res.json({error: err})
        })
})

module.exports = router;
