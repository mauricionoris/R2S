process.chdir('/')

const R2SPath = '../../..'

const logHandler = require(R2SPath + '/src/util/logHandler.js');
const python     = require(R2SPath + '/src/util/pythonBridge.js');

const assert     = require('assert');
const uuidV4     = require("uuid/v4");


describe('environment/recommender tests', function() {

  describe('Executing a python Script', function() {
    let r2sPid = uuidV4()
    let args = ['./source/R2S/test/python/IntegrationTests.py', r2sPid, null, null]

    describe('Calling the script', function() {
      it('should call a python script and return the r2sPid', async () => {
        args[2] = 0
        ret = await python.run(args)
        assert.strictEqual(ret['r2sPid'], r2sPid)
      
      })
    })

    describe('Checking the script output', function() {
      it('should be able to see the status of the script 1-fail', async () => {
        args[2] = 1
        ret = await python.run(args)
       
        assert.strictEqual(ret['exitCode'], 1)
      })

      it('should be able to see the status of the script 0-success', async () => {
        args[0] = './source/R2S/test/python/IntegrationTests.py'
        args[2] = 0
        ret = await python.run(args)
        assert.strictEqual(ret['exitCode'], 0)
      })
    });

    describe('Viewing script log', function() {

      let logmessage = ["BEGIN","DOING STAFF","END"]

      it('should be able to monitor the log of a specific r2sPid', async () => {
        args[0] = './source/R2S/test/python/IntegrationTests.py'
        args[3] = logmessage.join()
        ret = await python.run(args)
        let logRead = await logHandler.readbyr2sPid(r2sPid)
        assert.deepStrictEqual(logmessage, logRead)
      })
    });
  });
});








