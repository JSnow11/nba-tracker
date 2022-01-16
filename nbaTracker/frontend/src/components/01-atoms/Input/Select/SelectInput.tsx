import React from "react";

import { InputLabel, MenuItem, Select } from "@mui/material";
import { Controller } from "react-hook-form";
import { Option, SelectProps } from "..";

const Component = (props: SelectProps) => {
  return (
    <Controller
      name={props.name}
      control={props.control}
      defaultValue={props.defaultValue}
      rules={props.rules}
      render={({ field, fieldState }) => (
        <Select
          labelId={`select-label-${props.name}`}
          label={props.name}
          {...field}
        >
          {props.options.map((option: Option) => (
            <MenuItem value={option.value}>{option.label}</MenuItem>
          ))}
        </Select>
      )}
    />
  );
};

export default Component;
