import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { title: 'FLARE AI | Research Workspace', description: 'A scientific research workspace for combustion in space.', icons: { icon: '/flare-logo.jpg' } };
export default function Layout({children}:{children:React.ReactNode}) { return <html lang="en"><body>{children}</body></html> }
