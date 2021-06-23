process.chdir('/')

const assert = require('assert');
const spawn = require('child_process').spawn
const uuidV4 = require("uuid/v4")

let pythonReturn = null

const logOutput = (name) => (data) => console.log(`[${name}] ${data}`)

describe('environment/recommender tests', function() {

  describe('Executing a python Script', function() {
    let r2sPid = uuidV4()
    let args = ['./source/R2S/test/python/IntegrationTests.py', r2sPid, null]

    describe('Calling the script', function() {
      it('should call a python script and return the r2sPid', async () => {
        args[2] = 0
        ret = await runpython(args)
        process.exitCode = 0;
        assert.strictEqual(ret['r2sPid'], r2sPid)
      
      })
    })

    describe('Checking the script output', function() {
      it('should be able to see the status of the script 1-fail', async () => {
        args[2] = 1
        ret = await runpython(args)
        assert.strictEqual(pythonReturn, 1)
      })

      it('should be able to see the status of the script 0-success', async () => {
        args[0] = './source/R2S/test/python/IntegrationTests.py'
        args[2] = 0
        ret = await runpython(args)
        assert.strictEqual(pythonReturn, 0)
      })
    });

    describe('Viewing script log', function() {

      it('should be able to monitor the log of a specific r2sPid')

    });



  });
});


function runpython(args) {
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
      process.exitCode = code
      pythonReturn = code
      if (code === 0) {
        resolve(JSON.parse(out))
      } else {
        resolve(null)
        //reject(new Error(err.join('\n')))
      }
    });
  });
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