import './globals.css'

export const metadata = {
  title: 'Solo Reaction',
  description: 'Conscious Coaching Factory - Solo Reaction Mini App',
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
