"use client";

import { useState } from "react";
import PricePredictForm from "@/components/PredictPriceForm";
import Loading from "@/components/Icons/Loading";

export default function Home() {
  const [predictedPrice, setPredictedPrice] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  return (
    <div className="flex-grow grid grid-cols-1 sm:grid-cols-2">
      <div className="flex flex-col justify-center items-center">
        <PricePredictForm
          setPredictedPrice={setPredictedPrice}
          setIsLoading={setIsLoading}
        />
      </div>
      <div className="m-auto p-8 flex flex-col gap-2 items-center">
        {isLoading ? (
          <Loading />
        ) : (
          <>
            <div className="p-4 border-b border-gray-300 text-6xl font-medium">
              $ {predictedPrice.toFixed(2)}
            </div>
            <span className="text-sm text-gray-400">
              Predicted monthly rental rate
            </span>
          </>
        )}
      </div>
    </div>
  );
}
