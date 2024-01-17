import React, { useEffect, useRef } from "react";
import { TableauViz } from "@tableau/embedding-api"

interface TableauDashboardProps {
  url: string;
}

const TableauDashboard: React.FC<TableauDashboardProps> = ({ url }) => {
  const tableauVizRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const currentRef = tableauVizRef.current;

    if (currentRef) {
      const viz = new TableauViz();
      viz.src = url;
      currentRef.appendChild(viz);

      return () => {
        if (currentRef) {
          currentRef.removeChild(viz);
        }
      };
    }
  }, [url]);

  return (
    <div ref={tableauVizRef} style={{ width: "800px", height: "600px" }} />
  );
};

export default TableauDashboard;
