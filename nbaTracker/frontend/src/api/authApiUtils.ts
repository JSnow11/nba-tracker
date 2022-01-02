import { axios } from "./axios";

const authApi = {
  login: (username: string, password: string) =>
    axios.post("/auth", {
      username,
      password,
    }),
  logout: () => axios.delete("/auth"),

  register: (
    username: string,
    password: string,
    favs: { team: string; player: string }
  ) =>
    axios.post("/auth/register", {
      username,
      password,
      fav_team: favs.team,
      fav_player: favs.player,
    }),
};

export default authApi;
