import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const { estado } = useAuth();
  const navigate = useNavigate();

  
  return (
    
    <div className="min-h-screen bg-gray-100 pt-24 px-6">
      <Navbar />
      <h1 className="text-3xl font-bold mb-8 text-center text-blue-600">
        ¡Bienvenido, {estado.usuario?.nombre || "usuario"}!
      </h1>

      <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-4 max-w-6xl mx-auto">
        <button
          onClick={() => navigate("/ejercicios")}
          className="bg-white border border-gray-300 hover:border-blue-500 shadow rounded-lg p-6 text-center transition"
        >
          <h2 className="text-xl font-semibold text-gray-800">Ejercicios</h2>
          <p className="text-gray-500 mt-2 text-sm">Explora y aprende nuevos movimientos</p>
        </button>

        <button
          onClick={() => navigate("/rutinas")}
          className="bg-white border border-gray-300 hover:border-blue-500 shadow rounded-lg p-6 text-center transition"
        >
          <h2 className="text-xl font-semibold text-gray-800">Rutinas</h2>
          <p className="text-gray-500 mt-2 text-sm">Crea tu entrenamiento ideal</p>
        </button>

        <button
          onClick={() => navigate("/progreso")}
          className="bg-white border border-gray-300 hover:border-blue-500 shadow rounded-lg p-6 text-center transition"
        >
          <h2 className="text-xl font-semibold text-gray-800">Mi progreso</h2>
          <p className="text-gray-500 mt-2 text-sm">Registra tus avances y fotos</p>
        </button>

        <button
          onClick={() => navigate("/nutricion")}
          className="bg-white border border-gray-300 hover:border-blue-500 shadow rounded-lg p-6 text-center transition"
        >
          <h2 className="text-xl font-semibold text-gray-800">Consulta nutricional</h2>
          <p className="text-gray-500 mt-2 text-sm">Accede a tu plan y consejos</p>
        </button>
      </div>
    </div>
  );
}
