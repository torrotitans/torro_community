import { DELETE, GET, POST, PUT } from "@lib/data/api-types";

const API_URL = "http://localhost:3000/";

const config = {
  getUserInfo: {
    url: "/api/login2",
    method: POST,
  },
};

export default config;
