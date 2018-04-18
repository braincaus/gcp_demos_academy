/**
 * Background Cloud Function that returns a Promise. Note that we don't pass
 * a "callback" argument to the function.
 *
 * @param {object} event The Cloud Functions event.
 * @param {object} event.data The event data.
 * @returns {Promise}
 */
exports.helloPromise = (event) => {
    const request = require('request-promise');
  
    return request({
      uri: event.data.endpoint
    });
  };