import React, { useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import { Box } from "@mui/material";

import { authApi } from "api";
import { sessionUtils } from "utils";

import { Input, Button } from "components/01-atoms";
import Page from "../page";

type LoginInputs = {
  username: string;
  password: string;
};

const LoginPage = () => {
  const {
    control,
    getValues,
    setError,
    formState: { errors },
  } = useForm<LoginInputs>();

  const [action, setAction] = useState<"login" | "register">("login");

  const onSubmitFailed = (e: any) => {
    if (!e.response) {
      setError("password", { type: "manual", message: "Server Error" });
      setError("username", { type: "manual", message: "" });
    }
    if (e?.response?.status === 400) {
      setError("password", {
        type: "manual",
        message: e.response.data.non_field_errors[0],
      });
      setError("username", {
        type: "manual",
      });
    }
  };

  const onSubmit: SubmitHandler<LoginInputs> = (data) => {
    console.log("Login:", data.username);
    if (action === "login")
      authApi
        .login(data.username, data.password)
        .then((r) => {
          window.location.reload();
        })
        .catch((e) => {
          onSubmitFailed(e);
        });
    if (action === "register")
      authApi
        .register(data.username, data.password)
        .then((r) => {
          window.location.reload();
        })
        .catch((e) => {
          onSubmitFailed(e);
        });
  };

  return (
    <Page title={action}>
      <Box className="flex flex-col w-60 mx-auto my-4">
        <form
          className="space-y-5 mb-5"
          onSubmit={(e) => {
            e.preventDefault();
            onSubmit(getValues());
          }}
        >
          <Input.Text
            name="username"
            control={control}
            error={errors.username?.message}
          />
          <Input.Secret
            name="password"
            control={control}
            error={errors.password?.message}
          />
          <Button title={action} type="submit" />
        </form>
        <Button
          variant="text"
          title={action === "login" ? "Register" : "Login"}
          onClick={() => setAction(action === "login" ? "register" : "login")}
        />
      </Box>
    </Page>
  );
};

export default LoginPage;
