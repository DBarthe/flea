'use strict';

const Connection = require('./connection.js');
const adapter = require('./adapter.js');

module.exports = {
    driver: require('cassandra-driver'),
    Connection: Connection,
    adapter: adapter,
};
