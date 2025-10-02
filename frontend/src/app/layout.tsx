import './globals.css';
import React, { ReactNode } from 'react';
import { CopilotKit } from '@copilotkit/react-core';
import "@copilotkit/react-ui/styles.css"; // Import styles for CopilotChat

export default function RootLayout({ children }: { children: ReactNode }) {
  const BACKEND_URL = process.env.NEXT_PUBLIC_AGNO_BACKEND_URL || 'http://localhost:8000';

  return (
    <html lang="en">
      <body>
        <CopilotKit runtimeUrl={BACKEND_URL}>
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}