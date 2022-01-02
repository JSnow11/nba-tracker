import React from "react";
import Box from "@mui/material/Box";

import { playerType } from "types";

const List = (props: { player: playerType.Player }) => {
  return <Box className="w-full boder rounded p-2">{props.player.name}</Box>;
};

const Card = (props: { team: playerType.Player }) => {
  return (
    <Box className="w-full boder rounded p-2">
      <Box className="w-full boder rounded p-2">{props.team.name}</Box>
    </Box>
  );
};

const Details = (props: { team: playerType.Player }) => {
  return <Box className="w-1/5 p-2"></Box>;
};

export const Team = { List, Card, Details };
