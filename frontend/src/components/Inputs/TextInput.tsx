import { HTMLInputTypeAttribute } from "react";
import { FieldValues, FieldErrors, UseFormRegister } from "react-hook-form";

export default function TextInput({
  fieldName,
  label,
  placeholder,
  requiredErrorMessage,
  type,
  register,
  errors,
}: {
  fieldName: string;
  label: string;
  placeholder: string;
  requiredErrorMessage?: string;
  type: HTMLInputTypeAttribute | undefined;
  register: UseFormRegister<FieldValues>;
  errors: FieldErrors<FieldValues>;
}) {
  return (
    <>
      <div className="flex items-center gap-4">
        <label className="font-medium text-gray-900 dark:text-gray-300">
          {label}
        </label>
        <input
          {...register(fieldName, {
            required: requiredErrorMessage,
			valueAsNumber: type === "number", // Ensures input is treated as a number
			validate: type == "number" ? ((value) => value > 0 || "The number must be positive") : undefined,
          })}
          placeholder={placeholder}
          className="transition-all py-1 px-3 rounded-full border hover:bg-slate-50 focus:bg-white focus dark:bg-slate-600 dark:hover:bg-slate-500 dark:focus:bg-slate-600 dark:border-slate-500"
          type={type}
        />
      </div>
      {errors[fieldName] && (
        <span className="text-red-500 text-sm">{`${errors[fieldName]?.message}`}</span>
      )}
    </>
  );
}
