import Image from 'next/image';
import Link from 'next/link';
import { LayoutDashboard, Library, Users, Settings } from 'lucide-react';

export function Sidebar() {
    return (
        <div className="w-64 h-screen bg-gray-900 text-white p-4 flex flex-col border-r border-gray-800">
            <div className="flex flex-col items-center mb-8 pt-4">
                <div className="relative w-24 h-24 mb-3 rounded-full overflow-hidden border-4 border-purple-400/30">
                    <Image
                        src="/pamela-face.jpg"
                        alt="Coach Pamela"
                        fill
                        sizes="96px"
                        className="object-cover"
                    />
                </div>
                <div className="text-xl font-bold text-white font-display">Coach Pamela</div>
                <div className="text-xs text-purple-400 uppercase tracking-wider mt-1">Somatic Healing</div>
            </div>
            <nav className="flex-1 space-y-2">
                <Link href="/dashboard" className="flex items-center gap-3 p-3 rounded hover:bg-gray-800 transition-colors">
                    <LayoutDashboard size={20} />
                    <span>Dashboard</span>
                </Link>
                <Link href="/dashboard/pantry" className="flex items-center gap-3 p-3 rounded hover:bg-gray-800 transition-colors">
                    <Library size={20} />
                    <span>Component Pantry</span>
                </Link>
                <Link href="/dashboard/cohort" className="flex items-center gap-3 p-3 rounded hover:bg-gray-800 transition-colors">
                    <Users size={20} />
                    <span>Cohort Vibe</span>
                </Link>
                <Link href="/dashboard/settings" className="flex items-center gap-3 p-3 rounded hover:bg-gray-800 transition-colors">
                    <Settings size={20} />
                    <span>Settings</span>
                </Link>
            </nav>
            <div className="text-sm text-gray-500 mt-auto">
                v1.0.0 (Epic 7)
            </div>
        </div>
    );
}
