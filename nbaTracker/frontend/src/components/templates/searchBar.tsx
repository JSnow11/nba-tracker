import React from "react";
import { Box } from "@mui/material";
import { Search } from "@mui/icons-material";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import { IconButton, Input } from "components/01-atoms";

type searchInputs = {
  search_by: string;
  keywords: string;
};

const searchOptions = [
  {
    value: "team",
    label: "Team",
  },
  {
    value: "player",
    label: "Player",
  },
];

const SearchBar = () => {
  const navigate = useNavigate();

  const {
    control,
    getValues,
    formState: { errors },
  } = useForm<searchInputs>();

  const onSubmit = (data: searchInputs) => {
    navigate(`/results/${data.search_by}/${data.keywords}`);
  };

  return (
    <Box className="w-full inline-flex justify-center">
      <form
        className="flex w-full justify-center"
        onSubmit={(e) => {
          e.preventDefault();
          onSubmit(getValues());
        }}
      >
        <Input.Select
          name="search_by"
          control={control}
          defaultValue="team"
          options={searchOptions}
        />
        <Input.Text
          name="keywords"
          control={control}
          error={errors.keywords?.message}
        />
        <IconButton type="submit" title="Search" icon={<Search />} />
      </form>
    </Box>
  );
};

export default SearchBar;
