import { axios } from "./axios";

const authApi = {
  populate: () => axios.get("/populate"),
  indexSearch: () => axios.get("/index"),
};

export default authApi;
