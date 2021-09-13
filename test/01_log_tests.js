const util = require('./util')  

const python = util.python
const logHandler = util.logHandler
const assert = util.assert
const expect = util.expect
const Options = util.Options
const Options2 = util.Options2
const DictToParams = util.DictToParams
const host = util.host
const uuidV4 = util.uuidV4
const args = util.args

describe('Log tests', function() {
  this.timeout(3000)
  describe('Viewing script log', function() {
      let logmessage = 'test'

      it('should be able to monitor the log of a specific r2sPid', async () => {
        Options.log = logmessage
        Options.function = ""
        ret = await python.run(args.concat(DictToParams(Options)))
        let logRead = await logHandler.readbyr2sPid(Options.logfile,Options.r2sPid)
        assert.deepStrictEqual([logmessage], logRead)
      })
      this.timeout(20000)
      it('should be able to monitor the log of a specific r2sPid -- Remotelly', async () => {
        Options.r2sPid = uuidV4()
        Options.log = logmessage
        Options.logfile =  "/source/R2S/log/R2SD.log"
        ret = await python.runRemote(host, args.concat(DictToParams(Options)),Options.r2sPid)
        let logRead = await logHandler.readbyr2sPid(Options.logfile,Options.r2sPid)
        assert.deepStrictEqual([logmessage], logRead)


      })
  });
});