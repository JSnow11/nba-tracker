import React from "react";
import { Box } from "@mui/material";
import { Search } from "@mui/icons-material";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import { playerApi, teamApi } from "api";

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
    setError,
  } = useForm<searchInputs>();

  const onSubmit = (data: searchInputs) => {
    if (data.search_by === "team")
      teamApi
        .searchTeams(data.keywords)
        .then((res) => {
          navigate("/results", { state: { results: { teams: res.data } } });
        })
        .catch((err) => {
          console.log(err);
          setError("keywords", err.message);
        });
    if (data.search_by === "player")
      playerApi
        .searchPlayers(data.keywords)
        .then((res) => {
          navigate("/results", { state: { results: { players: res.data } } });
        })
        .catch((err) => {
          console.log(err);
          setError("keywords", err.message);
        });
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
