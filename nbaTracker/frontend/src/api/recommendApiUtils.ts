import { axios } from "./axios";

const recommendApi = {
  recommendTeams: () => axios.get("/recommend/teams"),
  recommendPlayers: () => axios.get("/recommend/players"),
};

export default recommendApi;
