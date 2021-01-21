const express = require('express')
const app = express()

const PORT = 3000;
const HOST = '0.0.0.0';

const arrayData = ["dog", "cat"]
 
app.get('/', function (req, res) {
  res.send(arrayData)
})

app.post('/:animal', (req, res )  => {
    arrayData.push(req.params.animal)
    res.send(arrayData)
})
 
app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);