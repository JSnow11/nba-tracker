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

const searchTypes = [
  {
    value: "search",
    label: "Search",
  },
  {
    value: "recommend",
    label: "Recommend",
  },
];

const SearchBar = (props: { setResults: any }) => {
  const navigate = useNavigate();

  const {
    control,
    getValues,
    reset,
    formState: { errors },
    setError,
  } = useForm<searchInputs>();

  const onSubmit = (data: any) => {
    if (data.searchOption === "team")
      teamApi
        .searchTeams(data.keywords)
        .then((res) => {
          props.setResults(res.data);
          navigate("/results");
        })
        .catch((err) => {
          console.log(err);
          setError("keywords", err.message);
        });
    if (data.searchOption === "player")
      playerApi
        .searchPlayers(data.keywords)
        .then((res) => {
          props.setResults(res.data);
          navigate("/results");
        })
        .catch((err) => {
          console.log(err);
          setError("keywords", err.message);
        });

    reset();
  };

  return (
    <Box className="w-full inline-flex justify-center">
      <form
        className="flex w-full justify-center"
        onSubmit={() => onSubmit(getValues())}
      >
        <Input.Select
          name="search_type"
          control={control}
          options={searchTypes}
        />
        <Input.Select
          name="search_by"
          control={control}
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
