import React from "react";

import { sessionUtils } from "utils";
import { adminApi, authApi } from "api";

import { Button, Loader, Title } from "components/01-atoms";

import Page from "../page";
import search from "static/img/search.png";
import stats from "static/img/stats.png";
import byebye from "static/img/byebye.png";
import { Check, Warning } from "@mui/icons-material";

const AdminCard = (props: {
  title: string;
  img: string;
  description: string;
  action: () => void;
  loading?: boolean;
  disabled?: boolean;
  error?: boolean;
}) => {
  return (
    <div className="col-span-1 flex flex-col border rounded-md p-5">
      <img src={props.img} alt={props.title} className="w-32 mx-auto" />
      <div className="my-2">
        <Title title={props.title} variant="subtitle1" />
        <p className="text-xs text-left h-20">{props.description}</p>
      </div>
      <div className="flex justify-between">
        <Button
          title={props.title}
          onClick={props.action}
          disabled={props.disabled}
        />
        {props.loading ? <Loader /> : props.error ? <Warning /> : <Check />}
      </div>
    </div>
  );
};

const AdminPage = () => {
  const [populateStatus, setPopulateStatus] = React.useState<
    "done" | "loading" | "error"
  >("done");
  const [indexStatus, setIndexStatus] = React.useState<
    "done" | "loading" | "error"
  >("done");

  return (
    <Page title="Admin zone">
      <div className="mt-4 grid grid-cols-3 justify-center gap-10">
        <AdminCard
          title="Populate"
          img={search}
          description="Search for info in the NBA official pages, scrap it and save it in the database."
          action={() => {
            setPopulateStatus("loading");
            adminApi
              .populate()
              .then(() => setPopulateStatus("done"))
              .catch(() => setPopulateStatus("error"));
          }}
          loading={populateStatus === "loading"}
          disabled={populateStatus === "loading" || indexStatus === "loading"}
          error={populateStatus === "error"}
        />
        <AdminCard
          title="Index"
          img={stats}
          description="Index the database players and teams and enable full text search for them."
          action={() => {
            setIndexStatus("loading");
            adminApi
              .indexSearch()
              .then(() => setIndexStatus("done"))
              .catch(() => setIndexStatus("error"));
          }}
          loading={indexStatus === "loading"}
          disabled={populateStatus === "loading" || indexStatus === "loading"}
          error={indexStatus === "error"}
        />
        <AdminCard
          title="Logout"
          img={byebye}
          description="Logout from the admin zone."
          action={() => {
            authApi
              .logout()
              .catch()
              .finally(() => sessionUtils.logout());
          }}
          disabled={populateStatus === "loading" || indexStatus === "loading"}
        />
      </div>
    </Page>
  );
};

export default AdminPage;
