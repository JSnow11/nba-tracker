import React, { useEffect, useMemo } from "react";

import { playerType, teamType } from "types";

import { Title } from "components/01-atoms";
import { Player, Team } from "components/03-organisms";

import Page from "../page";
import { useLocation, useParams } from "react-router";
import { playerApi, teamApi } from "api";

type Results = {
  teams?: teamType.Team[];
  players?: playerType.Player[];
};

const ResultsPage = () => {
  const { searchby, keywords } = useParams();

  const [results, setResults] = React.useState<Results>();

  useEffect(() => {
    console.log(searchby, keywords);
    if (searchby === "player")
      playerApi
        .searchPlayers(keywords || "")
        .then((res) => {
          setResults({ players: res.data });
        })
        .catch((err) => {
          console.log(err);
        });

    if (searchby === "team")
      teamApi
        .searchTeams(keywords || "")
        .then((res) => {
          setResults({ teams: res.data });
        })
        .catch((err) => {
          console.log(err);
        });
  }, [searchby, keywords]);

  const resultsLength = useMemo(
    () => (results?.players?.length || 0) + (results?.teams?.length || 0),
    [results]
  );
  const resultsType = useMemo(
    () => (results?.players ? "Players" : "Teams"),
    [results]
  );

  return (
    <Page title={`${resultsType}`}>
      <Title title={`${resultsLength} Found`} variant="subtitle1" />
      <div className="grid grid-cols-2 gap-3 xl:grid-cols-4 mb-5">
        {!results?.teams?.length ? (
          <></>
        ) : results.teams.length === 1 ? (
          <Team.Details team={results.teams[0]} />
        ) : (
          results?.teams?.map((team: teamType.Team) => (
            <Team.Card team={team} />
          ))
        )}

        {!results?.players ? (
          <></>
        ) : results.players.length === 1 ? (
          <Player.Details player={results.players[0]} />
        ) : (
          results?.players?.map((player: playerType.Player) => (
            <Player.Card player={player} />
          ))
        )}
      </div>
    </Page>
  );
};

export default ResultsPage;
