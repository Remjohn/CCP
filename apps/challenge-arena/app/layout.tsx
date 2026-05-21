import './globals.css';

export const metadata = {
  title: 'Challenge Arena',
  description: 'CBCS / Law28 Challenge Runtime',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
