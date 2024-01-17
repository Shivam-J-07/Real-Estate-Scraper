"use client";

import dynamic from "next/dynamic";
import PricePredictForm from "@/components/PredictPriceForm";

export default function Home() {
  const TableauDashboard = dynamic(
    () => import("@/components/Visualization/Viz"),
    {
      ssr: false,
    }
  );

  return (
    <div className="flex-grow m-auto h-full">
      {/* <TableauDashboard url={"https://public.tableau.com/views/RentRite/BedMetricsvsTime?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link"}/> */}
      <PricePredictForm />
    </div>
  );
}
