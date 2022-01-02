import Text from "./Text/TextInput";
import Secret from "./Secret/SecretInput";
import Radio from "./Radio/RadioInput";
import Select from "./Select/SelectInput";

export type FieldProps = {
  name: string;
  control: any;
  error?: string;
  rules?: any;
};

export type Option = {
  label: string;
  value: string;
};

export type RadioProps = FieldProps & {
  options: Option[];
};

export type SelectProps = FieldProps & {
  options: Option[];
};

export type InputProps = FieldProps & {
  type?: "text" | "password";
  useFormLabel?: boolean;
};

export const Input = { Text, Secret, Radio, Select };
