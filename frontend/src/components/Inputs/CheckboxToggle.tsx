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
    <div className={`relative transition-all py-[0.1rem] px-4 rounded-full text-center border border-sky-500 ${value ? "bg-sky-500 text-white" : "text-sky-500 hover:bg-sky-500/25"}`}>
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
