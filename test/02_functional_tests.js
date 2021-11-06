const util = require('./util')  


const fs = require('fs')



const python = util.python
const assert = util.assert
const expect = util.expect
const Options = util.Options
const Options2 = util.Options2
const DictToParams = util.DictToParams
const host = util.host
const uuidV4 = util.uuidV4


describe('functional tests', function() {

    let args = ['/source/R2S/src/util/R2S.py']
  
    let OptionsSetup = {
      "r2sPid": uuidV4(),
      "ret": 0,
      "log": "",
      "logfile": "",
      "function": "import_dataset",
      "extension": "csv",
      "folderIn": "/source/datasets/movielens/ml-25m",
      "folderOut":"/source/R2S/data/R2SDatasets/movielens"
    }
  
    let OptionsAlgo = {
      "r2sPid": uuidV4(),
      "ret": 0,
      "log": "",
      "logfile": "",
      "function": "recommend",
      "environment": {'dataset':{'name':'MovieLens', 'path':'/source/R2S/data/R2SDatasets/movielens'},
                      'data':{'ratings':null, 'movies': null},
                      'matrix':{'source':'ratings', 'row':'userId', 'col':'movieId', 'data':'rating'},
                      'algo':{'Random':'basic','PopScore': 'basic'},
                      'algodata':{'Random':{'items':{'dataset':'movies', 'feature':'movieId'}}
                              ,'PopScore':{'scores':{'dataset':'ratings','feature':'movieId'}}}
                      },
        "action": {'algo':'Random'},
        'parameters': {'users': [25,26,27,28,29,30], 'n': 3, 'score_method': 'count'}
      }




    let OptionsPickle = {
          "r2sPid": uuidV4(),
          "ret": 0,
          "log": "",
          "logfile": "",
          //"file_path": "/source/R2S/cache/d028d53bbde0d3cc5e2886e03ea2a6212e67a011.pickle",
          //"file_path": "/source/R2S/cache/fe34f3ef0f1d85fd59fc4cade5cc5bf25160edbb.pickle",
          "file_path": "/source/R2S/cache/6f1fc7c5411e80ba8ceef839f70b41487a7d1efa.pickle",
          "function": "read_pickle",
    }


    describe('Setup of a new domain', function() {
      this.timeout(40000)
      describe('Importing a dataset', function() {
        it('should be able to convert a dataset to parquet and import it into R2S datasets', async () => {
          ret = await python.runRemote(host,args.concat(DictToParams(OptionsSetup)))
          assert.strictEqual(ret['r2sPid'], OptionsSetup.r2sPid)
        
        })
      })
      describe('Algorithm execution', function() {
        it('should be able execute the Random algorithm and cache the results', async () => {
          
          ret = await python.runRemote(host, args.concat(DictToParams(OptionsAlgo)))
            //console.log(ret['metadata']['cache'])
          assert.strictEqual(ret['metadata']['cache'], OptionsPickle.file_path )
    
        })

        it("Should be able to read pickle file and list it's dictionary", async () => {
          ret = await python.run(args.concat(DictToParams(OptionsPickle)))
          //console.log(ret)
          assert.strictEqual(ret['data']['25'][0], 139911)
          
        })
      })
  
  
    })  
  
  
    
  })