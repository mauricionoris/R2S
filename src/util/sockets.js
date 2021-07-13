const zmq = require("zeromq");
const { StringDecoder } = require('string_decoder');
const decoder = new StringDecoder('utf8');

async function runbysockets(host, msg, id) {

  const req = new zmq.Request()
  let received = {'r2sPid':0}
  req.connect(host)

  const send = async () => {
    //console.log(msg)
    await req.send(msg.join(','))
    while(true) {
      const [res] =  await req.receive()
      received = JSON.parse(decoder.write(res))
      if (id === received['r2sPid']) {
        return JSON.parse(received)
      }
    } 
  }
  return await send()
}
    

module.exports = {

  run: function(host, msg, id) { return runbysockets(host,msg, id)}

}