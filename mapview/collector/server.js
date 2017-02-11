'use strict';

const Hapi = require('hapi')
const Joi = require('joi')
const cassandra = require('cassandra-driver')
const assert = require('assert')
const config = require('./config')

const server = new Hapi.Server()
server.connection({ port: config.LISTEN_PORT, host: config.LISTEN_ADDRESS })

const authProvider = new cassandra.auth.PlainTextAuthProvider(config.CASSANDRA_USER, config.CASSANDRA_PASSWORD);
const client = new cassandra.Client({
  authProvider: authProvider,
  contactPoints: [config.CASSANDRA_ENDPOINT],
  keyspace: 'fil',
})

client.connect(function (err){
  assert.ifError(err)
})

const reportByHostnameInsert = "INSERT INTO report (hostname, login, ts) VALUES ( ?, ?, dateOf(now())) ;"
const reportByLoginInsert = "INSERT INTO report (login, hostname, ts) VALUES ( ?, ?, dateOf(now())) ;"
const stationInsert = "INSERT INTO station (building, hostname, user, ts) VALUES ('M5', ?, dateOf(now()))"
const studentInsert = "UPDATE student SET hostname=?, hostname_ts=dateOf(now()) WHERE login=?;"

function collect(user, hostname, callback){

  if (user == 'empty'){
    user = null;
  }

  const reportByHostnameParams = [ hostname, user ]
  const reportByLoginParams = [ user, hostname ]
  const stationParams = [ hostname, user ]
  const studentParams = [ hostname, user ]

  var queries = [
    client.execute(reportByHostnameInsert, reportByHostnameParams, { prepared: true }),
    client.execute(stationInsert, stationParams, { prepared: true })
  ];

  if (!user) {
    queries.push(client.execute(reportByLoginInsert, reportByHostnameParams, { prepared: true }));
    queries.push(client.execute(studentInsert, studentParams, { prepared: true }));
  }

  return Promise.all(queries);
}

server.route({
  method: 'POST',
  path: '/collect',
  handler: function (request, reply) {
    var { hostname, user } = request.payload
    collect(user, hostname)
      .then(result => reply({
        error: false,
        message: "thanks"
      }))
      .catch(err => {
        reply({
          error: true,
          message: "sorry"
        })
        console.error(err)
      })
  },
  config: {
    validate: {
      payload:  {
        user: Joi.string().required(),
        hostname: Joi.string().required()
      }
    }
  }
})

server.start((err) => {
  if (err) {
      throw err;
  }
  console.log(`Server running at: ${server.info.uri}`)
});
