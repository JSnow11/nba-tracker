import { axios } from "./axios";

const authApi = {
  populate: () => axios.get("/populate"),
  index_search: () => axios.get("/index"),
};

export default authApi;
