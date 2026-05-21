import './globals.css'

export const metadata = {
  title: 'Debate with Jury',
  description: 'Conscious Coaching Factory - Debate Reaction Mini App',
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
