"use client"

import { FieldValues, useForm } from "react-hook-form";
import TextInput from "@/components/Inputs/TextInput";
import CheckboxToggle from "@/components/Inputs/CheckboxToggle";
import CheckboxInput from "@/components/Inputs/CheckboxInput";
import Loading from "@/components/Icons/Loading";
import { fetchLatandLon } from "@/utils";
import defaultValues from "./defaultValues";
import { useState } from "react";

export default function PricePredictForm() {
  const {
    register,
    handleSubmit,
    watch,
    getValues,
    reset,
    formState: { errors },
  } = useForm();

  const [predictedPrice, setPredictedPrice] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<boolean>(false);

  const submitForm = async (data: FieldValues) => {
    setIsLoading(true);
    setError(false);

    if (!process.env.NEXT_PUBLIC_MAPS_API_KEY) {
      console.error("Could not find Maps API key");
      setError(true);
      setIsLoading(false);
      return;
    }

    const { city, address, postal_code } = getValues();
    const { lat, lon } = await fetchLatandLon(
      `${address}, ${postal_code}, ${city}`
    );

    if (!lat || !lon) {
      console.error("Could not find lat or lon");
      setError(true);
      setIsLoading(false);
      return;
    }

    if (!process.env.NEXT_PUBLIC_API_URL) {
      console.error("Could not find API URL");
      setError(true);
      setIsLoading(false);
      return;
    }

    const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/predict`;
    try {
      const apiResponse = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ...data, lat, lon }),
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
        setError(true);
      }
    } catch (error) {
      console.error("Error handling POST request:", error);
      setError(true);
    }
    setIsLoading(false);
  };

  return (
    <div className="max-w-2xl flex flex-col gap-4 p-8 text-sm">
      <h1 className="text-3xl font-medium">Rental Pricing Estimate</h1>
      <p className="text-sm">
        Provide the details for your rental unit listing and we&apos;ll give a
        price prediction for a monthly rate based on this month&apos;s rental
        listings.
      </p>
      <hr className="border-gray-300 dark:border-gray-600" />

      <div className="m-auto p-8 flex flex-col gap-2 items-center">
        {isLoading ? (
          <Loading />
        ) : (
          <>
            {error && (
              <div className="w-full m-auto bg-rose-500/10 border-rose-500 border p-4 text-center rounded">
                <span>❗️ Something went wrong unexpectedly.</span>
              </div>
            )}
            <div className="p-4 border-b border-gray-300 text-4xl md:text-6xl font-medium">
              $ {predictedPrice.toFixed(2)}
            </div>
            <span className="text-sm text-gray-400">
              Predicted monthly rental rate
            </span>
          </>
        )}
      </div>

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
        fieldName="city"
        label="City"
        placeholder="City"
        requiredErrorMessage="Enter City"
        type="string"
        register={register}
        errors={errors}
      />

      <TextInput
        fieldName="postal_code"
        label="Postal Code"
        placeholder="Postal Code"
        requiredErrorMessage="Enter Postal Code"
        type="string"
        register={register}
        errors={errors}
      />

      <TextInput
        fieldName="address"
        label="Address"
        placeholder="Address"
        requiredErrorMessage="Enter Address"
        type="string"
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

      <div className="flex flex-row flex-wrap gap-2 items-center justify-center my-4">
        <button
          onClick={() => reset(defaultValues)}
          className="self-center font-medium transition-all border border-slate-600 text-slate-600 hover:border-emerald-400 hover:text-emerald-400 dark:text-slate-400 dark:border-slate-400 dark:hover:border-emerald-300 dark:hover:text-emerald-300 w-fit px-4 py-2 rounded-full"
        >
          Try an Example
        </button>
        <button
          onClick={handleSubmit(submitForm)}
          className="self-center font-medium transition-all hover:bg-slate-800 bg-slate-600 dark:bg-slate-500 dark:hover:bg-slate-400 w-fit px-8 py-2 text-white rounded-full"
        >
          Submit
        </button>
      </div>
    </div>
  );
}
