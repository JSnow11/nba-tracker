import React from "react";

import { InputLabel, MenuItem, Select } from "@mui/material";
import { Controller } from "react-hook-form";
import { Option, SelectProps } from "..";

const Component = (props: SelectProps) => {
  return (
    <Controller
      name={props.name}
      control={props.control}
      rules={props.rules}
      render={({ field, fieldState }) => (
        <>
          <InputLabel id={"label-" + props.name}>{props.name}</InputLabel>
          <Select
            className="min-w-xs"
            labelId={"label-" + props.name}
            label={props.name}
            {...field}
          >
            {props.options.map((option: Option, index: number) => (
              <MenuItem value={option.value}>{option.label}</MenuItem>
            ))}
          </Select>
        </>
      )}
    />
  );
};

export default Component;
