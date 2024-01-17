"use client";

import dynamic from "next/dynamic";
import { useState } from "react";
import PricePredictForm from "@/components/PredictPriceForm";
import Loading from "@/components/Icons/Loading";
// import TableauDashboard from "@/components/Visualization/Viz";

export default function Home() {
  const [predictedPrice, setPredictedPrice] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<boolean>(false);

  const TableauDashboard = dynamic(
    () => import("@/components/Visualization/Viz"),
    {
      ssr: false,
    }
  );

  return (
    <div className="flex-grow grid grid-cols-1 sm:grid-cols-2 h-full">
      {/* <TableauDashboard url={"https://public.tableau.com/views/RentRite/BedMetricsvsTime?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link"}/> */}
      <div className="flex flex-col justify-center items-center">
        <PricePredictForm
          setPredictedPrice={setPredictedPrice}
          setIsLoading={setIsLoading}
          setError={setError}
        />
      </div>
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
