const util = () => {
  return null;
};

const getTagClasses = (tag: string) => {
  console.log(tag);
  switch (tag) {
    case "ANOTADOR":
      return "border-red-600 text-red-600";
    case "3PT":
      return "border-fuchsia-600 text-fuchsia-600";
    case "ASISTENTE":
      return "border-blue-600 text-blue-600";
    case "REBOTEADOR":
      return "border-slate-600 text-slate-600";
    case "TAPONADOR":
      return "border-lime-600 text-lime-600";
    case "LADRON":
      return "border-orange-600 text-orange-600";
    case "DEFENSOR":
      return "border-green-600 text-green-600";
    case "STAR":
      return "border-yellow-600 text-yellow-600";
    default:
      return "border-gray-600 text-gray-600";
  }
};

const parseErrors = (error: any) => {
  return error.response.data?.join(", ");
};

export { util, parseErrors, getTagClasses };
