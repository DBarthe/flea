'use strict';

const Manager = require('./manager.js');

module.exports = {
    driver: require('cassandra-driver'),
    Manager: Manager,
};
