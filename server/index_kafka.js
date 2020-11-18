'use strict';

const Hapi = require('@hapi/hapi');
const { Kafka } = require('kafkajs')


const init = async () => {

    const server = Hapi.server({
        port: 3000,
        host: 'localhost'
    });

    server.route({
        method: 'GET',
        path: '/',
        handler: async (request, h) => {

            const kafka = new Kafka({
                clientId: 'cc_server',

                // See kafka quickstart guide for how to quickly get a local thingy running
                brokers: ['localhost:9092']
            })

            const producer = kafka.producer()

            await producer.connect()
            await producer.send({
                topic: 'web-requests',
                messages: [
                    { value: 'fuck yeah!' },
                ],
            })
            console.log("Sent a message?")

            await producer.disconnect()

            return 'Hello World!';
        }
    });

    await server.start();
    console.log('Server running on %s', server.info.uri);
};

process.on('unhandledRejection', (err) => {

    console.log(err);
    process.exit(1);
});

init();
