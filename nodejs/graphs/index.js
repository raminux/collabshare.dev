var express = require('express');
var app = express();
var neo4j =  require('neo4j-driver')

neo4j_service = process.env.NEO4J_SERVICE || 'localhost';
neo4j_port = process.env.NEO4J_PORT || 7687
neo4j_user = process.env.NEO4J_USER || 'neo4j';
neo4j_password = process.env.NEO4J_PASSWORD || 'password';
let driver;



// var amqp = require('amqplib/callback_api');


// rabbit_srv = process.env.RABBIT_SERVICE;
// amqp.connect(`amqp://admin:pass@${rabbit_srv}`, function(error0, connection) {
//     if (error0) {
//         throw error0;
//     }
//     connection.createChannel(function(error1, channel) {
//         if (error1) {
//             throw error1;
//         }
//         var queue = 'TEST_EVENT';
//         channel.assertQueue(queue, {durable: false});
//         console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);
//         channel.consume(queue, function(msg) {
//             console.log(" [x] Received %s", msg.content.toString());
//         }, {noAck: true});
//     });  

// });


app.get('/', async (req, res) => {

    driver = neo4j.driver(
        `neo4j://${neo4j_service}:${neo4j_port}`, 
        neo4j.auth.basic(neo4j_user, neo4j_password), 
        {
            maxConnectionPoolSize: 100,
            connectionTimeout: 30000, // 30 seconds
            logging: {
              level: 'info',
              logger: (level, message) => console.log(level + ' ' + message)
            },
          })
    
    await driver.verifyConnectivity()
    const session = driver.session();
    const result = await session.executeWrite(
        tx => tx.run(
            `
            CREATE (c:Collaborator {
              collaboratorId: randomUuid(),
              email: $email,
              password: $pass,
              name: $name
            })
            RETURN c
          `,
          { email:'test@collabshare.dev', pass: 'testPass', name: 'Anyone' }
        )
    )
    const [ first ] = result.records
    const node = first.get('c')
    console.log(node.properties)
    
    await session.close()

    res.status(200).send(`Collaborators Relationships on Port: ${process.env.PORT}`);
});

app.listen(3000, () => {
    console.log(" [*] Listening on Port: 3000. ");
});
