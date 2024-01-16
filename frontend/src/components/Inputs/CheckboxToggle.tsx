import { FieldValues, UseFormRegister } from "react-hook-form";

export default function CheckboxToggle({
  fieldName,
  label,
  register,
  value,
}: {
  fieldName: string;
  label: string;
  register: UseFormRegister<FieldValues>;
  value: boolean;
}) {
  return (
    <div className={`relative transition-all py-1 px-4 rounded-full text-center ${value ? "bg-indigo-500/80 dark:bg-indigo-400 text-white" : "bg-slate-200 dark:bg-slate-600 hover:bg-slate-300 dark:hover:bg-slate-500"}`}>
      <input
        {...register(fieldName)}
        className="absolute w-full opacity-0 cursor-pointer"
        type="checkbox"
      />
      <label className="text-sm">
        {label}
      </label>
    </div>
  );
}
