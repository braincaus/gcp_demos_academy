const uuid = require('uuid');

// Return a newly generated UUID in the HTTP response.
exports.getUuid = (req, res) => {
  res.send(uuid.v4());
};