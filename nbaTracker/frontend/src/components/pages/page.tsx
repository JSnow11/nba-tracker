import React from "react";
import { Box } from "@mui/material";

import { Title } from "components/01-atoms";
import { SearchBar } from "components/templates";
import { playerType, teamType } from "types";

const initialState: { teams: teamType.Team[]; players: playerType.Player[] } = {
  teams: [],
  players: [],
};
export const SearchContext = React.createContext(initialState);

const Page = (props: {
  title: string;
  children?: JSX.Element | JSX.Element[] | string;
}) => {
  const [results, setResults] = React.useState<{
    teams: teamType.Team[];
    players: playerType.Player[];
  }>(initialState);

  return (
    <SearchContext.Provider value={results}>
      <Box className="inline-block w-10/12 h-screen ml-10 p-5 overflow-scroll">
        <SearchBar setResults={setResults} />

        <Box id="content" className="w-full my-5 inline-block">
          <Title title={props.title} variant="h4" />
          {props.children}
        </Box>
      </Box>
    </SearchContext.Provider>
  );
};

export default Page;
