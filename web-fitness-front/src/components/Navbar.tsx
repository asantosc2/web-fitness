import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import logo from "../assets/logo.png";
import { useState } from "react";

export default function Navbar() {
  const { estado } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [open, setOpen] = useState(false);

  const cerrarSesion = () => {
    localStorage.clear();
    navigate("/");
    window.location.reload();
  };

  const enlacesPrivados = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/ejercicios", label: "Ejercicios" },
    { path: "/rutinas", label: "Rutinas" },
    { path: "/sesiones-historial", label: "Historial" },
    { path: "/progreso", label: "Progreso" },
    { path: "/consulta-nutricional", label: "Nutrición" }
  ];

  return (
    <nav className="bg-white shadow-md fixed top-0 w-full z-50">
      <div className="w-full h-16 flex items-center justify-between px-4 md:px-8">


        {/* Logo */}
        <Link to="/dashboard" className="flex items-center gap-3">
          <img src={logo} alt="Liftio Logo" className="h-12 w-auto object-contain" />
          <span className="text-xl font-bold text-blue-600">Liftio</span>
        </Link>

        {/* Botón móvil */}
        <div className="md:hidden">
          <button onClick={() => setOpen(!open)} className="text-gray-800 text-2xl">
            ☰
          </button>
        </div>

        {/* Navegación escritorio */}
        <div className="hidden md:flex items-center gap-6 text-sm font-semibold">
          {/* Botones en la pantalla de inicio (landing) si no hay token */}
          {location.pathname === "/" && !estado.token && (
            <div className="hidden md:flex items-center gap-4">
              <Link
                to="/login"
                className="text-blue-600 font-semibold hover:underline"
              >
                Iniciar sesión
              </Link>
              <Link
                to="/registro"
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 font-semibold text-sm"
              >
                Registrarse
              </Link>
            </div>
          )}
          {estado.token &&
            enlacesPrivados.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`hover:text-blue-600 transition ${location.pathname === link.path ? "text-blue-600 font-bold" : ""
                  }`}
              >
                {link.label}
              </Link>
            ))}
          {estado.token && (
            <button
              onClick={cerrarSesion}
              className="text-red-600 hover:text-red-800 transition"
            >
              Cerrar sesión
            </button>
          )}
        </div>
      </div>

      {/* Menú móvil */}
      {open && estado.token && (
        <div className="md:hidden bg-white shadow-inner flex flex-col items-start gap-4 px-6 py-4 text-sm font-semibold">
          {enlacesPrivados.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              onClick={() => setOpen(false)}
              className={`hover:text-blue-600 transition ${location.pathname === link.path ? "text-blue-600 font-bold" : ""
                }`}
            >
              {link.label}
            </Link>
          ))}
          <button
            onClick={cerrarSesion}
            className="text-red-600 hover:text-red-800 transition"
          >
            Cerrar sesión
          </button>
        </div>
      )}
    </nav>
  );
}
