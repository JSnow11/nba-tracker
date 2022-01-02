import React from "react";
import { useParams } from "react-router-dom";

import { teamApi } from "api";
import { teamType } from "types";

import { Team } from "components/03-organisms";
import Page from "../page";
import { Loader } from "components/01-atoms";

const TeamPage = () => {
  const params = useParams<{ abbr: string }>();

  const [team, setTeam] = React.useState<teamType.Team>();
  const [refetch, setRefetch] = React.useState(false);

  const refetchTeams = () => {
    setRefetch(!refetch);
  };

  React.useEffect(() => {
    if (params.abbr)
      teamApi
        .getTeam(params.abbr)
        .then((res) => {
          setTeam(res.data);
        })
        .catch((err) => {
          console.log(err);
        });
  }, [params.abbr, refetch]);

  return (
    <Page title={team?.name || "Error"}>
      {!!team ? <Team.Details team={team} /> : <Loader />}
    </Page>
  );
};

export default TeamPage;
