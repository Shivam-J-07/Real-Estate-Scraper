import { FieldValues, UseFormRegister } from "react-hook-form";

export default function CheckboxInput({
  fieldName,
  label,
  register,
  labelPos = "left",
}: {
  fieldName: string;
  label: string;
  register: UseFormRegister<FieldValues>;
  labelPos?: "left" | "right";
}) {
  return (
    <div className="flex items-center gap-4">
      {labelPos === "left" && (
        <label className="font-medium text-gray-900 dark:text-gray-300">
          {label}
        </label>
      )}
      <input {...register(fieldName)} type="checkbox" />
      {labelPos === "right" && (
        <label className="font-medium text-gray-900 dark:text-gray-300">
          {label}
        </label>
      )}
    </div>
  );
}
