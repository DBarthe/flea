'use strict';

const Hapi = require('hapi')
const Joi = require('joi')
const cassandra = require('cassandra-driver')

const CASSANDRA_ENDPOINT = "dbarth.eu"

const server = new Hapi.Server()
server.connection({ port: 3000, host: 'localhost' })

const client = new cassandra.Client({contactPoints: [CASSANDRA_ENDPOINT], keyspace: 'mapview'})
const reportInsert = "INSERT INTO report (user, ts, hostname) VALUES ( ?, dateOf(now()), ?) ;"
const stationInsert = "INSERT INTO station (hostname, user) VALUES (?, ?)"

function collect(user, hostname, callback){
  const reportParams = [ user, hostname ]
  const stationParams = [ hostname, user ]
  return Promise.all([
    client.execute(reportInsert, reportParams, { prepared: true }),
    client.execute(stationInsert, stationParams, { prepared: true })
  ])
}

server.route({
  method: 'POST',
  path: '/collect',
  handler: function (request, reply) {
    var { hostname, user } = request.payload
    collect(user, hostname).then(result => reply({
      error: false,
      message: "thanks"
    }))
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
