"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import GitHub from "../Icons/GitHub";
import Logo from "../Icons/Logo";

export default function Header() {
  const currentPath = usePathname();
  const isActive = (pathname: string) => {
    return currentPath === pathname;
  };

  return (
    <header className="w-full px-8 py-4 flex flex-row justify-between text-sm font-medium">
      <div className="flex flex-row items-center gap-2">
        <Logo className="w-5" />
        <span className="self-start">RentRite</span>
      </div>
      <nav className="flex flex-row gap-4">
        <Link
          href="/"
          className={
            isActive("/") ? "text-sky-500" : "hover:text-sky-500 transition-all"
          }
        >
          Price Predictions
        </Link>
        <Link
          href="/trends"
          className={
            isActive("/trends")
              ? "text-sky-500"
              : "hover:text-sky-500 transition-all"
          }
        >
          Market Trends
        </Link>
        <Link
          target="_blank"
          rel="noopener noreferrer"
          href="https://github.com/ShivamJ07/RentRite"
        >
          <GitHub className="w-5 h-5 hover:text-sky-500 transition-all" />
        </Link>
      </nav>
    </header>
  );
}
