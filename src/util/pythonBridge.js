const spawn      = require('child_process').spawn
const sck = require('./sockets.js');

const logOutput = (name) => (data) => console.log(`[${name}] ${data}`)


let runlocal = function(cmd, args) {


    return new Promise((resolve, reject) => {
            const process = spawn(cmd, args);
            //console.log(cmd, args)
            const out = []
            process.stdout.on('data', (data) => { out.push(data.toString()); } );
        
            const err = []
            process.stderr.on('data', (data) => { err.push(data.toString());
                logOutput('stderr')(data);
                }
            );
    
            process.on('exit', (code, signal) => {
                //logOutput('exit')(`${code} (${signal})`)

                let formatedOutput = {};
                process.exitCode = code;
                
                if (code === 0) {
                    try {
                        formatedOutput = JSON.parse(out)
                    } catch (e) {
                        //console.log(e)
                        formatedOutput = JSON.parse(out.slice(0,-1))
                    }
                }
                resolve(Object.assign({},formatedOutput, {'exitCode':code}))
            });
        });
}

let runRemote = function(host, args) {
    return sck.run(host,args)
}


module.exports = {

    run: function(args) {return runlocal('python',args)},
    runRemote: function(host,args,id) {return runRemote(host,args,id)}

}


/* function promisedParseJSON(json) {
  return new Promise((resolve, reject) => {
      try {
          resolve(JSON.parse(json))
      } catch (e) {
          console.log(e)
          reject(e)
      }
  })
} */
