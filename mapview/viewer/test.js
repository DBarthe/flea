'use strict';

const cassandra = require('./cassandra');
const config = require('./config');

let co = new cassandra.Connection().configure({
    keyspace: config.cassandra.keyspace,
    endpoint: config.cassandra.endpoint,
    user: config.cassandra.user,
    password: config.cassandra.password,
});

let adapter = new cassandra.adapter.ReadAdapter(co);

// adapter.select("station")
//     .then(res => console.log(res))
//     .catch(err => console.log(err))

adapter.select("station", { columns: ['building', 'hostname'], where: "building = ?" }, [ 1 ])
    .then(res => console.log(res))
    .catch(err => console.log(err))

