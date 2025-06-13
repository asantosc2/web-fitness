import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
  const { estado, logout } = useAuth();
  return (
    <div className="text-center mt-10">
      <h2 className="text-xl">Hola, {estado.usuario?.nombre} 👋</h2>
      <p className="mt-2">Has iniciado sesión correctamente.</p>
      <button onClick={logout} className="mt-4 px-4 py-2 bg-red-600 text-white rounded">
        Cerrar sesión
      </button>
    </div>
  );
}
