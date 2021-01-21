const express = require('express')
const app = express()
const axios = require('axios')
 
const PORT = 3000;
const HOST = '0.0.0.0';

app.get('/:animal',  async (req, res) => {
    const animalURL = `http://${process.env.APP_2_SERVICE_HOST}:${process.env.APP_2_SERVICE_PORT}/${process.env.APP_2_SERVICE_PATH}/${req.params.animal}`
   
    await addAnimal(animalURL)
  res.send('axios request sent')
})

const addAnimal = async () =>  await axios.post(`http://?:${process.env.APP_2_PORT}/${req.params.animal}`).then(response => {
    console.log(response.data)
}).catch(error => {
    console.log(error)
})
 
app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);