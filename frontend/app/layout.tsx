import type { Metadata } from "next";
import { GeistSans } from "geist/font/sans";
import "./globals.css";

export const metadata: Metadata = {
  title: "TechAssist",
  description: "Lafayette College Tech Lounge internal workflow tool",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={GeistSans.variable}>
      <body className="bg-bg font-sans text-primary antialiased">{children}</body>
    </html>
  );
}
