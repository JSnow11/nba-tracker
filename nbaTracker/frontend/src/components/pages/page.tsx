import React from "react";
import { Box } from "@mui/material";

import { Title } from "components/01-atoms";
import { SearchBar } from "components/templates";

const Page = (props: {
  title: string;
  children?: JSX.Element | JSX.Element[] | string;
}) => {
  return (
    <Box className="inline-block w-10/12 h-screen py-5 pl-24 pr-20 overflow-y-scroll">
      <SearchBar />

      <Box id="content" className="w-full my-5 inline-block">
        <Title title={props.title} variant="h4" />
        {props.children}
      </Box>
    </Box>
  );
};

export default Page;
