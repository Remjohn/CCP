import { redirect } from 'next/navigation';

export default function DashboardPage() {
    // Redirect to the Pantry as the default dashboard view
    redirect('/dashboard/pantry');
}
