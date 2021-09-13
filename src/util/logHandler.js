const fs         = require('fs');
const readline   = require('readline');
//const { Readable } = require('stream');


/* let readlog = function(file) {

    const fsp = fs.promises;
    return async () => {
        const data = fs.readFile(file, "binary");
        return Buffer.from(data);
    }

} */


let logreader = function readLog(file, r2sPid){
        return new Promise((resolve, reject) => {
        let logLines = []
        let rl = readline.createInterface({
            input:  fs.createReadStream(file),
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