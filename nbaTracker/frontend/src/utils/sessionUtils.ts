const sessionUtils = {
  getToken: () => {
    return document.cookie
      .split("; ")
      ?.find((row) => row.startsWith("token"))
      ?.split("=")?.[1];
  },
  setToken: (cookie?: string) => {
    if (cookie) document.cookie = cookie;
  },
  removeToken: () => {
    document.cookie = "token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
  },
};

export default sessionUtils;
