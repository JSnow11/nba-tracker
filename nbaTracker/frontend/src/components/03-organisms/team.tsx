import React from "react";
import Box from "@mui/material/Box";

import { teamType } from "types";

const List = (props: { team: teamType.Team }) => {
  return <Box className="w-full boder rounded p-2">{props.team.name}</Box>;
};

const Card = (props: { team: teamType.Team }) => {
  return (
    <Box className="w-full boder rounded p-2">
      <Box className="w-full boder rounded p-2">{props.team.name}</Box>
    </Box>
  );
};

const Details = (props: { team: teamType.Team }) => {
  return <Box className="w-1/5 p-2"></Box>;
};

export const Team = { List, Card, Details };
