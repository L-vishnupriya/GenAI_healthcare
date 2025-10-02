import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import React, { ReactNode } from 'react';
import { CopilotKit } from '@copilotkit/react-core';
import "@copilotkit/react-ui/styles.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Healthcare Multi-Agent System",
  description: "Personalized healthcare tracking and meal planning with AI agents",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  const BACKEND_URL = process.env.NEXT_PUBLIC_AGNO_BACKEND_URL || 'http://localhost:8000';

  return (
    <html lang="en">
      <body className={inter.className}>
        <CopilotKit runtimeUrl={BACKEND_URL}>
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}