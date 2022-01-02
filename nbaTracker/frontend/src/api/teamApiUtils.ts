import { axios } from "./axios";

const teamApi = {
  getTeams: () => axios.get("/search/teams?query="),
  getTeam: (teamAbbr: string) => axios.get(`/search/teams?query=${teamAbbr}`),

  searchTeams: (searchTerm: string) =>
    axios.get(`/search/teams?query=${searchTerm}`),
};

export default teamApi;
