const util = () => {
  return null;
};

const getTagColor = (tag: string) => {
  console.log(tag);
  switch (tag) {
    case "ANOTADOR":
      return "red";
    case "3PT":
      return "fuchsia";
    case "ASISTENTE":
      return "blue";
    case "REBOTEADOR":
      return "slate";
    case "TAPONADOR":
      return "lime";
    case "LADRON":
      return "orange";
    case "DEFENSOR":
      return "green";
    case "STAR":
      return "yellow";
    default:
      return "gray";
  }
};

const parseErrors = (error: any) => {
  return error.response.data?.join(", ");
};

export { util, parseErrors, getTagColor };
