let cmd = require("node-cmd");
exports.commandrun = function(req, res) {
  console.log("command req", req.body.command);
  cmd.run(req.body.command, function(err, data, stderr) {
    console.log(data);
    res.send({
      code: 200,
      result: data,
    });
  });
};
