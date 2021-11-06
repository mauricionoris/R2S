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

let _args = ['/source/R2S/src/util/R2S.py']
  
isObject = function(a) {
  return (!!a) && (a.constructor === Object);
}

isArray = function(a) {
  return (!!a) && (a.constructor === Array);
};

function _DictToParams(opt, keyflag="--") {

    let params = [];


    for (let [k,v] of Object.entries(opt)) {
      
      if (isObject(v)) {
         k = k + '_obj'
         v = JSON.stringify(v).replace(/,/g, '&');
        
      }

      params.push(keyflag + k + "=" + v + "") 
   
 
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



  









