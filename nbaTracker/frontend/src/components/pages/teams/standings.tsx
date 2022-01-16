import React from "react";

import { authApi, teamApi } from "api";
import { teamType } from "types";

import { Loader, Title } from "components/01-atoms";
import { Team } from "components/03-organisms";
import Page from "../page";

const StandingsPage = () => {
  const [teams, setTeams] = React.useState<teamType.Team[]>();
  const [refetch, setRefetch] = React.useState(false);

  const refetchTeams = () => {
    setRefetch(!refetch);
  };

  React.useEffect(() => {
    teamApi
      .getTeams()
      .then((res) => {
        setTeams(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [refetch]);

  return (
    <Page title={"Standings and Stats"}>
      <div className="flex justify-center gap-10">
        <div className="w-1/2 flex flex-col items-center gap-2">
          <Title title={"Western"} variant="subtitle1" />
          {!!teams ? (
            teams
              .filter((t) => t.conference === "Western")
              .sort((a, b) => b.wins - a.wins)
              .map((t, i) => <Team.List pos={i + 1} team={t} />)
          ) : (
            <Loader />
          )}
        </div>
        <div className="w-1/2 flex flex-col items-center gap-2">
          <Title title={"Eastern"} variant="subtitle1" />
          {!!teams ? (
            teams
              .filter((t) => t.conference === "Eastern")
              .sort((a, b) => b.wins - a.wins)
              .map((t, i) => <Team.List pos={i + 1} team={t} />)
          ) : (
            <Loader />
          )}
        </div>
      </div>
    </Page>
  );
};

export default StandingsPage;
