import './globals.css';

export const metadata = {
  title: 'Webinar Companion',
  description: 'Interactive Webinar Client',
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
