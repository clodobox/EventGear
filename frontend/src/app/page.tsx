import Link from 'next/link'
import { Package, Calendar, Users, BarChart } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">EventGear</h1>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            
            <Link href="/equipment" className="card hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4">
                <Package className="h-10 w-10 text-primary-600" />
                <div>
                  <h2 className="text-lg font-semibold">Matériel</h2>
                  <p className="text-gray-600">Gérer le stock</p>
                </div>
              </div>
            </Link>

            <Link href="/projects" className="card hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4">
                <Calendar className="h-10 w-10 text-green-600" />
                <div>
                  <h2 className="text-lg font-semibold">Projets</h2>
                  <p className="text-gray-600">Événements</p>
                </div>
              </div>
            </Link>

            <Link href="/contacts" className="card hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4">
                <Users className="h-10 w-10 text-blue-600" />
                <div>
                  <h2 className="text-lg font-semibold">Contacts</h2>
                  <p className="text-gray-600">Clients & fournisseurs</p>
                </div>
              </div>
            </Link>

            <Link href="/reports" className="card hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4">
                <BarChart className="h-10 w-10 text-purple-600" />
                <div>
                  <h2 className="text-lg font-semibold">Rapports</h2>
                  <p className="text-gray-600">Statistiques</p>
                </div>
              </div>
            </Link>

          </div>
        </div>
      </main>
    </div>
  )
}
