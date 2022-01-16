import { axios } from "./axios";

const authApi = {
  login: (username: string, password: string) =>
    axios.post("/auth", {
      username,
      password,
    }),
  logout: () => axios.delete("/auth"),

  register: (username: string, password: string, email: string) =>
    axios.post("/register", {
      username,
      password,
      email,
    }),
};

export default authApi;
