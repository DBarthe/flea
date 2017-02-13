'use strict';

const cassandra = require('cassandra-driver');

class Connection {
    constructor() {
        this._client = null;
        this._authProvider = null;
    }

    configure({ endpoint, keyspace, user, password }) {
        this._endpoint = endpoint;
        this._keyspace = keyspace;
        this._authProvider = new cassandra.auth.PlainTextAuthProvider(user, password);
        this._client = new cassandra.Client({
            authProvider: this._authProvider,
            contactPoints: [this._endpoint],
            keyspace: this._keyspace
        });
        return this
    }

    connect() {
        return this._client.connect();
    }

    get client() {
        return this._client;
    }
}

module.exports = Connection;
