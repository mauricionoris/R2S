const spawn      = require('child_process').spawn
const logOutput = (name) => (data) => console.log(`[${name}] ${data}`)


let runlocal = function(args) {

    return new Promise((resolve, reject) => {
            const process = spawn('python', args);
    
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
                    formatedOutput = JSON.parse(out)
                }
                resolve(Object.assign({},formatedOutput, {'exitCode':code}))
            });
        });
}

//TODO: runelsewhere --> allow to execution of python scripts outside the R2S Server


module.exports = {

    run:runlocal

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
