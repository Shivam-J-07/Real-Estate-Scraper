"use client";

import dynamic from "next/dynamic";

export default function PriceTrends() {
  const TableauDashboard = dynamic(
    () => import("@/components/Visualization/TableauDashboard"),
    {
      ssr: false,
    }
  );

  return (
    <div className="flex flex-col mx-auto w-full gap-4 p-8 lg:px-16">
      <div className="flex flex-col gap-4 max-w-xl">
        <h1 className="text-3xl font-medium w-full text-left">
          Data Visualization
        </h1>
        <p className="text-sm">
          Here&apos;s an overview of the monthly rental unit trends we&apos;ve gathered
          from five major Canadian cities: Toronto, Montreal, Vancouver, Ottawa,
          and Winnipeg. We use this data for our price predictions.
        </p>
        <hr className="border-gray-300 dark:border-gray-600" />
      </div>
      <p className="sm:hidden font-medium m-auto">
        Please rotate your screen or use desktop to view visualizations.
      </p>
      <div className="lg:grid-cols-2 gap-4 sm:grid hidden">
        <TableauDashboard
          url={
            "https://public.tableau.com/views/RentRite/BedMetricsvsTime?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link"
          }
        />
        <TableauDashboard
          url={
            "https://public.tableau.com/views/RentRite/CityvsAvgPrice?:language=en-US&publish=yes&:sid=&:display_count=n&:origin=viz_share_link"
          }
        />
        <TableauDashboard
          url={
            "https://public.tableau.com/views/RentRite/CityMetricsvsTime?:language=en-US&publish=yes&:sid=&:display_count=n&:origin=viz_share_link"
          }
        />
      </div>
    </div>
  );
}
