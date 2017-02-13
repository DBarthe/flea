'use strict';

/**
 * Base adapter
 */
class BaseAdapter {
    /**
     * @param {Connection} connection
     */
    constructor(connection) {
        this._connection = connection
    }

    execute(query, params = [], options = {}) {
        return this._connection.client.execute(query, params, options)
    }

    use(keyspace) {
        return this.execute("use ?", keyspace, { prepare: true })
    }
}

/**
 * Cassandra read adapter
 */
class ReadAdapter extends BaseAdapter {

    select(table, { columns = ['*'], where } = {}, params = [], options = { prepare: true }) {

        if (typeof columns == "string") {
            columns = [ columns ]
        }
        else if (columns.length == 0) {
            columns = ['*'];
        }

        let columnsPart = columns.join(','),
            wherePart = typeof where !== 'undefined' ? `WHERE ${ where }` : '',
            queryString = `SELECT ${ columnsPart } FROM ${ table } ${ wherePart }`;

        return this.execute(queryString, params, options);
    }
}

module.exports = {
    BaseAdapter: BaseAdapter,
    ReadAdapter: ReadAdapter,
}