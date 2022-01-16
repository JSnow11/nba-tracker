import React from "react";
import Box from "@mui/material/Box";

import { playerType } from "types";
import { Title } from "components/01-atoms";
import { utils } from "utils";
import { useNavigate } from "react-router";

const List = (props: { player: playerType.Player }) => {
  return <Box className="w-full boder rounded p-2">{props.player.name}</Box>;
};

const PlayerTags = (props: { player: playerType.Player }) => {
  return (
    <div className="text-xs h-8">
      <div className="flex justify-center gap-x-3 gap-y-1 flex-wrap">
        {props.player.tags?.map((t) => {
          const color = utils.getTagClasses(t.name);
          return (
            <span className={`${color} p-1 border-2 rounded `}>{t.name}</span>
          );
        })}
      </div>
    </div>
  );
};

const StatLeader = (props: {
  player: playerType.Player;
  stat: string;
  value: number;
}) => {
  return (
    <div className="flex flex-col gap-2 mt-3">
      <div className="flex items-center justify-between border rounded p-2 border-yellow-600 text-yellow-600 hover:bg-yellow-100">
        <span>{props.stat}</span>
        <span className="font-bold text-lg">{props.value}</span>
      </div>
      <Card player={props.player} />
    </div>
  );
};

const Card = (props: { player: playerType.Player }) => {
  const navigate = useNavigate();

  const isStar = !!props.player.tags?.find((t) => t.name === "STAR");

  return (
    <div
      className={
        "hover:bg-gray-200 cursor-pointer border rounded-md shadow-sm p-2 flex flex-col items-center gap-3 " +
        (isStar ? "border-yellow-600" : "")
      }
      onClick={() => {
        navigate(`/results/player/${props.player.name}`);
      }}
    >
      <div className="flex justify-between items-center w-full p-2">
        {props.player.team && (
          <>
            <img src={props.player.team?.logo_url} className="w-8" alt="logo" />
            <span>{props.player.team?.abbreviation}</span>
          </>
        )}
      </div>

      <img src={props.player.img_url} className="w-32" alt="logo" />

      <Title title={props.player.name} variant="subtitle1" />
      <PlayerTags player={props.player} />
      <div className="w-full flex justify-between p-2">
        <span className="text-gray-500 font-bold">#{props.player.number}</span>
        <span>{props.player.position}</span>
      </div>
    </div>
  );
};

const Details = (props: { player: playerType.Player }) => {
  return (
    <Box className="col-span-4 grid grid-cols-6 hover:bg-slate-100 border rounded-md shadow-sm p-2 gap-6">
      <div className="flex flex-col items-center justify-between col-span-2">
        <img src={props.player.img_url} className="w-56 mb-4" alt="logo" />
        <PlayerTags player={props.player} />
        <Title title={props.player.name} variant="subtitle1" />
      </div>
      <div className="flex flex-col items-start">
        <span className="font-bold">Team: </span>
        <span className="flex gap-6 items-center">
          <img src={props.player.team?.logo_url} className="w-10" alt="logo" />{" "}
          {props.player.team?.abbreviation}
        </span>
        <br />

        <span className="font-bold">Position: </span>
        <span>{props.player.position}</span>

        <span className="font-bold">Number: </span>
        <span>#{props.player.number}</span>

        <span className="font-bold">Country: </span>
        <span>{props.player.country}</span>
      </div>
      <div className="flex flex-col items-start gap-2">
        <div className="flex justify-between items-center w-full border rounded-sm p-2">
          <span className="font-bold">MPG: </span>
          <span>{props.player.min_per_game}</span>
        </div>
        <div className="flex justify-between items-center w-full border rounded-sm p-2">
          <span className="font-bold">PPG: </span>
          <span>{props.player.pts_per_game}</span>
        </div>
        <div className="flex justify-between items-center w-full border rounded-sm p-2">
          <span className="font-bold">%FG: </span>
          <span>{props.player.field_goal}</span>
        </div>
        <div className="flex justify-between items-center w-full border rounded-sm p-2">
          <span className="font-bold">%3P: </span>
          <span>{props.player.three_p_ptg}</span>
        </div>
        <div className="flex justify-between items-center w-full border rounded-sm p-2">
          <span className="font-bold">%FT: </span>
          <span>{props.player.ft_ptg}</span>
        </div>
      </div>
      <div className="flex flex-col items-start gap-2">
        <div className="flex justify-between items-center w-full border rounded-sm p-2">
          <span className="font-bold">APG: </span>
          <span>{props.player.ast_per_game}</span>
        </div>
        <div className="flex justify-between items-center w-full border rounded-sm p-2">
          <span className="font-bold">RPG: </span>
          <span>{props.player.reb_per_game}</span>
        </div>
        <div className="flex justify-between items-center w-full border rounded-sm p-2">
          <span className="font-bold">SPG: </span>
          <span>{props.player.stl_per_game}</span>
        </div>
        <div className="flex justify-between items-center w-full border rounded-sm p-2">
          <span className="font-bold">BPG: </span>
          <span>{props.player.blk_per_game}</span>
        </div>
        <div className="flex justify-between items-center w-full border rounded-sm p-2">
          <span className="font-bold">SPG: </span>
          <span>{props.player.tov_per_game}</span>
        </div>
      </div>
      <div className="flex flex-col items-start gap-2">
        <div
          className={
            "flex justify-between items-center w-full border rounded-sm p-2 " +
            (props.player.plus_minus > 0 ? "text-green-600" : "text-red-600")
          }
        >
          <span className="font-bold">+/-: </span>
          <span>{props.player.plus_minus}</span>
        </div>
      </div>
    </Box>
  );
};

export const Player = { List, Card, Details, StatLeader };
