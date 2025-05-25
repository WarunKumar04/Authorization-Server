const fastify = require('fastify')({ logger: true });
const path = require('path');
const { exec } = require('child_process');

// Serve the registration page
fastify.register(require('@fastify/static'), {
    root: path.join(__dirname),
    index: 'index.html'
});

// Handle registration
fastify.post('/register', (req, reply) => {
    exec('start cmd /k python create_user.py', (error) => {
        if (error) {
            console.error(error);
            return reply.status(500).send({ error: "Failed to start registration" });
        }
        reply.send({ message: "Check your command prompt for registration" });
    });
});

// Start server with correct listen options
fastify.listen({
    port: 3000,
    host: '0.0.0.0'
}, (err) => {
    if (err) {
        fastify.log.error(err);
        process.exit(1);
    }
    console.log(`Registration server running on http://localhost:3000`);
});