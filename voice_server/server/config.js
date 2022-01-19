const os = require('os');

module.exports = {
    domain : process.env.DOMAIN || 'localhost',
    mediasoup : {
        numWorkers : 1,
        workerSettings : {
            logLevel : 'warn',
            logTags : [
                'info'
            ],
            rtcMinPort : process.env.MEDIASOUP_MIN_PORT || 40000,
            rtcMaxPort : process.env.MEDIASOUP_MIN_PORT || 49999
        },

        routerOptions : {

            // For now, we only support voice
            mediaCodecs : [
                {
                    kind : 'audio',
                    mimeType : 'audio/opus',
                    clockRate : 48000,
                    channels: 2
                }
            ]
        },

        // TODO: add config for this
        // See https://mediasoup.org/documentation/v3/mediasoup/api/#WebRtcTransportOptions
        webRtcTransportOptions : {},

        // TODO: add config for this
        // See https://mediasoup.org/documentation/v3/mediasoup/api/#PlainTransportOptions
        plainTransportOptions: {}
    }
}