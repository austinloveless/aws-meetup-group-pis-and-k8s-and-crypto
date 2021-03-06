const express = require('express')
const app = express()

const PORT = 3002;
const HOST = '0.0.0.0';

const arrayData = ["dog", "cat"]
 
app.get('/', (req, res) => {
  res.send("Nothing here")
})

app.get('/listAnimals', function (req, res) {
  res.send(arrayData)
})

app.get('/health-check', (req, res) => {
  res.send("Healthy")
})

app.post('/addAnimal/:newAnimal', (req, res )  => {
    arrayData.push(req.params.newAnimal)
    res.send(arrayData)
})

 
app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);