import Link from "next/link";
import { FC } from "react";

import NavLink from "@/components/nav_link";

const LINKS = [
  {
    label: "Questions",
    href: "/questions",
  },
  {
    label: "Tournaments",
    href: "/tournaments",
  },
];

const Header: FC = () => {
  return (
    <header className="ng-scope fixed left-0 top-0 z-50 flex w-full flex-wrap items-stretch justify-between border-b border-metac-blue-200-dark bg-metac-blue-900 text-white">
      <div className="ml-0.5 flex min-h-12 flex-auto">
        <Link
          href="/"
          className="inline-flex max-w-60 flex-shrink-0 flex-grow-0 basis-auto flex-col justify-center text-center no-underline"
        >
          <h1 className="mx-3 my-0 pt-1 font-['alternate-gothic-no-1-d'] text-[30px] font-light tracking-[.08em] text-white antialiased">
            M<span className="hidden xs:inline">etaculus</span>
          </h1>
        </Link>

        <ul className="relative flex flex-auto list-none items-stretch justify-end p-0 text-base font-medium lg:text-sm">
          {LINKS.map((link) => (
            <li key={link.href} className="z-10">
              <NavLink
                href={link.href}
                className="flex h-full items-center p-3 no-underline hover:bg-metac-blue-200-dark"
                activeClassName="bg-metac-blue-300-dark"
              >
                {link.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
    </header>
  );
};

export default Header;