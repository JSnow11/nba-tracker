import React, { useContext, useMemo } from "react";

import { playerType, teamType } from "types";

import { Title } from "components/01-atoms";
import { Team } from "components/03-organisms";

import Page, { SearchContext } from "../page";

const ResultsPage = () => {
  const searchContext = useContext(SearchContext);

  const resultType = useMemo(
    () => (searchContext.teams.length > 0 ? "team" : "player"),
    [searchContext.teams]
  );

  return (
    <Page title="Teams">
      <Title
        title={`${searchContext} ${
          resultType === "team" ? "Teams" : "Players"
        } Found`}
        variant="h3"
      />
      <div>
        {searchContext.teams.map((team: teamType.Team) => (
          <Team.Card team={team} />
        ))}
        {searchContext.players.map((player: playerType.Player) => (
          <div>{player.name}</div>
        ))}
      </div>
    </Page>
  );
};

export default ResultsPage;
