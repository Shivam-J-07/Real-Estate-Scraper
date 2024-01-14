import { FieldValues, useForm } from "react-hook-form";

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
    <div className="max-w-lg flex flex-col gap-4 p-8 sm:overflow-y-auto sm:max-h-screen">
      <h1 className="text-3xl font-medium">Rental Pricing Estimate</h1>
      <p className="text-sm">
        Provide the details for your rental unit listing and we&apos;ll give a price
        prediction for a monthly rate based on this month&apos;s rental listings.
      </p>
      <hr className="border-gray-300 dark:border-gray-600" />
      <div className="flex items-center gap-4">
        <label className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">
          Bedrooms
        </label>
        <input
          {...register("bed", {
            required: "Enter number of bedrooms",
          })}
          placeholder="Number of bedrooms"
          className="py-1 px-3 rounded-full border border-gray-300 dark:border-gray-600 dark:bg-gray-600 text-gray-900 dark:text-gray-300"
          type="number"
        />
      </div>
      {errors.bed && (
        <span className="text-red-500 text-sm">{`${errors.bed.message}`}</span>
      )}

      <div className="flex items-center gap-4">
        <label className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">
          Bathrooms
        </label>
        <input
          {...register("bath", {
            required: "Enter number of bathrooms",
          })}
          placeholder="Number of bathrooms"
          className="py-1 px-3 rounded-full border border-gray-300 dark:border-gray-600 dark:bg-gray-600 text-gray-900 dark:text-gray-300"
          type="number"
        />
      </div>
      {errors.bath && (
        <span className="text-red-500 text-sm">{`${errors.bath.message}`}</span>
      )}

      <div className="flex items-center gap-4">
        <label className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">
          Area (sqft)
        </label>
        <input
          {...register("sqft", {
            required: "Enter SqFt",
          })}
          placeholder="Sqft"
          className="py-1 px-3 rounded-full border border-gray-300 dark:border-gray-600 dark:bg-gray-600 text-gray-900 dark:text-gray-300"
          type="number"
        />
      </div>
      {errors.sqft && (
        <span className="text-red-500 text-sm">{`${errors.sqft.message}`}</span>
      )}

      <div className="flex items-center gap-4">
        <label className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">
          Latitude
        </label>
        <input
          {...register("lat", {
            required: "Enter Latitude",
          })}
          placeholder="Latitude"
          className="py-1 px-3 rounded-full border border-gray-300 dark:border-gray-600 dark:bg-gray-600 text-gray-900 dark:text-gray-300"
          type="number"
        />
      </div>
      {errors.lat && (
        <span className="text-red-500 text-sm">{`${errors.lat.message}`}</span>
      )}

      <div className="flex items-center gap-4">
        <label className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">
          Longitude
        </label>
        <input
          {...register("lon", {
            required: "Enter Longitude",
          })}
          placeholder="Longitude"
          className="py-1 px-3 rounded-full border border-gray-300 dark:border-gray-600 dark:bg-gray-600 text-gray-900 dark:text-gray-300"
          type="number"
        />
      </div>
      {errors.lon && (
        <span className="text-red-500 text-sm">{`${errors.lon.message}`}</span>
      )}

      <div className="flex items-center gap-4">
        <label className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">
          Allows Pets
        </label>
        <input
          {...register("pets")}
          id="teal-checkbox"
          type="checkbox"
          value=""
          className="w-4 h-4"
        />
      </div>

      <div className="flex flex-row gap-10">
        <div className="flex flex-col gap-2">
          <label className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">
            Building Amenities
          </label>
          <div className="pl-4">
            <div className="flex items-center gap-4">
              <input
                {...register("controlled_access")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                Controlled Access
              </label>
            </div>
            <div className="flex items-center gap-4">
              <input
                {...register("fitness_center")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                Fitness Center
              </label>
            </div>
            <div className="flex items-center gap-4">
              <input
                {...register("outdoor_space")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                Outdoor Space
              </label>
            </div>
            <div className="flex items-center gap-4">
              <input
                {...register("residents_lounge")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                Residents Lounge
              </label>
            </div>
            <div className="flex items-center gap-4">
              <input
                {...register("roof_deck")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                Roof Deck
              </label>
            </div>
            <div className="flex items-center gap-4">
              <input
                {...register("storage")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                Storage
              </label>
            </div>
            <div className="flex items-center gap-4">
              <input
                {...register("swimming_pool")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                Swimming Pool
              </label>
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-2">
          <label className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">
            Unit Amenities
          </label>
          <div className="pl-4">
            <div className="flex items-center gap-4">
              <input
                {...register("air_conditioning")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                Air Conditioning
              </label>
            </div>
            <div className="flex items-center gap-4">
              <input
                {...register("balcony")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                Balcony
              </label>
            </div>
            <div className="flex items-center gap-4">
              <input
                {...register("furnished")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                Furnished
              </label>
            </div>
            <div className="flex items-center gap-4">
              <input
                {...register("hardwood_floor")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                Hardwood Floor
              </label>
            </div>
            <div className="flex items-center gap-4">
              <input
                {...register("high_ceilings")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                High Ceilings
              </label>
            </div>
            <div className="flex items-center gap-4">
              <input
                {...register("in_unit_laundry")}
                type="checkbox"
                value=""
                className="w-4 h-4"
              />
              <label className="ms-2 text-sm text-gray-900 dark:text-gray-300">
                In Unit Laundry
              </label>
            </div>
          </div>
        </div>
      </div>
      <button
        onClick={handleSubmit(submitForm)}
        className="self-center transition-all hover:bg-sky-600 bg-sky-500 dark:hover:bg-sky-500 dark:bg-sky-600 w-fit px-6 py-1 text-white rounded-full"
      >
        Submit
      </button>
    </div>
  );
}
