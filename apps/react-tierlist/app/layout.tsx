import './globals.css'

export const metadata = {
  title: 'Tierlist Authority',
  description: 'Conscious Coaching Factory - Tierlist Reaction Mini App',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
