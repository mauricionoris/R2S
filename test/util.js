process.chdir('/')

const R2SPath = '../'
const _host = "tcp://10.0.0.11:5555"

const _logHandler = require(R2SPath + '/src/util/logHandler.js');
const _python     = require(R2SPath + '/src/util/pythonBridge.js');

const _assert     = require('assert');
const _expect     = require('chai').expect;

const _uuidV4     = require("uuid/v4");

let _Options = {
  "r2sPid": _uuidV4(),
  "ret": 0,
  "log": "",
  "logfile": "/source/R2S/log/R2SS.log",
  "function": ""
}


let _Options2 = {
  "r2sPid": _uuidV4(),
  "ret": 0,
  "folder_path": "/source/R2S/data/R2SDatasets/test",
  "file_path": "",
  "extension":"csv",
  "function": "",
  "log": ""
}

let _args = ['/source/R2S/test/python/IntegrationTests.py']
  

function _DictToParams(opt) {

    let params = [];

    for (const [k,v] of Object.entries(opt)) {
       params.push("--" + k + "=" + v + "") 

    } 

    return params;


}

module.exports = {
  args: _args,
  assert: _assert,
  expect: _expect,
  python: _python, 
  logHandler: _logHandler,
  DictToParams: _DictToParams,
  host: _host,
  Options: _Options,
  Options2: _Options2,
  uuidV4: _uuidV4

}



  









