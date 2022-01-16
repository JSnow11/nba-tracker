import React from "react";
import { Info } from "@mui/icons-material";

import Page from "../page";

const NotFoundPage = () => {
  return (
    <Page title="404">
      <div className="w-full border rounded py-10 px-20 bg-gray-100 mt-10">
        <Info />
        <p className="font-bold">Nothing found, </p>{" "}
        <p>Search for something,</p>
        <p className="px-32">
          you can use the <strong>selector</strong> to choose between{" "}
          <strong>teams</strong> or <strong>players</strong> and then add some
          name, number, team, ... to the <strong>keywords</strong> and press{" "}
          <strong>enter</strong>
        </p>
      </div>
    </Page>
  );
};

export default NotFoundPage;
