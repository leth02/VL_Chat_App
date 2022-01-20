const https = require('https');
const fs = require('fs');

const options = {
    key: "pass the key.pem here",
    cert: "pass the cert.pem here"
};

// Create a HTTPS server that listen to voice calling request
let httpsServer = https.createServer(options, (req, res) => {
    res.writeHead(200);
    res.end('hello world\n');
}).listen(8000);
