import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import {
  Dumbbell,
  ListTodo,
  BarChart2,
  Salad,
  History
} from "lucide-react";

export default function Dashboard() {
  const { estado } = useAuth();
  const navigate = useNavigate();

  const cards = [
    {
      title: "Ejercicios",
      description: "Explora y aprende nuevos movimientos",
      icon: <Dumbbell size={32} className="text-blue-600" />,
      route: "/ejercicios",
    },
    {
      title: "Rutinas",
      description: "Crea tu entrenamiento ideal",
      icon: <ListTodo size={32} className="text-yellow-500" />,
      route: "/rutinas",
    },
    {
      title: "Historial",
      description: "Revisa tus sesiones anteriores",
      icon: <History size={32} className="text-indigo-600" />,
      route: "/sesiones-historial",
    },
    {
      title: "Mi Progreso",
      description: "Registra tus avances y fotos",
      icon: <BarChart2 size={32} className="text-purple-600" />,
      route: "/progreso",
    },
    {
      title: "Consulta Nutricional",
      description: "Consulta alimentos saludables",
      icon: <Salad size={32} className="text-emerald-600" />,
      route: "/consulta-nutricional",
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-indigo-100 pt-24 px-4">
      <Navbar />
      <h1 className="text-4xl font-bold text-center text-blue-700 mb-12">
        ¡Hola, {estado.usuario?.nombre || "usuario"}!
      </h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {cards.map((card, index) => (
          <div
            key={index}
            onClick={() => navigate(card.route)}
            className="bg-white border hover:border-blue-400 hover:shadow-xl transition cursor-pointer rounded-xl p-6 shadow-sm"
          >
            <div className="flex items-center gap-4">
              <div className="bg-gray-100 p-3 rounded-full shadow">
                {card.icon}
              </div>
              <div>
                <h2 className="text-xl font-semibold text-gray-800">{card.title}</h2>
                <p className="text-sm text-gray-600 mt-1">{card.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
