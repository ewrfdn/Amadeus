import axios from "../utils/http/axios"

const text2Audio = async (params) => {
  const res = await axios.post("/vits/text2mp3", params, {
    responseType: "arraybuffer"
  })
  return res
}

const getAllVitsModel = async (params) => {
  const res = await axios.get("/vits/models", params)
  return res
}


export default {
  text2Audio,
  getAllVitsModel,
}