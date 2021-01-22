const express = require('express')
const app = express()
const axios = require('axios')
 
const PORT = 3000;
const HOST = '0.0.0.0';

console.log(process.env)

app.get('/', (req, res) => {
    res.send("Nothing here")
})

app.get('/health-check', (req, res) => {
    res.send("Healthy")
})

app.get('/addAnimal/:newAnimal',  async (req, res) => {
    const animalURL = `http://${process.env.APP_2_SERVICE_HOST}:${process.env.APP_2_SERVICE_PORT}/${process.env.APP_2_SERVICE_PATH}/addAnimal/${req.params.newAnimal}`
    await addAnimal(animalURL)
  res.send('axios request sent')
})

const addAnimal = async (animalURL) => {
    await axios.post(animalURL).then(response => {
        console.log(response.data)
    }).catch(error => {
        console.log(error)
    })
}


app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);