import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import fondoLanding from "../assets/fondo-landing.jpg";
import Navbar from "../components/Navbar";
import { useEffect } from "react";

export default function Inicio() {
  const { estado } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (estado.token) {
      navigate("/dashboard");
    }
  }, [estado.token]);

  return (
    <div className="flex flex-col font-sans">
      <Navbar />

      {/* Hero Section */}
      <div
        className="min-h-screen pt-24 flex items-center justify-center text-white bg-cover bg-center relative"
        style={{ backgroundImage: `url(${fondoLanding})` }}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-black via-black/50 to-transparent"></div>
        <div className="relative text-center px-6">
          <h1 className="text-4xl md:text-6xl font-extrabold leading-tight mb-4 drop-shadow-lg">
            Liftio – Lleva tu entrenamiento al siguiente nivel
          </h1>
          <p className="text-lg md:text-xl text-gray-200 max-w-2xl mx-auto mb-8 drop-shadow">
            Gestiona tus ejercicios, diseña rutinas, controla tu progreso y accede a información nutricional precisa desde un solo lugar.
          </p>
          <button
            onClick={() => navigate(estado.token ? "/dashboard" : "/login")}
            className="mt-4 px-8 py-3 bg-blue-500 hover:bg-blue-600 rounded-full font-semibold shadow-lg transition-transform transform hover:scale-105"
          >
            Comienza tu viaje
          </button>
        </div>
      </div>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <h2 className="text-center text-4xl font-bold text-gray-800 mb-12">¿Por qué elegir Liftio?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto px-6">
          <div className="bg-blue-50 rounded-2xl shadow-md hover:shadow-xl transition p-6">
            <h3 className="text-xl font-semibold text-blue-600 mb-2">🏋️ Rutinas Personalizadas</h3>
            <p className="text-gray-600">Crea y ajusta entrenamientos adaptados a tus objetivos y nivel de experiencia.</p>
          </div>
          <div className="bg-green-50 rounded-2xl shadow-md hover:shadow-xl transition p-6">
            <h3 className="text-xl font-semibold text-green-600 mb-2">📈 Controla tu Progreso</h3>
            <p className="text-gray-600">Registra peso, fotos y mejoras semanales para medir tu evolución real.</p>
          </div>
          <div className="bg-yellow-50 rounded-2xl shadow-md hover:shadow-xl transition p-6">
            <h3 className="text-xl font-semibold text-yellow-600 mb-2">🥗 Consulta Nutricional</h3>
            <p className="text-gray-600">Busca alimentos reales y conoce sus valores nutricionales desde OpenFoodFacts.</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 py-16 text-center text-white">
        <h2 className="text-3xl md:text-4xl font-bold mb-6">¿Listo para comenzar con Liftio?</h2>
        <button
          onClick={() => navigate(estado.token ? "/dashboard" : "/login")}
          className="px-10 py-3 bg-white text-blue-600 font-semibold rounded-full shadow-lg hover:bg-gray-100 transition"
        >
          Únete Ahora
        </button>
      </section>
    </div>
  );
}
