const sessionUtils = {
  getToken: () => {
    return document.cookie
      .split("; ")
      ?.find((row) => row.startsWith("token"))
      ?.split("=")?.[1];
  },
  getAdmin: () => {
    return document.cookie
      .split("; ")
      ?.find((row) => row.startsWith("admin"))
      ?.split("=")?.[1];
  },
  removeCookie: (cookieName: string) => {
    document.cookie =
      cookieName + "=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
  },
  logout: () => {
    sessionUtils.removeCookie("token");
    sessionUtils.removeCookie("admin");
    window.location.reload();
  },
};

export default sessionUtils;
