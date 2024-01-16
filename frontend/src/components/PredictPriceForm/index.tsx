import { useEffect } from "react";
import { FieldValues, useForm } from "react-hook-form";
import TextInput from "../Inputs/TextInput";
import CheckboxToggle from "../Inputs/CheckboxToggle";
import CheckboxInput from "../Inputs/CheckboxInput";

export default function PricePredictForm({
  setPredictedPrice,
  setIsLoading,
}: {
  setPredictedPrice: React.Dispatch<React.SetStateAction<number>>;
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();

  const submitForm = async (data: FieldValues) => {
    setIsLoading(true);
    if (process.env.NEXT_PUBLIC_API_URL) {
      const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/predict`;
      try {
        const apiResponse = await fetch(apiUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        // Check if the request was successful
        if (apiResponse.ok) {
          const { price_prediction } = await apiResponse.json();
          setPredictedPrice(Number(price_prediction));
        } else {
          console.error(
            "Error making request to external API:",
            apiResponse.statusText
          );
        }
      } catch (error) {
        console.error("Error handling POST request:", error);
      }
    }
    setIsLoading(false);
  };

  return (
    <div className="max-w-lg flex flex-col gap-4 p-8 text-sm">
      <h1 className="text-3xl font-medium">Rental Pricing Estimate</h1>
      <p className="text-sm">
        Provide the details for your rental unit listing and we&apos;ll give a
        price prediction for a monthly rate based on this month&apos;s rental
        listings.
      </p>
      <hr className="border-gray-300 dark:border-gray-600" />

      <TextInput
        fieldName="bed"
        label="Bedrooms"
        placeholder="Number of bedrooms"
        requiredErrorMessage="Enter number of bedrooms"
        type="number"
        register={register}
        errors={errors}
      />

      <TextInput
        fieldName="bath"
        label="Bathrooms"
        placeholder="Number of bathrooms"
        requiredErrorMessage="Enter number of bathrooms"
        type="number"
        register={register}
        errors={errors}
      />

      <TextInput
        fieldName="sqft"
        label="Area (sqft)"
        placeholder="Sqft"
        requiredErrorMessage="Enter SqFt"
        type="number"
        register={register}
        errors={errors}
      />

      <TextInput
        fieldName="lat"
        label="Latitude"
        placeholder="Latitude"
        requiredErrorMessage="Enter Latitude"
        type="number"
        register={register}
        errors={errors}
      />

      <TextInput
        fieldName="lon"
        label="Longitude"
        placeholder="Longitude"
        requiredErrorMessage="Enter Longitude"
        type="number"
        register={register}
        errors={errors}
      />

      <CheckboxInput fieldName="pets" label="Allows Pets" register={register} />

      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-gray-900 dark:text-gray-300">
          Building Amenities
        </label>
        <div className="flex flex-row gap-2 flex-wrap">
          <CheckboxToggle
            fieldName="controlled_access"
            label="Controlled Access"
            register={register}
            value={watch("controlled_access")}
          />
          <CheckboxToggle
            fieldName="fitness_center"
            label="Fitness Center"
            register={register}
            value={watch("fitness_center")}
          />
          <CheckboxToggle
            fieldName="outdoor_space"
            label="Outdoor Space"
            register={register}
            value={watch("outdoor_space")}
          />
          <CheckboxToggle
            fieldName="residents_lounge"
            label="Residents Lounge"
            register={register}
            value={watch("residents_lounge")}
          />
          <CheckboxToggle
            fieldName="roof_deck"
            label="Roof Deck"
            register={register}
            value={watch("roof_deck")}
          />
          <CheckboxToggle
            fieldName="storage"
            label="Storage"
            register={register}
            value={watch("storage")}
          />
          <CheckboxToggle
            fieldName="swimming_pool"
            label="Swimming Pool"
            register={register}
            value={watch("swimming_pool")}
          />
        </div>
      </div>

      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-gray-900 dark:text-gray-300">
          Unit Amenities
        </label>
        <div className="flex flex-row gap-2 flex-wrap">
          <CheckboxToggle
            fieldName="air_conditioning"
            label="Air Conditioning"
            register={register}
            value={watch("air_conditioning")}
          />
          <CheckboxToggle
            fieldName="balcony"
            label="Balcony"
            register={register}
            value={watch("balcony")}
          />
          <CheckboxToggle
            fieldName="furnished"
            label="Furnished"
            register={register}
            value={watch("furnished")}
          />
          <CheckboxToggle
            fieldName="hardwood_floor"
            label="Hardwood Floor"
            register={register}
            value={watch("hardwood_floor")}
          />
          <CheckboxToggle
            fieldName="high_ceilings"
            label="High Ceilings"
            register={register}
            value={watch("high_ceilings")}
          />
          <CheckboxToggle
            fieldName="in_unit_laundry"
            label="In Unit Laundry"
            register={register}
            value={watch("in_unit_laundry")}
          />
        </div>
      </div>

      <button
        onClick={handleSubmit(submitForm)}
        className="my-2 self-center font-medium transition-all hover:bg-slate-700 bg-slate-600 dark:bg-slate-500 dark:hover:bg-slate-400 w-fit px-8 py-2 text-white rounded-full"
      >
        Submit
      </button>
    </div>
  );
}
