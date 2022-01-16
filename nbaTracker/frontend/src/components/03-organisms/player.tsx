import React from "react";
import Box from "@mui/material/Box";

import { playerType } from "types";
import { Title } from "components/01-atoms";
import { Chip, Divider } from "@mui/material";
import { utils } from "utils";

const List = (props: { player: playerType.Player }) => {
  return <Box className="w-full boder rounded p-2">{props.player.name}</Box>;
};

const PlayerStatsReduced = (props: { player: playerType.Player }) => {
  return (
    <div className="text-xs">
      <span className="font-bold">Stats: </span>
      <div className="flex justify-center gap-x-3 gap-y-1 flex-wrap">
        <span className="hover:bg-slate-100 p-1 border rounded">
          {props.player.pts_per_game} ppg
        </span>
        <span className="hover:bg-slate-100 p-1 border rounded">
          {props.player.field_goal} %fg
        </span>
      </div>
    </div>
  );
};

const PlayerTags = (props: { player: playerType.Player }) => {
  return (
    <div className="text-xs h-8">
      <div className="flex justify-center gap-x-3 gap-y-1 flex-wrap">
        {props.player.tags?.map((t) => (
          <span
            className={`p-1 border rounded bg-${utils.getTagColor(
              t.name
            )}-200 border-${utils.getTagColor(
              t.name
            )}-600 text-${utils.getTagColor(t.name)}-600`}
          >
            {t.name}
          </span>
        ))}
      </div>
    </div>
  );
};

const PlayerStatLeader = (props: {
  player: playerType.Player;
  stat: string;
}) => {
  return <div></div>;
};

const Card = (props: { player: playerType.Player }) => {
  const isStar = !!props.player.tags?.find((t) => t.name === "STAR");

  return (
    <div
      className={
        "hover:bg-slate-200 cursor-pointer border rounded-md shadow-sm p-2 flex flex-col items-center gap-3 " +
        (isStar ? "border-yellow-600" : "")
      }
    >
      {props.player.team && (
        <div className="w-full flex justify-between items-center">
          <img src={props.player.team?.logo_url} className="w-8" alt="logo" />
          <span>{props.player.team?.abbreviation}</span>
        </div>
      )}
      <img src={props.player.img_url} className="w-32" alt="logo" />

      <Title title={props.player.name} variant="subtitle1" />
      <PlayerTags player={props.player} />
      <div className="w-full flex justify-between">
        <span className="text-gray-500 font-bold">#{props.player.number}</span>
        <span>{props.player.position}</span>
      </div>
    </div>
  );
};

const Details = (props: { player: playerType.Player }) => {
  return <Box className="w-1/5 p-2"></Box>;
};

export const Player = { List, Card, Details };
