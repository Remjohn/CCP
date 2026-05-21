import './globals.css';

export const metadata = {
  title: 'Ranking Quiz Co-Creation',
  description: 'Propose your ranking',
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
