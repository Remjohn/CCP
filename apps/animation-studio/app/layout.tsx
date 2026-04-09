import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Animation Studio | Conscious Coaching Factory',
  description: 'CCP Animation Pipeline Editor',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased overflow-hidden w-screen h-screen">
        {children}
      </body>
    </html>
  )
}
