import Axios from "axios";

import { sessionUtils } from "utils";

const API_URL = "http://localhost:8000/api";

export const axios = Axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// Auth interceptor (logout)
axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 403 || error.response?.status === 401) {
      sessionUtils.removeCookie("admin");
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

// Error handling interceptor
axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    return Promise.reject(error);
  }
);
