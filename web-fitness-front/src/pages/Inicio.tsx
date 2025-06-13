import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import fondoLanding from "../assets/fondo-landing.jpg";
import Navbar from "../components/Navbar";

export default function Inicio() {
  const { estado } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="flex flex-col">
      <Navbar />

      {/* Hero Section */}
      <div
        className="min-h-screen pt-24 flex items-center justify-center text-white bg-cover bg-center relative"
        style={{ backgroundImage: `url(${fondoLanding})` }}
      >
        <div className="absolute inset-0 bg-black bg-opacity-60"></div>
        <div className="relative text-center px-4">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            Liftio – Tu entrenamiento al siguiente nivel
          </h1>
          <p className="text-xl max-w-2xl mx-auto mb-8">
            Gestiona tus ejercicios, crea rutinas, controla tu progreso y descubre alimentos saludables, todo desde un solo lugar.
          </p>
          <button
            onClick={() => navigate(estado.token ? "/dashboard" : "/login")}
            className="mt-4 px-8 py-3 bg-blue-500 hover:bg-blue-600 rounded-lg font-semibold shadow-xl transition-transform transform hover:scale-105"
          >
            Comienza tu viaje
          </button>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-gray-50">
        <h2 className="text-center text-4xl font-bold text-gray-800 mb-12">
          ¿Por qué elegir Liftio?
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto px-6">
          <div className="bg-white rounded-xl shadow-xl p-6 hover:shadow-2xl transition-shadow">
            <h3 className="text-2xl font-bold text-blue-600 mb-4">Rutinas Personalizadas</h3>
            <p className="text-gray-600">Crea y personaliza rutinas adaptadas a tus objetivos y nivel.</p>
          </div>
          <div className="bg-white rounded-xl shadow-xl p-6 hover:shadow-2xl transition-shadow">
            <h3 className="text-2xl font-bold text-blue-600 mb-4">Controla tu Progreso</h3>
            <p className="text-gray-600">Registra tu evolución con fotos, peso y estadísticas claras.</p>
          </div>
          <div className="bg-white rounded-xl shadow-xl p-6 hover:shadow-2xl transition-shadow">
            <h3 className="text-2xl font-bold text-blue-600 mb-4">Alimentación Inteligente</h3>
            <p className="text-gray-600">Integra tu dieta con alimentos reales desde OpenFoodFacts.</p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-blue-600 py-16 text-center text-white">
        <h2 className="text-4xl font-bold mb-6">¿Listo para comenzar con Liftio?</h2>
        <button
          onClick={() => navigate(estado.token ? "/dashboard" : "/login")}
          className="px-10 py-3 bg-white text-blue-600 font-semibold rounded-lg shadow-lg hover:bg-gray-100 transition-colors"
        >
          Únete Ahora
        </button>
      </div>
    </div>
  );
}