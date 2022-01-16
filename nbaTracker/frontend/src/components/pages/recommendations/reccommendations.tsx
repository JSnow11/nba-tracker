import React, { useEffect } from "react";

import { playerType, teamType } from "types";
import { recommendApi } from "api";

import { Title } from "components/01-atoms";
import { Player, Team } from "components/03-organisms";

import Page from "../page";
import { Divider } from "@mui/material";
import { Info } from "@mui/icons-material";

const RecommendationsPage = () => {
  const [teams, setTeams] = React.useState<teamType.Team[]>();
  const [playersByStats, setPlayersByStats] =
    React.useState<playerType.Player[]>();
  const [playersByTags, setPlayersByTags] =
    React.useState<playerType.Player[]>();

  useEffect(() => {
    recommendApi
      .recommendTeams()
      .then((res) => {
        setTeams(res.data.by_search);
      })
      .catch((err) => {
        console.log(err);
      });
    recommendApi
      .recommendPlayers()
      .then((res) => {
        setPlayersByStats(res.data.by_stat);
        setPlayersByTags(res.data.by_tags);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <Page title="Recommendations">
      <Title title="Teams" variant="subtitle1" />
      <div className="grid grid-cols-3 gap-3 xl:grid-cols-4">
        {teams?.map((team: teamType.Team) => (
          <Team.Card team={team} />
        ))}
      </div>
      <br></br>
      <br></br>
      <Title title="Players" variant="subtitle1" />

      {!playersByStats || playersByStats.length === 0 ? (
        <div className="w-full border rounded p-8 bg-slate-100 mt-10">
          <Info /> <p>We still don't know what do you like.</p>{" "}
          <p>
            Search and open some players and teams in order to get some
            recommendations
          </p>
        </div>
      ) : (
        <>
          <Title title="By Stats" variant="subtitle2" />
          <div className="grid grid-cols-3 gap-3 xl:grid-cols-4 mb-5">
            {playersByStats?.map((player: playerType.Player) => (
              <Player.Card player={player} />
            ))}
          </div>
          <Title title="By Tags" variant="subtitle2" />
          <div className="grid grid-cols-3 gap-3 xl:grid-cols-4 mb-5">
            {playersByTags?.map((player: playerType.Player) => (
              <Player.Card player={player} />
            ))}
          </div>
        </>
      )}
    </Page>
  );
};

export default RecommendationsPage;
