import React, { ReactElement } from "react";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { Tooltip } from "@mui/material";
import {
  Search,
  GraphicEqOutlined,
  Logout,
  StarBorder,
  AdminPanelSettingsOutlined,
} from "@mui/icons-material";
import { Link, useLocation } from "react-router-dom";

import logo from "static/img/logo.png";
import { IconButton } from "components/01-atoms";
import { authApi } from "api";
import { sessionUtils } from "utils";

const LinkTab = (props: {
  label?: string;
  icon?: ReactElement;
  href?: string;
}) => {
  return (
    <Link to={props.href || "."}>
      <Tooltip title={props.label || ""}>
        <Tab {...props} />
      </Tooltip>
    </Link>
  );
};

const Menu = () => {
  const [value, setValue] = React.useState(0);

  const location = useLocation();

  React.useEffect(() => {
    const tab = location.pathname.split("/")[1];
    if (tab === "" || tab === "standings") setValue(0);
    else if (tab === "results") setValue(1);
    else if (tab === "recommendations") setValue(2);
    else if (tab === "admin") setValue(3);
  }, [location]);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <Box className="inline-flex flex-col w-2/12 h-screen py-4 justify-between items-center bg-gray-200">
      <img src={logo} alt="logo" className="w-1/3" />{" "}
      <span className="font-bold">Tracker</span>
      <nav className="w-full h-3/4 items-center mt-10">
        <Tabs
          value={value}
          onChange={handleChange}
          aria-label="nav tabs"
          orientation="vertical"
          centered
        >
          <LinkTab
            label="Standings"
            icon={<GraphicEqOutlined />}
            href="/standings"
          />
          <LinkTab label="Search" icon={<Search />} href="/results/" />
          <LinkTab
            label="Reccomend"
            icon={<StarBorder />}
            href="/recommendations"
          />
          <LinkTab
            label="Admin"
            icon={<AdminPanelSettingsOutlined />}
            href="/admin"
          />
        </Tabs>
      </nav>
      <IconButton
        icon={<Logout />}
        title="Logout"
        onClick={() => authApi.logout().finally(() => sessionUtils.logout())}
      />
    </Box>
  );
};

export default Menu;
