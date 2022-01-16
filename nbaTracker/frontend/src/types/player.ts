import { Team } from "./team";

export type Tag = {
  name: string;
};

export type Player = {
  name: string;
  img_url: string;

  min_per_game: number;
  pts_per_game: number;
  field_goal: number;
  three_p_ptg: number;
  ft_ptg: number;
  reb_per_game: number;
  ast_per_game: number;
  tov_per_game: number;
  stl_per_game: number;
  blk_per_game: number;
  team?: Team;
  tags?: Tag[];
  number: number;
  plus_minus: number;
  position: string;
  country: string;
};
