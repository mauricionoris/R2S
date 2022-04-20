const util = require('./util')  

const python = util.python
const assert = util.assert
const expect = util.expect
const Options = util.Options
const Options2 = util.Options2
const DictToParams = util.DictToParams
const host = util.host

describe('Structural tests', function() {


  
    //let args = ['/source/R2S/test/python/IntegrationTests.py']
    let args = ['/source/R2S/src/util/R2S.py']
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
  

    describe('Handling files and folders', function(){
     
      it("Should be able to create a new folder", async () => {
        Options2.function = "create_folder"
        ret = await python.run(args.concat(DictToParams(Options2)))
        assert.strictEqual(ret['r2sPid'], Options2.r2sPid)
        
      })
  
      it("Should be able to create a new folder - Remotelly", async () => {
        Options2.function = "create_folder"
        ret = await python.runRemote(host, args.concat(DictToParams(Options2)))
        assert.strictEqual(ret['r2sPid'], Options2.r2sPid)
        
      })
      
      it("Should be able to list all files of a specific extension", async () => {
        Options2.function = "read_folder"
        Options2.folder_path = "/source/R2S/data/R2SDatasets/test2"
        ret = await python.run(args.concat(DictToParams(Options2)))
        assert.deepStrictEqual(ret['files'], ['arq1.csv','arq2.csv'])
        
      })
      it("Should be able to list all files of a specific extension - Remotelly", async () => {
        Options2.function = "read_folder"
        Options2.folder_path = "/source/R2S/data/R2SDatasets/test2"
        ret = await python.runRemote(host,args.concat(DictToParams(Options2)))
        assert.deepStrictEqual(ret['files'], ['arq1.csv','arq2.csv'])
        
      })
  
      it("Should be able to get the size of a file", async () => {
        Options2.function = "file_size"
        Options2.file_path = "/source/R2S/data/R2SDatasets/test2/arq2.csv"
        ret = await python.run(args.concat(DictToParams(Options2)))
        expect(ret['file_size']).to.be.greaterThan(0)
      })
      it("Should be able to get the size of a file - Remotelly", async () => {
        Options2.function = "file_size"
        Options2.file_path = "/source/R2S/data/R2SDatasets/test2/arq2.csv"
        ret = await python.runRemote(host,args.concat(DictToParams(Options2)))
        expect(ret['file_size']).to.be.greaterThan(0)
      })
    })


    describe('Arrow Library Tests', function(){
      describe('Calling an Arrow Script', function() {
        this.timeout(60000)
        it('should be able to use Arrow on R2SData', async () => {
          Options.function = "ArrowTesting"  
          Options.ret = ""
          ret = await python.runRemote(host, args.concat(DictToParams(Options)),Options.r2sPid)
          assert.strictEqual(ret['tCompare'], true)
        })

    })

  })

})  