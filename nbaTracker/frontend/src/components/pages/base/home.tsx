import React from "react";

import { sessionUtils } from "utils";
import { authApi } from "api";

import { Button } from "components/01-atoms";

import Page from "../page";

const HomePage = () => {
  return (
    <Page title="Home">
      <Button
        title="Logout"
        onClick={() =>
          authApi.logout().finally(() => {
            sessionUtils.removeCookie("token");
            sessionUtils.removeCookie("admin");
            window.location.reload();
          })
        }
      />
    </Page>
  );
};

export default HomePage;
