process.chdir('/')

const R2SPath = '../../..'
const host = "tcp://10.0.0.11:5555"

const logHandler = require(R2SPath + '/src/util/logHandler.js');
const python     = require(R2SPath + '/src/util/pythonBridge.js');

const assert     = require('assert');
const expect     = require('chai').expect;

const uuidV4     = require("uuid/v4");

let Options = {
  "r2sPid": uuidV4(),
  "ret": 0,
  "log": "",
  "logfile": "/source/R2S/log/R2SS.log",
  "function": ""
}

let Options2 = {
  "r2sPid": uuidV4(),
  "ret": 0,
  "folder_path": "/source/R2S/data/R2SDatasets/test",
  "file_path": "",
  "extension":"csv",
  "function": "",
  "log": ""
}

function DictToParams(opt) {

    let params = [];

    for (const [k,v] of Object.entries(opt)) {
       params.push("--" + k + "=" + v + "") 

    } 

    return params;


}


describe('structural tests', function() {
  let args = ['/source/R2S/test/python/IntegrationTests.py']

  describe('Executing a python Script', function() {

    describe('Calling the script', function() {
      it('should call a python script and return the r2sPid', async () => {
        ret = await python.run(args.concat(DictToParams(Options)))
        assert.strictEqual(ret['r2sPid'], Options.r2sPid)
      
      })
    })

    describe('Calling the script remotelly', function() {
      this.timeout(6000)
       it('should call a python script and return the r2sPid', async () => {
        ret = await python.runRemote(host, args.concat(DictToParams(Options)),Options.r2sPid)
        assert.strictEqual(ret['r2sPid'], Options.r2sPid)
      }) 
    })


  })  

  describe('Checking the script output', function() {
    it('should be able to see the status of the script 1-fail', async () => {
        Options.ret = 1
        ret = await python.run(args.concat(DictToParams(Options)))
       
        assert.strictEqual(ret['exitCode'], Options.ret)
    })

    it('should be able to see the status of the script 0-success', async () => {
      Options.ret = 0
      ret = await python.run(args.concat(DictToParams(Options)))
      assert.strictEqual(ret['exitCode'], Options.ret)
    })
  
    it('should be able to see the status of the script 1-fail - Remotelly', async () => {
      Options.ret = 1
      ret = await python.runRemote(host, args.concat(DictToParams(Options)), Options.r2sPid)
      assert.strictEqual(ret['exitCode'], Options.ret)
    })

    it('should be able to see the status of the script 0-success  - Remotelly ', async () => {
      Options.ret = 0
      ret = await python.runRemote(host, args.concat(DictToParams(Options)), Options.r2sPid)
      assert.strictEqual(ret['exitCode'], Options.ret)
    })
  });

  describe('Viewing script log', function() {
      let logmessage = 'test'

      it('should be able to monitor the log of a specific r2sPid', async () => {
        Options.log = logmessage
        ret = await python.run(args.concat(DictToParams(Options)))
        let logRead = await logHandler.readbyr2sPid(Options.logfile,Options.r2sPid)
        assert.deepStrictEqual([logmessage], logRead)
      })

      it('should be able to monitor the log of a specific r2sPid -- Remotelly', async () => {
        Options.r2sPid = uuidV4()
        Options.log = logmessage
        Options.logfile =  "/source/R2S/log/R2SD.log"
        ret = await python.runRemote(host, args.concat(DictToParams(Options)),Options.r2sPid)
        let logRead = await logHandler.readbyr2sPid(Options.logfile,Options.r2sPid)
        assert.deepStrictEqual([logmessage], logRead)


      })
  });

  describe('Handling files and folders', function(){
    //let args2 = ['/source/R2S/src/util/fileHandler.py']
    let args2 = ['/source/R2S/test/python/IntegrationTests.py']
    it("Should be able to create a new folder", async () => {
      Options2.function = "create_folder"
      ret = await python.run(args2.concat(DictToParams(Options2)))
      assert.strictEqual(ret['r2sPid'], Options2.r2sPid)
      
    })

    it("Should be able to create a new folder - Remotelly", async () => {
      Options2.function = "create_folder"
      ret = await python.runRemote(host, args2.concat(DictToParams(Options2)))
      assert.strictEqual(ret['r2sPid'], Options2.r2sPid)
      
    })
    
    it("Should be able to list all files of a specific extension", async () => {
      Options2.function = "read_folder"
      Options2.folder_path = "/source/R2S/data/R2SDatasets/test2"
      ret = await python.run(args2.concat(DictToParams(Options2)))
      assert.deepStrictEqual(ret['files'], ['arq1.csv','arq2.csv'])
      
    })
    it("Should be able to list all files of a specific extension - Remotelly", async () => {
      Options2.function = "read_folder"
      Options2.folder_path = "/source/R2S/data/R2SDatasets/test2"
      ret = await python.runRemote(host,args2.concat(DictToParams(Options2)))
      assert.deepStrictEqual(ret['files'], ['arq1.csv','arq2.csv'])
      
    })

    it("Should be able to get the size of a file", async () => {
      Options2.function = "file_size"
      Options2.file_path = "/source/R2S/data/R2SDatasets/test2/arq2.csv"
      ret = await python.run(args2.concat(DictToParams(Options2)))
      expect(ret['file_size']).to.be.greaterThan(0)
    })
    it("Should be able to get the size of a file - Remotelly", async () => {
      Options2.function = "file_size"
      Options2.file_path = "/source/R2S/data/R2SDatasets/test2/arq2.csv"
      ret = await python.runRemote(host,args2.concat(DictToParams(Options2)))
      expect(ret['file_size']).to.be.greaterThan(0)
    })
  })
  describe('Calling an Arrow Script', function() {
      this.timeout(5000)
      it('should be able to use Arrow on R2SData', async () => {
        Options.function = "ArrowTesting"  
        Options.ret = ""
        ret = await python.runRemote(host, args.concat(DictToParams(Options)),Options.r2sPid)
        assert.strictEqual(ret['tCompare'], true)
      })
    

  })




});



describe('functional tests', function() {

  let args = ['/source/R2S/src/util/R2S.py']

  let OptionsFunctional = {
    "r2sPid": uuidV4(),
    "ret": 0,
    "log": "",
    "logfile": "",
    "function": "import_dataset",
    "extension": "csv",
    "folderIn": "/source/datasets/movielens/ml-25m",
    "folderOut":"/source/R2S/data/R2SDatasets/movielens"
  }

  describe('Setup of a new domain', function() {
    this.timeout(10000)
    describe('Importing a dataset', function() {
      it('should be able to convert a dataset to parquet and import it into R2S datasets', async () => {
        ret = await python.runRemote(host,args.concat(DictToParams(OptionsFunctional)))
        assert.strictEqual(ret['r2sPid'], OptionsFunctional.r2sPid)
      
      })
    })



  })  


  
})
