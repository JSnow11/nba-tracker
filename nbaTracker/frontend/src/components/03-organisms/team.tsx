import React from "react";
import Box from "@mui/material/Box";

import { playerType, teamType } from "types";
import { Title } from "components/01-atoms";
import { Player } from ".";
import { useNavigate } from "react-router";

const List = (props: { team: teamType.Team; pos: number }) => {
  const navigate = useNavigate();

  return (
    <div
      onClick={() => {
        navigate(`/results/team/${props.team.abbreviation}`);
      }}
      className="hover:bg-slate-200 hover:font-bold cursor-pointer flex items-center gap-4 w-full border rounded-sm p-3"
    >
      <span>{"#" + props.pos}</span>
      <img src={props.team.logo_url} className="w-10" alt="logo" />
      <span>{props.team.name}</span>
      <div className="w-auto ml-auto">
        <TeamWinLossIndicator
          wins={props.team.wins}
          losses={props.team.losses}
        />
      </div>
    </div>
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
  const navigate = useNavigate();

  return (
    <div
      onClick={() => {
        navigate(`/results/team/${props.team.abbreviation}`);
      }}
      className="hover:bg-slate-200 cursor-pointer border rounded-md shadow-sm p-2 flex flex-col items-center gap-3"
    >
      <TeamWinLossIndicator wins={props.team.wins} losses={props.team.losses} />
      <img src={props.team.logo_url} className="w-24" alt="logo" />
      <Title title={props.team.name} variant="subtitle1" />
    </div>
  );
};

const Details = (props: { team: teamType.Team }) => {
  return (
    <>
      <Card team={props.team} />
      <div className="col-span-4"> Roaster </div>
      {props.team?.players
        ?.sort((p1, p2) => p1.number - p2.number)
        ?.map((p) => (
          <Player.Card player={p} />
        ))}
    </>
  );
};

export const Team = { List, Card, Details };
