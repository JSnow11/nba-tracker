import React from "react";

import { playerApi, teamApi } from "api";
import { playerType, teamType } from "types";

import { Loader, Title } from "components/01-atoms";
import { Player, Team } from "components/03-organisms";
import Page from "../page";

const StandingsPage = () => {
  const [teams, setTeams] = React.useState<teamType.Team[]>();
  const [statLeaders, setStatLeaders] = React.useState<{
    ppg: playerType.Player;
    apg: playerType.Player;
    rpg: playerType.Player;
    blk: playerType.Player;
  }>();

  React.useEffect(() => {
    teamApi
      .getTeams()
      .then((res) => {
        setTeams(res.data);
      })
      .catch((err) => {
        console.log(err);
      });

    playerApi
      .getStatLeaders()
      .then((res) => {
        setStatLeaders(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <Page title={"Standings"}>
      <div className="grid grid-cols-2 gap-3 xl:grid-cols-4 mb-5">
        {statLeaders?.ppg && (
          <Player.StatLeader
            player={statLeaders?.ppg}
            stat="PTS per Game"
            value={statLeaders?.ppg.pts_per_game}
          />
        )}
        {statLeaders?.apg && (
          <Player.StatLeader
            player={statLeaders?.apg}
            stat="AST per Game"
            value={statLeaders?.apg.ast_per_game}
          />
        )}
        {statLeaders?.rpg && (
          <Player.StatLeader
            player={statLeaders?.rpg}
            stat="REB per Game"
            value={statLeaders?.rpg.reb_per_game}
          />
        )}
        {statLeaders?.blk && (
          <Player.StatLeader
            player={statLeaders?.blk}
            stat="BLK per Game"
            value={statLeaders?.blk.blk_per_game}
          />
        )}
      </div>
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
