import React from "react";
import Box from "@mui/material/Box";

import { teamType } from "types";
import { Title } from "components/01-atoms";

const List = (props: { team: teamType.Team; pos: number }) => {
  return (
    <Box className="hover:bg-slate-200 hover:font-bold cursor-pointer flex items-center gap-4 w-full border rounded-sm p-3">
      <span>{"#" + props.pos}</span>
      <img src={props.team.logo_url} className="w-10" alt="logo" />
      <span>{props.team.name}</span>
      <div className="w-auto ml-auto">
        <TeamWinLossIndicator
          wins={props.team.wins}
          losses={props.team.losses}
        />
      </div>
    </Box>
  );
};

const TeamWinLossIndicator = (props: { wins: number; losses: number }) => {
  return (
    <div className="flex mx-5 justify-between">
      <span className="text-green-900">{props.wins}W</span>/
      <span className="text-red-900">{props.losses}L</span>
    </div>
  );
};

const Card = (props: { team: teamType.Team }) => {
  return (
    <div className="hover:bg-slate-200 cursor-pointer border rounded-md shadow-sm p-2 flex flex-col items-center gap-3">
      <TeamWinLossIndicator wins={props.team.wins} losses={props.team.losses} />
      <img src={props.team.logo_url} className="w-24" alt="logo" />
      <Title title={props.team.name} variant="subtitle1" />
    </div>
  );
};

const Details = (props: { team: teamType.Team }) => {
  return <Box className="w-1/5 p-2"></Box>;
};

export const Team = { List, Card, Details };
