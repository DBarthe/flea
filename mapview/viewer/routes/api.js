const express = require('express')
const config = require('../config.js')

const router = express.Router()

// pagination middleware for GET endpoints
router.get('*', (req, res, next) => {
    let { pageToken = undefined
        , maxResults = config.api.defaultFetchSize } = req.query
    req.pagination = { pageToken, maxResults }
    console.log(`pagination ${req.pagination}`)
    next()
})

router.get('/students', (req, res) => {
    console.log("main handler")
    req.cassandra.adapter.select('student', {}, [], {
        prepare: true,
        fetchSize: req.pagination.maxResults,
        pageState: req.pagination.pageToken,
    }).then(result => {
        res.json({
            nextPageToken: result.pageState,
            students: result.rows,
        })
    }).catch(err => {
        res.json({error: err})
    })
})

module.exports = router