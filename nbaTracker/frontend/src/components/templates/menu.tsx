import React, { ReactElement } from "react";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { Tooltip } from "@mui/material";
import { Search, GraphicEqOutlined } from "@mui/icons-material";
import { Link } from "react-router-dom";

import logo from "static/img/logo.png";

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

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <Box className="inline-flex flex-col w-2/12 h-screen pl-4 justify-between items-center bg-slate-300">
      <img src={logo} alt="logo" className="w-1/2" />
      <nav className="w-full h-3/4 items-center">
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
          <LinkTab label="Search" icon={<Search />} href="/results" />
        </Tabs>
      </nav>
    </Box>
  );
};

export default Menu;
