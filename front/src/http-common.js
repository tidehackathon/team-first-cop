import axios from "axios";

export default axios.create({
  baseURL: "http://20.245.26.188:8000/", // comment for local development
  headers: {
    "Content-type": "application/json"
  }
});
