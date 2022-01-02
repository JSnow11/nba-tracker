import { axios } from "./axios";

const playerApi = {
  getPlayers: () => axios.get("/search/players?query="),
  getPlayer: (playerName: string) =>
    axios.get(`/search/players?query=${playerName}`),

  searchPlayers: (searchTerm: string) =>
    axios.get(`/search/players?query=${searchTerm}`),
};

export default playerApi;
