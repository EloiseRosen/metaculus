import { config } from "@fortawesome/fontawesome-svg-core";
import "@fortawesome/fontawesome-svg-core/styles.css";
import type { Metadata } from "next";

import Footer from "@/app/(main)/footer";
import Header from "@/app/(main)/header";

config.autoAddCss = false;

export const metadata: Metadata = {
  title: "Metaculus",
  description: "Metaculus rewrite",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <Header />
      <div className="pt-12 ">{children}</div>
      <Footer />
    </>
  );
}