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
        <label className="text-sm font-medium text-gray-900 dark:text-gray-300">
          {label}
        </label>
        <input
          {...register(fieldName, {
            required: requiredErrorMessage,
          })}
          placeholder={placeholder}
          className="py-1 px-3 rounded-full border border-gray-300 dark:border-gray-600 dark:bg-gray-600 text-gray-900 dark:text-gray-300"
          type={type}
        />
      </div>
      {errors[fieldName] && (
        <span className="text-red-500 text-sm">{`${errors[fieldName]?.message}`}</span>
      )}
    </>
  );
}
