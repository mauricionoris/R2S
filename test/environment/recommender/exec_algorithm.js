
const assert = require('assert');
const spawn = require('child_process').spawn
const uuidV4 = require("uuid/v4")

const logOutput = (name) => (data) => console.log(`[${name}] ${data}`)


describe('environment/recommender tests', function() {

  describe('Executing a python Script', function() {

    describe('Calling the script', function() {
      let uniqueId = uuidV4()
      let args = [
        '/source/R2S/src/environment/recommender/main.py',
        '-pic', uniqueId
      ]
      
      it('should call a python script and return the PIC', async () => {
          try {
            
            promisedParseJSON(await runpython(args)).then((ret) =>{
              assert.strictEqual(ret['pic'], uniqueId)
              //process.exit(0)
              
            })
            
            
          } catch (e) {
            console.error('Error during script execution ', e.stack);
            process.exit(1);
          }
        })
      })
   

    describe('Viewing script log', function() {
      it('should be able to monitor the log of a specific process')

    });

    describe('Checking the script output', function() {
      it('should be able to see the status of the script 1-success; 0-fail')

      
    });

  });
});


function runpython(args) {
  return new Promise((resolve, reject) => {
    const process = spawn('python', args);

    const out = []
    process.stdout.on('data', (data) => { out.push(data.toString()); } );


    const err = []
    process.stderr.on(
      'data',
      (data) => {
        err.push(data.toString());
        logOutput('stderr')(data);
      }
    );

    process.on('exit', (code, signal) => {
      logOutput('exit')(`${code} (${signal})`)
      if (code === 0) {
        resolve(out);
      } else {
        reject(new Error(err.join('\n')))
      }
    });
  });
}


function promisedParseJSON(json) {
  return new Promise((resolve, reject) => {
      try {
          resolve(JSON.parse(json))
      } catch (e) {
          reject(e)
      }
  })
}
