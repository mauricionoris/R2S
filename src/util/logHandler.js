const fs         = require('fs');
const readline   = require('readline');
const logfile = './source/R2S/log/R2S.log'


let logreader = function readLog(r2sPid){
        return new Promise((resolve, reject) => {
        let logLines = []
        let rl = readline.createInterface({
            input: fs.createReadStream(logfile),
            output: process.stdout,
            terminal: false
        });
    
        rl.on('line', function (line) {
            if (line.substr(21,36) === r2sPid) {
                logLines.push(line.substr(58))
            }
        });
    
        rl.on('close', function() {
            resolve(logLines)
        });
        })
    }

module.exports = {

    readbyr2sPid: logreader

}